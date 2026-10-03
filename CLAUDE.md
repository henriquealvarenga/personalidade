# Personalidade — livro em Quarto

Livro-texto em português (Quarto *book*), publicado em <https://henriquealvarenga.com/personalidade/>. Um push na `main` publica o site pelo CI; **nunca faça push sem o OK do autor**.

## Data de publicação e ISBN

- A data de publicação é **fixa**: `date: "2026-10-03"` no `_quarto.yml` (exibida como "outubro de 2026"). **Nunca use `date: today`**: com ele, cada render troca a data.
- **Lembrete ao autor:** quando o ISBN do livro sair, revisar juntos todos os lugares abaixo. Inventário feito em 2026-10-03; para conferir se apareceu algum novo, rodar `git ls-files | grep -v -E "^references/|\.bib$" | xargs grep -n -i -E "ISBN|edição|data de publicação|última atualização|\b2026\b|date *:"`.

| Arquivo | Onde | Valor atual | O que fazer |
|---|---|---|---|
| `_quarto.yml` | `book.date` | `"2026-10-03"` (exibe "outubro de 2026" na página inicial) | ajustar para a data oficial da edição com ISBN |
| `_quarto.yml` | `book.edition` | `"2ª edição"` | conferir |
| `creditos.qmd` | ficha bibliográfica | Edição "2ª edição"; Ano "2026"; **ISBN "2ª edição: em cadastramento. A 1ª edição (2020) tem o ISBN 978-65-00-08880-9"** | pôr o ISBN da 2ª edição, manter o da 1ª separado, conferir o ano |
| `creditos.qmd` | "Como citar" — ABNT, Vancouver, APA e BibTeX | ano 2026 nos quatro; BibTeX com `edition = {2}` e `year = {2026}`, sem campo `isbn` | conferir o ano; acrescentar o ISBN onde o formato prevê |
| `creditos.qmd` | fim da página | "*Última atualização: Outubro de 2026*" | atualizar |
| `_includes/autor.html` | dados estruturados (JSON-LD, invisíveis ao leitor, lidos por buscadores) | livro com `"bookEdition": "2ª edição"`, **sem** `isbn`; a 1ª edição em `isBasedOn`, com o ISBN dela | pôr o ISBN novo em `"isbn"` do livro; não mexer no `isBasedOn` |
| `README.md` | topo e linha "Edição" | "2ª edição — 2026"; "2ª edição (2026), ainda sem ISBN. A 1ª edição saiu em 2020 [...] (ISBN 978-65-00-08880-9 [...])" | pôr o ISBN da 2ª edição; manter o da 1ª |
| `epub-metadata.xml` | `dc:date`, `dc:rights` | publicação "2026"; edição "2026-05"; "© 2026" | arquivo sem uso desde a remoção do EPUB (2026-05-23); atualizar só se o EPUB voltar |

- **Duas edições, dois ISBN — não confundir.** O número **978-65-00-08880-9 é da 1ª edição (2020)**, conforme a página de créditos do manuscrito original (`Original_Manuscripts/Personalidade - Uma Breve Introdução.docx`: "Copyright: © 2020 [...] ISBN: 978-65-00-08880-9 · Coleção: Temas em Psicopatologia") e o registro do ISBN, conferido pelo autor em 2026-10-03: *Personalidade: Uma Breve Introdução*, Henrique Alvarenga da Silva, formato digital, situação "Registrado", 04/09/2020 (finalizado em 08/09/2020). Cada edição tem seu próprio ISBN. O site é a **2ª edição**, que ainda não tem ISBN. Até 2026-10-03 o site atribuía por engano esse número à 2ª edição (`autor.html`, desde 2026-08-08); corrigido. Nunca usar o ISBN da 1ª edição como se fosse da 2ª.

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
