# Material fora do livro publicado

Pasta criada em 2026-10-09, a pedido do autor: o Quarto não renderiza pastas que começam com `_`, então nada daqui aparece no site. Tudo veio de dentro do livro, com `git mv` (o histórico de cada arquivo está no git):

| Aqui | Vinha de | O que é |
|---|---|---|
| `parte-4-cultura/` | `capitulos/parte-4-cultura/` | Parte IV, caps. 12–14 (esqueletos: cinema e literatura) |
| `parte-5-atividades/atividade-1-casos/` | `capitulos/parte-5-atividades/atividade-1-casos/` | Atividade 1: casos clínicos A–I (ver `revisao.md` na raiz antes de mexer) |
| `parte-5-atividades/atividade-2-visoes-ia/` | `capitulos/parte-5-atividades/atividade-2-visoes-ia/` | Atividade 2: visões da personalidade com IA |
| `apendices/descoberta-as-avessas.qmd`, `apendices/critica-interdisciplinar.qmd` | `apendices/` | Apêndices I e II (ensaios) |
| `apendices/scripts/` | `apendices/scripts/` | Apêndice III: scripts dos casos (material do professor) |
| `extras/` | `_extras/` | dashboard da Atividade 2, roteiro de aula, 12-casos-clinicos (já estavam fora do livro) |

Os links relativos entre estes arquivos e os capítulos do livro não foram ajustados: só importam quando o material voltar. As citações `[@chave]` continuam sendo validadas por `code/validate_bib.py`, que varre esta pasta.

## Para devolver ao livro

Recolocar os arquivos nos caminhos de origem (`git mv` de volta) e restaurar em `_quarto.yml` os blocos abaixo, exatamente como estavam em 2026-10-09 (as Partes dentro de `chapters:`, antes de `- creditos.qmd`; `appendices:` depois de `chapters:`).

```yaml
    - part: "Parte IV — A personalidade na cultura: cinema e literatura"
      chapters:
        - capitulos/parte-4-cultura/12-personalidade-como-mascara.qmd
        - capitulos/parte-4-cultura/13-personalidade-como-narrativa.qmd
        - capitulos/parte-4-cultura/14-personalidade-no-transtorno.qmd
    - part: "Parte V — Atividades"
      chapters:
        # ── Atividade 1: Casos clínicos (versão para leitura, diagnóstico oculto) ──
        # Nomes neutros (caso-a…caso-i) para o endereço da página não revelar
        # o diagnóstico. Os scripts correspondentes estão no Apêndice C.
        - capitulos/parte-5-atividades/atividade-1-casos/00-introducao.qmd
        - capitulos/parte-5-atividades/atividade-1-casos/caso-a.qmd   # TP Dependente
        - capitulos/parte-5-atividades/atividade-1-casos/caso-b.qmd   # TP Esquizotípica
        - capitulos/parte-5-atividades/atividade-1-casos/caso-c.qmd   # TP Obsessivo-Compulsiva
        - capitulos/parte-5-atividades/atividade-1-casos/caso-d.qmd   # TP Antissocial
        - capitulos/parte-5-atividades/atividade-1-casos/caso-e.qmd   # TP Histriônica
        - capitulos/parte-5-atividades/atividade-1-casos/caso-f.qmd   # TP Narcisista
        - capitulos/parte-5-atividades/atividade-1-casos/caso-g.qmd   # TP Evitativa
        - capitulos/parte-5-atividades/atividade-1-casos/caso-h.qmd   # TP Paranoide
        - capitulos/parte-5-atividades/atividade-1-casos/caso-i.qmd   # TP Borderline
        # Falta: TP Esquizoide (cluster A) — adicionar como Caso J quando pronto.
        # ── Atividade 2: Quatro visões da personalidade × IAs ──
        - capitulos/parte-5-atividades/atividade-2-visoes-ia/01-leitura-preparatoria.qmd
        - capitulos/parte-5-atividades/atividade-2-visoes-ia/02-atividade.qmd
```

```yaml
  appendices:
    - apendices/descoberta-as-avessas.qmd
    - apendices/critica-interdisciplinar.qmd
    # ── Apêndice C: scripts para simulação em vídeo (material do professor) ──
    # Cada script usa number-sections: false, para não ganhar letra própria
    # de apêndice (evita "Apêndice D — Script A").
    - apendices/scripts/00-introducao.qmd
    - apendices/scripts/dependente.qmd      # Script A — TP Dependente
    - apendices/scripts/esquizotipica.qmd   # Script B — TP Esquizotípica
    - apendices/scripts/obsessivo.qmd       # Script C — TP Obsessivo-Compulsiva
    - apendices/scripts/antissocial.qmd     # Script D — TP Antissocial
    - apendices/scripts/histrionica.qmd     # Script E — TP Histriônica
    - apendices/scripts/narcisista.qmd      # Script F — TP Narcisista
    - apendices/scripts/esquiva.qmd         # Script G — TP Evitativa
    - apendices/scripts/paranoide.qmd       # Script H — TP Paranoide
    - apendices/scripts/borderline.qmd      # Script I — TP Borderline

# =========================================================================
# Bibliografia — Nature Publishing Group - NLM/Vancouver (numérico, número
# sobrescrito), processado pelo Citeproc do Pandoc. O CSL tem ajustes locais
# comentados no arquivo (língua padrão pt-BR; ordinal feminino; volume
# ausente; espaço antes da URL e do ano de acesso; edição nos capítulos).
# =========================================================================
```
