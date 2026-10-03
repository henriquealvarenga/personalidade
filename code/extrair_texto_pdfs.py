#!/usr/bin/env python3
"""
extrair_texto_pdfs.py — Gera uma cópia em texto de cada PDF e EPUB de referência.

Para que serve:
  Os PDFs e EPUBs de references/PDF/ são lidos com frequência (conferência 2
  das referências, ver revisao.md). Em texto, dá para procurar em todos de uma vez
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
  4.  EPUBs: o texto segue a ordem de leitura do livro (o spine), com uma
      marca "=== seção N: título ===" no início de cada arquivo interno (N é
      a posição no spine; o título vem do índice do EPUB, ou é o nome do
      arquivo). EPUB não tem páginas: quando ele traz a paginação da edição
      impressa, ela aparece no texto como "[p. N]"; quando não traz, a
      citação com página exige conferir numa edição paginada. EPUBs gerados
      pelo Internet Archive são OCR automático de páginas escaneadas (uma
      seção por página, com erros), e o cabeçalho do .txt avisa.
  5.  Só refaz o .txt quando o PDF/EPUB é mais novo que ele (ou com --tudo).
  6.  Lista os .txt cujo PDF/EPUB não existe mais (renomeado ou apagado); com
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
  0  todos os PDFs e EPUBs têm .txt
  1  algum ficou sem .txt (PDF escaneado sem tesseract, ou erro na extração)
  2  pdftotext/pdftoppm não encontrados (brew install poppler)
"""

from __future__ import annotations

import argparse
import html
import os
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote

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


def extrair_pdf(pdf: Path, pool: ThreadPoolExecutor, lingua: str, tem_ocr: bool) -> tuple[list[str], int, int] | None:
    """Páginas, quantas foram lidas por OCR e quantas eram duplas; None se o PDF não tem texto nenhum."""
    paginas = pdftotext(pdf)
    vazias = [n for n, p in enumerate(paginas, start=1) if len("".join(p.split())) < MIN_CARACTERES]
    lidas_ocr = duplas = 0
    if vazias and tem_ocr:
        if len(vazias) > 2:
            print(f"OCR   {pdf.name} ({len(vazias)} páginas sem texto)")
        for n, texto in zip(vazias, pool.map(lambda n: ocr_pagina(pdf, n, lingua), vazias)):
            if palavras(texto) >= MIN_PALAVRAS_OCR:
                paginas[n - 1] = limpar(texto)
                lidas_ocr += 1
                duplas += "metade esquerda" in texto
    if lidas_ocr == 0 and len(vazias) == len(paginas):
        return None
    return paginas, lidas_ocr, duplas


def escrever_pdf(destino: Path, pdf: Path, paginas: list[str], lidas_ocr: int, duplas: int, lingua: str) -> None:
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


# --- EPUB ---------------------------------------------------------------------

BLOCOS_HTML = {"p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "li", "tr", "blockquote", "section",
               "article", "table", "dd", "dt", "pre", "figcaption", "header", "footer", "aside"}
VAZIOS_HTML = {"br", "hr", "img", "meta", "link", "input", "col", "area", "base", "wbr", "source"}
AVISO_ARCHIVE = "produced in EPUB format by the Internet Archive"


def pagina_impressa(attrs: dict) -> tuple[str, bool] | None:
    """(número, descartar o conteúdo?) se o elemento marca o início de uma página impressa.

    Marcadores explícitos (epub:type="pagebreak", role="doc-pagebreak", classes
    pageno/pagenum do Gutenberg) só contêm o rótulo da página, que é descartado.
    Âncoras id="page_N", comuns em EPUBs de editora, podem envolver texto, que
    é mantido. Outras numerações (ex.: data-ep_ppid="Page-__-N") são do
    programa que gerou o EPUB, não da edição impressa, e são ignoradas.
    """
    tipo = f"{attrs.get('epub:type') or ''} {attrs.get('role') or ''}"
    if "pagebreak" in tipo or re.search(r"page-?(no|num(ber)?)\b", attrs.get("class") or ""):
        rotulo = attrs.get("title") or attrs.get("aria-label") or attrs.get("id") or ""
        m = re.search(r"(\d+|\b[ivxlcdm]+)\s*\]?\s*$", rotulo, re.I)  # "[Pg 3]", "Page_3", "xii"
        return (m.group(1), True) if m else None
    m = re.fullmatch(r"page[_-]?(\d+|[ivxlcdm]+)", attrs.get("id") or "", re.I)
    return (m.group(1), False) if m else None


class TextoXHTML(HTMLParser):
    """Texto de um arquivo XHTML do EPUB: um parágrafo por bloco, [p. N] nas quebras de página."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.partes: list[str] = []
        self.pilha: list[tuple[str, bool]] = []  # (tag, descarta o texto de dentro?)
        self.oculto = 0

    def handle_starttag(self, tag, attrs):
        marca = pagina_impressa(dict(attrs))
        if not self.oculto:
            if tag == "br" or tag in BLOCOS_HTML:
                self.partes.append("\n")
            if marca:
                self.partes.append(f" [p. {marca[0]}] ")
        if tag in VAZIOS_HTML:
            return
        descarta = tag in ("head", "script", "style") or bool(marca and marca[1])
        self.pilha.append((tag, descarta))
        self.oculto += descarta

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VAZIOS_HTML:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in VAZIOS_HTML or tag not in (t for t, _ in self.pilha):
            return
        while self.pilha:  # fecha também o que ficou aberto dentro dele
            t, descarta = self.pilha.pop()
            self.oculto -= descarta
            if t == tag:
                break
        if tag in BLOCOS_HTML and not self.oculto:
            self.partes.append("\n")

    def handle_data(self, data):
        if not self.oculto:
            self.partes.append(data)

    def texto(self) -> str:
        linhas = (" ".join(linha.split()) for linha in "".join(self.partes).split("\n"))
        return re.sub(r"\n{3,}", "\n\n", "\n".join(linhas)).strip()


def secoes_epub(epub: Path) -> list[tuple[int, str, str]]:
    """(posição no spine, título, texto) de cada arquivo do EPUB, na ordem de leitura."""
    with zipfile.ZipFile(epub) as z:
        def ler(caminho: str) -> str:
            return z.read(caminho).decode("utf-8", errors="replace")

        def resolver(base: str, href: str) -> str:
            return posixpath.normpath(posixpath.join(posixpath.dirname(base), unquote(href.split("#")[0])))

        opf = re.search(r'full-path="([^"]+)"', ler("META-INF/container.xml")).group(1)
        pacote = ler(opf)
        itens = {}
        for tag in re.findall(r"<item\s[^>]*>", pacote):
            a = dict(re.findall(r'([\w:-]+)="([^"]*)"', tag))
            itens[a.get("id")] = a
        spine = re.findall(r'<itemref\s[^>]*idref="([^"]+)"', pacote)

        # Títulos do índice: nav do EPUB 3 (só a parte "toc", não a lista de páginas) e NCX do EPUB 2.
        titulos: dict[str, str] = {}
        for a in itens.values():
            href = resolver(opf, a.get("href", ""))
            if "nav" in a.get("properties", "").split():
                toc = re.search(r'<nav[^>]*epub:type="[^"]*\btoc\b[^"]*"[^>]*>(.*?)</nav>', ler(href), re.S)
                pares = re.findall(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', toc.group(1) if toc else "", re.S)
            elif a.get("media-type") == "application/x-dtbncx+xml":
                pares = [(s, t) for t, s in re.findall(
                    r"<navLabel>\s*<text>(.*?)</text>\s*</navLabel>\s*<content[^>]*src=\"([^\"]+)\"", ler(href), re.S)]
            else:
                continue
            for alvo, rotulo in pares:
                rotulo = " ".join(html.unescape(re.sub(r"<[^>]+>", "", rotulo)).split())
                if rotulo:
                    titulos.setdefault(resolver(href, alvo), rotulo[:80])

        secoes = []
        for pos, idref in enumerate(spine, start=1):
            if idref not in itens or "nav" in itens[idref].get("properties", "").split():
                continue  # o índice já virou os títulos das seções
            arquivo = resolver(opf, itens[idref]["href"])
            parser = TextoXHTML()
            parser.feed(ler(arquivo))
            if texto := limpar(parser.texto()):
                secoes.append((pos, titulos.get(arquivo) or posixpath.splitext(posixpath.basename(arquivo))[0], texto))
        return secoes


def escrever_epub(destino: Path, epub: Path, secoes: list[tuple[int, str, str]]) -> None:
    corpo = "\n".join(f"\n=== seção {pos}: {titulo} ===\n{texto}" for pos, titulo, texto in secoes)
    cabecalho = [
        f"# Texto extraído de: {epub.relative_to(PROJECT_ROOT)}",
        f"# Gerado por code/extrair_texto_pdfs.py em {date.today().isoformat()}. Não editar: rodar o script de novo.",
        f"# EPUB, {len(secoes)} seções na ordem de leitura. '=== seção N: título ===' marca o início de cada"
        " arquivo interno do livro (N é a posição no spine).",
    ]
    if re.search(r"\[p\. [^\]]+\]", corpo):
        cabecalho.append("# '[p. N]' marca o início da página N da edição impressa que o EPUB reproduz.")
    else:
        cabecalho.append("# Este EPUB não traz a paginação impressa: citação com página exige conferir numa edição paginada.")
    if AVISO_ARCHIVE in corpo:
        cabecalho.append("# Gerado pelo Internet Archive por OCR automático de páginas escaneadas: cada seção é uma"
                         " página escaneada (o número impresso costuma aparecer no texto); há erros de"
                         " reconhecimento e a ordem de leitura pode falhar.")
    cabecalho.append("# Serve para achar o trecho; confirmar no EPUB antes de anotar no resumo.")
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text("\n".join(cabecalho) + "\n" + corpo + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Gera references/texto/*.txt a partir dos PDFs e EPUBs de references/PDF/.")
    ap.add_argument("--tudo", action="store_true", help="refaz todos os .txt")
    ap.add_argument("--limpar", action="store_true", help="apaga .txt cujo PDF/EPUB não existe mais")
    ap.add_argument("--ocr-lang", default="eng", help="idiomas do OCR, no formato do tesseract (padrão: eng)")
    args = ap.parse_args()

    if not (shutil.which("pdftotext") and shutil.which("pdftoppm")):
        print("pdftotext/pdftoppm não encontrados. Instale com: brew install poppler")
        return 2
    tem_ocr = shutil.which("tesseract") is not None

    # PDFs primeiro: se houver PDF e EPUB com o mesmo nome, o .txt fica com o PDF.
    documentos = sorted(PASTA_PDF.rglob("*.pdf")) + sorted(PASTA_PDF.rglob("*.epub"))
    feitos = pulados = 0
    sem_texto: list[Path] = []
    erros: list[str] = []
    destinos: set[Path] = set()

    with ThreadPoolExecutor(os.cpu_count()) as pool:
        for doc in documentos:
            destino = PASTA_TEXTO / doc.relative_to(PASTA_PDF).with_suffix(".txt")
            if destino in destinos:
                erros.append(f"{doc.name}: há um PDF com o mesmo nome; renomeie um dos dois")
                continue
            destinos.add(destino)
            if not args.tudo and destino.exists() and destino.stat().st_mtime >= doc.stat().st_mtime:
                pulados += 1
                continue
            if doc.suffix == ".epub":
                try:
                    escrever_epub(destino, doc, secoes_epub(doc))
                except (zipfile.BadZipFile, KeyError, AttributeError) as e:
                    erros.append(f"{doc.name}: EPUB ilegível ({type(e).__name__}: {e})")
                    continue
            else:
                try:
                    extraido = extrair_pdf(doc, pool, args.ocr_lang, tem_ocr)
                except subprocess.CalledProcessError as e:
                    erros.append(f"{doc.name}: {str(e.stderr or '').strip()[:200]}")
                    continue
                if extraido is None:
                    sem_texto.append(doc)
                    continue
                escrever_pdf(destino, doc, *extraido, args.ocr_lang)
            feitos += 1

    orfaos = sorted(t for t in PASTA_TEXTO.rglob("*.txt") if t not in destinos) if PASTA_TEXTO.exists() else []

    n_epub = sum(d.suffix == ".epub" for d in documentos)
    print(f"\n{len(documentos) - n_epub} PDFs e {n_epub} EPUBs: {feitos} extraídos agora, {pulados} já estavam em dia.")
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
