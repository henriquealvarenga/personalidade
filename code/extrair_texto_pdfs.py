#!/usr/bin/env python3
"""
extrair_texto_pdfs.py — Gera uma cópia em texto de cada PDF de referência.

Para que serve:
  Os PDFs de references/PDF/ são lidos com frequência (conferência 2 das
  referências, ver revisao.md). Em texto, dá para procurar em todos de uma vez
  (grep) e ler trechos longos gastando muito menos do que lendo o PDF como
  imagem. O texto serve para ACHAR o trecho; a confirmação final, com a página
  anotada no resumo, continua sendo no PDF: tabelas, quadros de destaque e
  páginas em duas colunas podem sair embaralhados. Para ler uma tabela, use
  `pdftotext -layout -f N -l N arquivo.pdf -`.

O que faz:
  1.  Percorre references/PDF/ (com subpastas) e, para cada PDF, escreve
      references/texto/<mesmo caminho>.txt, com uma marca "=== p. N ===" no
      início de cada página. N é a página do ARQUIVO PDF, não a impressa (o
      número impresso costuma aparecer no texto, no topo ou no pé da página).
  2.  Troca ligaduras tipográficas (ﬁ, ﬂ...) pelas letras e apaga hifens
      invisíveis (U+00AD), que impediriam a busca por "classification".
  3.  Páginas sem camada de texto (PDF escaneado, ou figura com texto dentro de
      um PDF com texto) passam por OCR com o tesseract, uma a uma. Se a página
      escaneada tem duas páginas do original lado a lado (página larga com
      margem central em branco), cada metade é lida em separado, da esquerda
      para a direita. Essas páginas começam com a linha "[texto de OCR]".
  4.  Só refaz o .txt quando o PDF é mais novo que ele (ou com --tudo).
  5.  Lista os .txt cujo PDF não existe mais (renomeado ou apagado); com
      --limpar, apaga esses .txt.

references/texto/ fica fora do git (.gitignore), como os PDFs: é texto
integral de obras com direitos autorais. Os resumos (references/resumos/)
continuam sendo o registro versionado da leitura.

Uso:
  python3 code/extrair_texto_pdfs.py            # só PDFs novos ou alterados
  python3 code/extrair_texto_pdfs.py --tudo     # refaz todos
  python3 code/extrair_texto_pdfs.py --limpar   # também apaga .txt órfãos
  python3 code/extrair_texto_pdfs.py --ocr-lang por   # OCR em português
                                                      # (brew install tesseract-lang)

Códigos de saída:
  0  todos os PDFs têm .txt
  1  algum PDF ficou sem .txt (escaneado sem tesseract, ou erro na extração)
  2  pdftotext/pdftoppm não encontrados (brew install poppler)
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PASTA_PDF = PROJECT_ROOT / "references" / "PDF"
PASTA_TEXTO = PROJECT_ROOT / "references" / "texto"

# Página com menos caracteres que isto (sem contar espaços) é tratada como sem
# camada de texto e vai para o OCR.
MIN_CARACTERES = 20
# O OCR só substitui a página se reconhecer ao menos estas palavras; abaixo
# disso a página é figura ou está em branco, e o OCR só traria ruído.
MIN_PALAVRAS_OCR = 40
DPI_OCR = 300
DPI_CALHA = 50

LIGADURAS = str.maketrans({"ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl", "ﬃ": "ffi",
                           "ﬄ": "ffl", "ﬅ": "st", "ﬆ": "st", "­": None})


def limpar(texto: str) -> str:
    return texto.translate(LIGADURAS)


def pdftotext(pdf: Path) -> list[str]:
    """Texto de cada página, na ordem de leitura (sem -layout, que cola colunas)."""
    saida = subprocess.run(
        ["pdftotext", "-enc", "UTF-8", str(pdf), "-"],
        capture_output=True, check=True, text=True, encoding="utf-8", errors="replace",
    ).stdout
    paginas = saida.split("\f")
    if paginas and not paginas[-1].strip():
        paginas.pop()  # o pdftotext termina com um \f após a última página
    return [limpar(p) for p in paginas]


def renderizar(pdf: Path, n: int, pasta: str, dpi: int, *extra: str) -> Path:
    raiz = f"{pasta}/p{n}_{dpi}_{'_'.join(extra)}"
    subprocess.run(["pdftoppm", "-r", str(dpi), "-f", str(n), "-l", str(n), "-singlefile",
                    *extra, str(pdf), raiz], capture_output=True, check=True)
    return next(Path(pasta).glob(Path(raiz).name + ".*"))


def ler_pgm(img: Path) -> tuple[int, int, bytes]:
    """Largura, altura e pixels (1 byte cada) de uma imagem PGM do pdftoppm -gray."""
    dados = img.read_bytes()
    _, w, h = dados.split(maxsplit=3)[:3]  # cabeçalho: P5 <largura> <altura> 255
    w, h = int(w), int(h)
    return w, h, dados[-w * h:]


def calha(pdf: Path, n: int, pasta: str) -> float | None:
    """Posição (fração da largura) da margem central de uma página dupla, ou None."""
    w, h, pixels = ler_pgm(renderizar(pdf, n, pasta, DPI_CALHA, "-gray"))
    if w < 1.2 * h:
        return None
    linhas = range(int(0.1 * h), int(0.9 * h))
    for x in sorted(range(int(0.4 * w), int(0.6 * w)), key=lambda x: abs(x - w / 2)):
        if sum(pixels[y * w + x] < 128 for y in linhas) <= 0.005 * len(linhas):
            return x / w
    return None


def ocr_pagina(pdf: Path, n: int, lingua: str) -> str:
    def tesseract(img: Path) -> str:
        texto = subprocess.run(["tesseract", str(img), "-", "-l", lingua], capture_output=True,
                               text=True, check=True, env={**os.environ, "OMP_THREAD_LIMIT": "1"}).stdout
        # Junta palavras partidas no fim da linha ("experi-\nmenter"), como o
        # pdftotext já faz nos PDFs com texto.
        return re.sub(r"([a-zà-ÿ])-\n([a-zà-ÿ])", r"\1\2", texto)

    with tempfile.TemporaryDirectory() as pasta:
        corte = calha(pdf, n, pasta)
        if corte is None:
            return "[texto de OCR]\n" + tesseract(renderizar(pdf, n, pasta, DPI_OCR, "-gray"))
        largura, altura, _ = ler_pgm(renderizar(pdf, n, pasta, DPI_OCR, "-gray"))
        x = int(corte * largura)
        esq = renderizar(pdf, n, pasta, DPI_OCR, "-gray", "-x", "0", "-y", "0", "-W", str(x), "-H", str(altura))
        dir_ = renderizar(pdf, n, pasta, DPI_OCR, "-gray", "-x", str(x), "-y", "0",
                          "-W", str(largura - x), "-H", str(altura))
        return (f"[texto de OCR — metade esquerda]\n{tesseract(esq).rstrip()}\n\n"
                f"[texto de OCR — metade direita]\n{tesseract(dir_)}")


def palavras(texto: str) -> int:
    return len(re.findall(r"[A-Za-zÀ-ÿ]{3,}", texto))


def escrever(destino: Path, pdf: Path, paginas: list[str], lidas_ocr: int, duplas: int, lingua: str) -> None:
    cabecalho = [
        f"# Texto extraído de: {pdf.relative_to(PROJECT_ROOT)}",
        f"# Gerado por code/extrair_texto_pdfs.py em {date.today().isoformat()}. Não editar: rodar o script de novo.",
        f"# {len(paginas)} páginas. '=== p. N ===' é a página do arquivo PDF, não a impressa.",
        "# Serve para achar o trecho; confirmar no PDF antes de anotar no resumo.",
    ]
    if lidas_ocr:
        cabecalho.append(f"# {lidas_ocr} página(s) lidas por OCR (tesseract, {lingua}), marcadas com"
                         " [texto de OCR]: pode haver erros de reconhecimento.")
    if duplas:
        cabecalho.append(f"# Em {duplas} delas o PDF traz duas páginas do original lado a lado;"
                         " cada metade foi lida em separado.")
    corpo = [f"\n=== p. {n} ===\n{p.rstrip()}" for n, p in enumerate(paginas, start=1)]
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text("\n".join(cabecalho) + "\n" + "\n".join(corpo) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Gera references/texto/*.txt a partir de references/PDF/*.pdf.")
    ap.add_argument("--tudo", action="store_true", help="refaz todos os .txt")
    ap.add_argument("--limpar", action="store_true", help="apaga .txt cujo PDF não existe mais")
    ap.add_argument("--ocr-lang", default="eng", help="idiomas do OCR, no formato do tesseract (padrão: eng)")
    args = ap.parse_args()

    if not (shutil.which("pdftotext") and shutil.which("pdftoppm")):
        print("pdftotext/pdftoppm não encontrados. Instale com: brew install poppler")
        return 2
    tem_ocr = shutil.which("tesseract") is not None

    pdfs = sorted(PASTA_PDF.rglob("*.pdf"))
    feitos = pulados = 0
    sem_texto: list[Path] = []
    erros: list[str] = []

    with ThreadPoolExecutor(os.cpu_count()) as pool:
        for pdf in pdfs:
            destino = PASTA_TEXTO / pdf.relative_to(PASTA_PDF).with_suffix(".txt")
            if not args.tudo and destino.exists() and destino.stat().st_mtime >= pdf.stat().st_mtime:
                pulados += 1
                continue
            try:
                paginas = pdftotext(pdf)
                vazias = [n for n, p in enumerate(paginas, start=1) if len("".join(p.split())) < MIN_CARACTERES]
                if vazias and not tem_ocr and len(vazias) == len(paginas):
                    sem_texto.append(pdf)
                    continue
                lidas_ocr = duplas = 0
                if vazias and tem_ocr:
                    if len(vazias) > 2:
                        print(f"OCR   {pdf.name} ({len(vazias)} páginas sem texto)")
                    for n, texto in zip(vazias, pool.map(lambda n: ocr_pagina(pdf, n, args.ocr_lang), vazias)):
                        if palavras(texto) >= MIN_PALAVRAS_OCR:
                            paginas[n - 1] = limpar(texto)
                            lidas_ocr += 1
                            duplas += "metade esquerda" in texto
                if lidas_ocr == 0 and len(vazias) == len(paginas):
                    sem_texto.append(pdf)
                    continue
            except subprocess.CalledProcessError as e:
                erros.append(f"{pdf.name}: {str(e.stderr or '').strip()[:200]}")
                continue
            escrever(destino, pdf, paginas, lidas_ocr, duplas, args.ocr_lang)
            feitos += 1

    esperados = {PASTA_TEXTO / p.relative_to(PASTA_PDF).with_suffix(".txt") for p in pdfs}
    orfaos = sorted(t for t in PASTA_TEXTO.rglob("*.txt") if t not in esperados) if PASTA_TEXTO.exists() else []

    print(f"\n{len(pdfs)} PDFs: {feitos} extraídos agora, {pulados} já estavam em dia.")
    if sem_texto:
        dica = "" if tem_ocr else " (instale o OCR: brew install tesseract)"
        print(f"\n{len(sem_texto)} PDF(s) escaneados, sem texto{dica}:")
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
