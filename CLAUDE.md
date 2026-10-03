# Personalidade — livro em Quarto

Livro-texto em português (Quarto *book*), publicado em <https://henriquealvarenga.com/personalidade/>. Um push na `main` publica o site pelo CI; **nunca faça push sem o OK do autor**.

## Data de publicação e ISBN

- A data de publicação é **fixa**: `date: "2026-10-03"` no `_quarto.yml` (exibida como "outubro de 2026"). **Nunca use `date: today`**: com ele, cada render troca a data.
- **Lembrete ao autor:** quando o ISBN do livro sair, revisar juntos todos os lugares abaixo. Inventário feito em 2026-10-03; para conferir se apareceu algum novo, rodar `git ls-files | grep -v -E "^references/|\.bib$" | xargs grep -n -i -E "ISBN|edição|data de publicação|última atualização|\b2026\b|date *:"`.

| Arquivo | Onde | Valor atual | O que fazer |
|---|---|---|---|
| `_quarto.yml` | `book.date` | `"2026-10-03"` (exibe "outubro de 2026" na página inicial) | ajustar para a data oficial da edição com ISBN |
| `_quarto.yml` | `book.edition` | `"2ª edição"` | conferir |
| `creditos.qmd` | ficha bibliográfica | Edição "2ª edição"; Ano "2026"; **ISBN "em cadastramento"** | pôr o ISBN e conferir o ano |
| `creditos.qmd` | "Como citar" — ABNT, Vancouver, APA e BibTeX | ano 2026 nos quatro; BibTeX com `edition = {2}` e `year = {2026}`, sem campo `isbn` | conferir o ano; acrescentar o ISBN onde o formato prevê |
| `creditos.qmd` | fim da página | "*Última atualização: Outubro de 2026*" | atualizar |
| `_includes/autor.html` | dados estruturados (JSON-LD do livro, invisíveis ao leitor, lidos por buscadores) | **`"isbn": "978-65-00-08880-9"`**, publicado desde 2026-08-08 | **pendência:** os Créditos dizem "em cadastramento". Confirmar se esse ISBN é deste livro (talvez da 1ª edição); trocar pelo novo ou remover |
| `README.md` | topo e seção "Edição" | "2ª edição — 2026"; "2ª edição (2026); a 1ª edição circulou em 2020" | conferir |
| `epub-metadata.xml` | `dc:date`, `dc:rights` | publicação "2026"; edição "2026-05"; "© 2026" | arquivo sem uso desde a remoção do EPUB (2026-05-23); atualizar só se o EPUB voltar |

  Não são datas do livro e **não** devem mudar: "Data de publicação: 30 de abril de 2017" em `creditos.qmd` (é da foto da capa); "escrito originalmente em 2020" em `index.qmd` (história da 1ª edição); `_extras/analise_personalidade.qmd` usa `Sys.Date()`, mas `_extras/` não entra no livro.

## Casos clínicos da Atividade 1

Antes de qualquer trabalho nos casos clínicos (`capitulos/parte-5-atividades/atividade-1-casos/` ou `apendices/scripts/`), **leia [revisao.md](revisao.md) inteiro** e siga o roteiro de sessão descrito lá. Ao final da sessão, atualize o progresso e o diário nesse arquivo.

## Referências (valem para o livro todo)

- **Nunca invente referências.** Nada de autor, título, ano, periódico ou DOI tirado da memória.
- Toda referência é **conferida duas vezes** antes de entrar no texto: primeiro os metadados (Crossref, PubMed, editora), depois o conteúdo (de preferência no PDF, lido e resumido).
- Toda referência citada entra em `references/references.bib`, seguindo as convenções do cabeçalho desse arquivo.
- O procedimento completo está em [revisao.md](revisao.md), na seção "Regras sobre referências".

## Verificação

- `python3 code/validate_bib.py --no-doi`: citações sem entrada no `.bib`, campos ABNT, padrão das chaves.
- `rm -rf _book && quarto render --to html`: o livro deve ser gerado sem avisos.
- `python3 code/verificar_spoiler.py`: confere se as páginas de caso revelam o diagnóstico fora dos blocos recolhidos.
