#!/usr/bin/env python3
"""
extrair_texto_pdfs.py — Gera uma cópia em texto de cada PDF de referência.

Para que serve:
  Os PDFs de references/PDF/ são lidos com frequência (conferência 2 das
  referências, ver revisao.md). Em texto, dá para procurar em todos de uma vez
  (grep) e ler trechos longos gastando muito menos do que lendo o PDF como
  imagem. O texto serve para ACHAR o trecho; a confirmação final, com a página
  anotada no resumo, continua sendo no PDF (tabelas e páginas em duas colunas
  saem embaralhadas na extração).

O que faz:
  1.  Percorre references/PDF/ (com subpastas) e, para cada PDF, escreve
      references/texto/<mesmo caminho>.txt, com uma marca "=== p. N ===" no
      início de cada página. N é a página do ARQUIVO PDF, não a impressa.
  2.  Só refaz o .txt quando o PDF é mais novo que ele (ou com --tudo).
  3.  PDFs sem camada de texto (escaneados) passam por OCR se o ocrmypdf
      estiver instalado; senão, são listados no fim e ficam sem .txt.
  4.  Lista os .txt cujo PDF não existe mais (renomeado ou apagado); com
      --limpar, apaga esses .txt.

references/texto/ fica fora do git (.gitignore), como os PDFs: é texto
integral de obras com direitos autorais. Os resumos (references/resumos/)
continuam sendo o registro versionado da leitura.

Uso:
  python3 code/extrair_texto_pdfs.py            # só PDFs novos ou alterados
  python3 code/extrair_texto_pdfs.py --tudo     # refaz todos
  python3 code/extrair_texto_pdfs.py --limpar   # também apaga .txt órfãos
  python3 code/extrair_texto_pdfs.py --ocr-lang eng+por

Códigos de saída:
  0  todos os PDFs têm .txt
  1  algum PDF ficou sem .txt (escaneado sem OCR, ou erro na extração)
  2  pdftotext não encontrado (brew install poppler)
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PASTA_PDF = PROJECT_ROOT / "references" / "PDF"
PASTA_TEXTO = PROJECT_ROOT / "references" / "texto"

# Abaixo desta média de caracteres (sem espaços) por página, o PDF é tratado
# como escaneado. Capas e páginas em branco não chegam a puxar um livro com
# texto para baixo disso.
MIN_CARACTERES_POR_PAGINA = 20


def pdftotext(pdf: Path) -> list[str]:
    """Texto de cada página, na ordem de leitura (sem -layout, que cola colunas)."""
    saida = subprocess.run(
        ["pdftotext", "-enc", "UTF-8", str(pdf), "-"],
        capture_output=True, check=True, text=True, encoding="utf-8", errors="replace",
    ).stdout
    paginas = saida.split("\f")
    if paginas and not paginas[-1].strip():
        paginas.pop()  # o pdftotext termina com um \f após a última página
    return paginas


def tem_texto(paginas: list[str]) -> bool:
    caracteres = sum(len("".join(p.split())) for p in paginas)
    return bool(paginas) and caracteres >= MIN_CARACTERES_POR_PAGINA * len(paginas)


def ocr(pdf: Path, lingua: str) -> list[str]:
    with tempfile.TemporaryDirectory() as tmp:
        saida = Path(tmp) / "ocr.pdf"
        subprocess.run(
            ["ocrmypdf", "--quiet", "--skip-text", "-l", lingua, str(pdf), str(saida)],
            capture_output=True, check=True,
        )
        return pdftotext(saida)


def escrever(destino: Path, pdf: Path, paginas: list[str], origem: str) -> None:
    rel = pdf.relative_to(PROJECT_ROOT)
    cabecalho = [
        f"# Texto extraído de: {rel}",
        f"# Gerado por code/extrair_texto_pdfs.py em {date.today().isoformat()} ({origem}). Não editar: rodar o script de novo.",
        f"# {len(paginas)} páginas. '=== p. N ===' é a página do arquivo PDF, não a impressa.",
        "# Serve para achar o trecho; confirmar no PDF antes de anotar no resumo.",
    ]
    if origem.startswith("OCR"):
        cabecalho.append("# Texto de OCR: pode ter erros de reconhecimento.")
    corpo = [f"\n=== p. {n} ===\n{p.rstrip()}" for n, p in enumerate(paginas, start=1)]
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text("\n".join(cabecalho) + "\n" + "\n".join(corpo) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Gera references/texto/*.txt a partir de references/PDF/*.pdf.")
    ap.add_argument("--tudo", action="store_true", help="refaz todos os .txt")
    ap.add_argument("--limpar", action="store_true", help="apaga .txt cujo PDF não existe mais")
    ap.add_argument("--ocr-lang", default="eng", help="idiomas do OCR, no formato do tesseract (padrão: eng)")
    args = ap.parse_args()

    if not shutil.which("pdftotext"):
        print("pdftotext não encontrado. Instale com: brew install poppler")
        return 2
    tem_ocr = shutil.which("ocrmypdf") is not None

    pdfs = sorted(PASTA_PDF.rglob("*.pdf"))
    feitos = pulados = 0
    sem_texto: list[Path] = []
    erros: list[str] = []

    for pdf in pdfs:
        destino = PASTA_TEXTO / pdf.relative_to(PASTA_PDF).with_suffix(".txt")
        if not args.tudo and destino.exists() and destino.stat().st_mtime >= pdf.stat().st_mtime:
            pulados += 1
            continue
        try:
            paginas = pdftotext(pdf)
            origem = "pdftotext"
            if not tem_texto(paginas):
                if not tem_ocr:
                    sem_texto.append(pdf)
                    continue
                print(f"OCR   {pdf.name}")
                paginas, origem = ocr(pdf, args.ocr_lang), f"OCR ocrmypdf, {args.ocr_lang}"
        except subprocess.CalledProcessError as e:
            erros.append(f"{pdf.name}: {(e.stderr or b'').strip()[:200]!r}")
            continue
        escrever(destino, pdf, paginas, origem)
        feitos += 1

    esperados = {PASTA_TEXTO / p.relative_to(PASTA_PDF).with_suffix(".txt") for p in pdfs}
    orfaos = sorted(t for t in PASTA_TEXTO.rglob("*.txt") if t not in esperados) if PASTA_TEXTO.exists() else []

    print(f"\n{len(pdfs)} PDFs: {feitos} extraídos agora, {pulados} já estavam em dia.")
    if sem_texto:
        print(f"\n{len(sem_texto)} PDF(s) escaneados, sem texto (instale o OCR: brew install ocrmypdf):")
        for p in sem_texto:
            print(f"  - {p.relative_to(PASTA_PDF)}")
    if erros:
        print(f"\n{len(erros)} erro(s) na extração:")
        for e in erros:
            print(f"  - {e}")
    if orfaos:
        acao = "apagados" if args.limpar else "órfãos (rode com --limpar para apagar)"
        print(f"\n{len(orfaos)} .txt {acao}:")
        for t in orfaos:
            print(f"  - {t.relative_to(PASTA_TEXTO)}")
            if args.limpar:
                t.unlink()

    return 1 if sem_texto or erros else 0


if __name__ == "__main__":
    sys.exit(main())
