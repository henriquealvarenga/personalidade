#!/usr/bin/env python3
"""
verificar_spoiler.py — Confere se as páginas de caso revelam o diagnóstico.

O que faz:
  1.  Lê as páginas geradas dos casos de leitura da Atividade 1
      (_book/capitulos/parte-5-atividades/atividade-1-casos/caso-*.html).
  2.  Descarta o conteúdo dos blocos recolhidos (div.callout-collapse), que é
      onde o diagnóstico deve ficar, o menu lateral (igual em todas as
      páginas; os endereços dos scripts no apêndice contêm o diagnóstico por
      decisão do autor) e a lista de referências do fim da página (div#refs;
      os títulos das obras podem nomear o diagnóstico, decisão do autor em
      2026-10-03).
  3.  Procura no restante (título, subtítulo, história, pergunta, sumário,
      atributos como title/alt/href) termos que nomeiem algum diagnóstico.
  4.  Confere que cada página tem os 5 blocos recolhidos e que todos começam
      fechados.

Uso (depois de `quarto render --to html`):
  python3 code/verificar_spoiler.py            # todos os casos
  python3 code/verificar_spoiler.py caso-a     # só um caso

Códigos de saída:
  0  nenhum diagnóstico visível
  1  termo de diagnóstico visível ou bloco faltando/aberto
  2  páginas não encontradas (rode o render antes)
"""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PASTA = PROJECT_ROOT / "_book" / "capitulos" / "parte-5-atividades" / "atividade-1-casos"
BLOCOS_ESPERADOS = 5

# Radicais que denunciam um diagnóstico de personalidade (com e sem acento).
TERMOS = [
    "dependente", "esquizotíp", "esquizotip", "esquizoide", "obsessiv", "anancást",
    "anancast", "antissocial", "dissocial", "psicopata", "psicopatia", "histriôn", "histrion",
    "narcis", "evitativ", "esquiv", "paranoi", "borderline", "limítrofe",
]

VAZIOS = {"area", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "wbr"}
ATRIBUTOS = ("href", "title", "aria-label", "alt", "content")


class TextoVisivel(HTMLParser):
    """Junta o texto e os atributos fora dos blocos recolhidos e do menu lateral."""

    def __init__(self) -> None:
        super().__init__()
        self.pilha: list[bool] = []
        self.oculto = 0
        self.partes: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if self.oculto == 0:
            self.partes += [str(v) for k, v in a.items() if v and k in ATRIBUTOS]
        if tag in VAZIOS:
            return
        classes = (a.get("class") or "").split()
        entra = (
            (tag == "div" and "callout-collapse" in classes)
            or (tag == "nav" and a.get("id") == "quarto-sidebar")
            or (tag == "div" and a.get("id") == "refs")
        )
        self.pilha.append(entra)
        if entra:
            self.oculto += 1

    def handle_endtag(self, tag):
        if tag in VAZIOS:
            return
        if self.pilha and self.pilha.pop():
            self.oculto -= 1

    def handle_data(self, data):
        if self.oculto == 0:
            self.partes.append(data)


def verificar(pagina: Path) -> list[str]:
    html = pagina.read_text(encoding="utf-8")
    parser = TextoVisivel()
    parser.feed(html)
    visivel = " ".join(parser.partes).lower()

    problemas = [f"termo visível: '{t}'" for t in TERMOS if t in visivel]
    blocos = re.findall(r'<div[^>]*class="([^"]*callout-collapse[^"]*)"', html)
    if len(blocos) != BLOCOS_ESPERADOS:
        problemas.append(f"{len(blocos)} blocos recolhidos (esperado: {BLOCOS_ESPERADOS})")
    abertos = [b for b in blocos if "show" in b.split()]
    if abertos:
        problemas.append(f"{len(abertos)} bloco(s) começam abertos")
    return problemas


def main() -> int:
    filtro = sys.argv[1] if len(sys.argv) > 1 else "caso-"
    paginas = sorted(PASTA.glob(f"{filtro}*.html"))
    if not paginas:
        print(f"Nenhuma página '{filtro}*.html' em {PASTA}. Rode `quarto render --to html` antes.")
        return 2

    falhou = False
    for pagina in paginas:
        problemas = verificar(pagina)
        if problemas:
            falhou = True
            print(f"FALHA {pagina.name}: " + "; ".join(problemas))
        else:
            print(f"OK    {pagina.name}")
    return 1 if falhou else 0


if __name__ == "__main__":
    sys.exit(main())
