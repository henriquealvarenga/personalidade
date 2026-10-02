# Personalidade — livro em Quarto

Livro-texto em português (Quarto *book*), publicado em <https://henriquealvarenga.com/personalidade/>. Um push na `main` publica o site pelo CI; **nunca faça push sem o OK do autor**.

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
