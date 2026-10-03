# Revisão dos casos clínicos da Atividade 1

Guia para as sessões em que os casos de leitura da Atividade 1 são escritos. **Cada sessão trata de um único caso.** Leia este arquivo inteiro antes de começar e atualize as seções [Progresso](#progresso) e [Diário das sessões](#diário-das-sessões) ao terminar.

## Contexto

Cada caso clínico existe em duas versões:

| Versão | Onde | Situação |
|---|---|---|
| **Leitura** (Atividade 1) | `capitulos/parte-5-atividades/atividade-1-casos/caso-x.qmd` | esqueleto publicado, a escrever |
| **Script** para simulação em vídeo (Apêndice C) | `apendices/scripts/<diagnóstico>.qmd` | pronto; é a **fonte** da história clínica |

Cada página de leitura tem, nesta ordem:

1. aviso "Página em elaboração" (sai quando o caso fica pronto);
2. **História clínica**, visível;
3. **Sua hipótese**, a pergunta ao aluno, visível e já escrita;
4. **Discussão**, com cinco blocos recolhidos que só abrem com um clique:
   - Ver o diagnóstico;
   - História do diagnóstico na psiquiatria;
   - Importância do diagnóstico hoje;
   - O diagnóstico no DSM-5-TR e na CID-11;
   - Críticas ao diagnóstico.

Cada campo vazio tem um comentário `<!-- -->`, invisível no site, que indica de onde tirar o material.

**Atenção:** um push na `main` publica o site, porque o CI renderiza e faz o deploy. Nunca faça push sem o OK do autor.

## Regras sobre referências — inegociáveis

1. **NUNCA inventar referências.** Nenhum autor, título, ano, periódico, volume, página ou DOI pode vir da memória. Uma afirmação sem fonte conferida tem dois destinos possíveis:
   - fica sem citação, marcada com `<!-- FALTA REFERÊNCIA: o que precisa de fonte -->`, e o autor é avisado; ou
   - sai do texto.

   Citação aproximada, "plausível" ou reconstruída não é aceitável em hipótese alguma.

2. **Toda referência é conferida duas vezes antes de entrar no texto:**
   - **Conferência 1 — a obra existe e os metadados estão certos.**
     - Artigos: resolver o DOI na Crossref ou achar o registro no PubMed, e confirmar autores, ano, título, periódico, volume e páginas.
     - Livros: página da editora ou catálogo com ISBN.
   - **Conferência 2 — a obra diz o que o texto afirma.**
     - Confirmar no PDF, anotando a página no resumo (regra 4).
     - Se só o *abstract* estiver acessível, registrar isso no resumo e limitar a afirmação ao que o *abstract* diz.

3. **Toda referência citada entra em `references/references.bib`**, seguindo as convenções do cabeçalho do arquivo:
   - **Chave:** `autor_palavra-chave_ano`, em ASCII puro. Exemplo: `bach_icd11_personality_2018`.
   - **`note`:** `verified-doi: AAAA-MM-DD` quando o DOI foi conferido.
   - **`keywords`:** `clinica`, `historica` etc.
   - **DOI e/ou URL** sempre que existirem.
   - **Duplicatas:** antes de criar uma entrada, procurar uma existente com `grep` pelo DOI e por palavras do título. Reaproveitar o que já está lá: os capítulos 8 a 10 já citam o DSM-5 (`apa_dsm5_2013`), a CID-11 (`who_icd11_2022`, `bach_icd11_personality_2018`, `reed_innovations_2019`, `mulder_*`, `tyrer_doghouse_2020`) e estudos de prevalência (`volkert_prevalence_2018`, `torgersen_prevalence_2001`, `zimmerman_*`).
   - **Entradas `pending-verification`:** só podem ser usadas depois de passar pelas duas conferências. Ao conferir, atualize o `note`.
   - **Fusão de lotes:** para fundir um lote de referências com conferência na Crossref e backup datado, use a skill `bib-merge-pdfs`, se disponível, mantendo o `note` no formato do cabeçalho do `.bib`.

4. **PDFs: de preferência, ler e resumir antes de usar.**
   - **Onde guardar os PDFs:** em `references/PDF/`, com o nome `SobrenomeAno - Título.pdf`: só o sobrenome do primeiro autor, colado ao ano (ex.: `Goldberg1993 - The structure of phenotypic personality traits.pdf`); os dois-pontos do título viram ` - `. É uma pasta local, fora do git, conforme o `.gitignore`.
   - **Onde guardar os resumos:** em `references/resumos/<chave>.md`. Os resumos são **versionados**, porque os PDFs não vão para o git e as próximas sessões dependem deles. Escreva o resumo antes de citar a obra no caso.
   - **Origem dos PDFs:** só fontes legítimas (editora, PubMed Central, repositório do autor, acesso institucional). Antes de baixar qualquer arquivo, peça confirmação ao autor informando o nome do arquivo, a origem e o tamanho. Se o PDF não estiver acessível, peça ao autor; nunca baixe de sites piratas.
   - **Direitos autorais:** resuma com palavras próprias. Citações literais devem ser curtas e sempre com a página.

5. **Coerência com o livro.** Toda afirmação sobre classificação (DSM, CID, códigos, domínios de traço) deve bater com o Cap. 8 (`08-transtornos.qmd`, tabela `@tbl-dsm-cid11`). Se a fonte divergir do capítulo, **avise o autor em vez de escolher sozinho**.

### Modelo de resumo (`references/resumos/<chave>.md`)

```markdown
# <chave>

- **Referência:** <referência completa, como no .bib>
- **DOI / URL:** <...>
- **Conferência 1 (metadados):** <Crossref | PubMed | editora> em AAAA-MM-DD
- **Conferência 2 (conteúdo):** <PDF lido integralmente | partes (páginas) | só o abstract>

## O que a obra diz
<5 a 15 linhas, com palavras próprias>

## Trechos úteis para os casos
- p. <n>: <ideia, ou citação curta entre aspas>

## Onde é citada no livro
- `caso-x.qmd`, bloco "<nome do bloco>": <afirmação apoiada>
```

## Roteiro de cada sessão

0. **Preparar.**
   - Rodar `git status`.
   - Ler a linha do caso na tabela de [Progresso](#progresso), o `caso-x.qmd` e o script correspondente inteiro.
   - Ler no Cap. 8 a seção sobre a CID-11 e a tabela de correspondência, e o que os capítulos 9 e 10 dizem sobre este transtorno.
   - Ler os [Pontos de atenção](#pontos-de-atenção-já-identificados).

1. **História clínica.** Não leva referências.
   - **Tamanho e voz:** 2 a 3 parágrafos, em terceira pessoa.
   - **Dados do paciente:** os mesmos do script (nome, idade, ocupação, contexto).
   - **Conteúdo:** incluir as pistas listadas no "Guia oculto para o professor" (seção 6 do script), descritas como **comportamento e relato**, nunca como rótulo. O nome do transtorno e adjetivos diagnósticos (paranoide, narcisista, obsessivo, histriônico, borderline, esquizotípico, antissocial, dependente, evitativo) não podem aparecer.
   - **Diferenciais:** deixe material suficiente para discutir os diagnósticos diferenciais do script.
   - **Antes de seguir:** mostre a história ao autor.

2. **Bloco "Ver o diagnóstico".** Já está preenchido, com o nome do diagnóstico e o link para o script. Só altere se o autor pedir.

3. **Fontes para os outros quatro blocos.**
   - **Selecionar:** buscar no PubMed ou na Crossref e escolher **poucas fontes boas**: manuais, revisões, artigos clássicos.
   - **Conferir e registrar:** aplicar as regras 1 a 4 (conferência 1, PDF, resumo, conferência 2, entrada no `.bib`).
   - **Antes de escrever:** mostre ao autor a lista de fontes e o que cada uma sustenta.

4. **Escrever os quatro blocos:**
   - **História do diagnóstico na psiquiatria:** origem do conceito, autores, entrada e mudanças nos manuais (DSM e CID).
   - **Importância do diagnóstico hoje:** prevalência, impacto clínico e funcional, relevância para o tratamento. Deve ser coerente com os capítulos 9 e 10.
   - **O diagnóstico no DSM-5-TR e na CID-11:** responder se o diagnóstico ainda existe, sob que nome e com que código; qual a situação no Modelo Alternativo (Seção III) do DSM-5; e qual o perfil dimensional na CID-11.
   - **Críticas ao diagnóstico:** validade, confiabilidade, sobreposição com outros diagnósticos, vieses de gênero e culturais, estigma. Tratar só do que se aplica a este diagnóstico.

   Regras de forma:
   - **Dentro dos blocos:** só prosa (parágrafos, listas, negrito para conceitos-chave). Não use títulos (`#`) dentro dos blocos.
   - **Citações:** no formato Pandoc, `[@chave]` ou `@chave`. O ABNT é aplicado automaticamente.
   - **Limpeza:** ao preencher um bloco, apague o `*Em elaboração.*` e o comentário-guia dele.
   - **Extensão:** combine com o autor na primeira sessão e registre a decisão em [Decisões de estilo](#decisões-de-estilo).

5. **Fechar o caso.** Com os cinco blocos e a história prontos, remova o aviso "Página em elaboração" do topo.

6. **Verificar.**
   - `python3 code/validate_bib.py --no-doi`: zero erros.
   - `python3 code/deep_validate_bib.py`: as entradas novas precisam sair OK.
   - `rm -rf _book && quarto render --to html`: sem avisos, especialmente "citation … not found".
   - `python3 code/verificar_spoiler.py caso-x`: precisa dar OK.

7. **Registrar.** Atualize a tabela de [Progresso](#progresso) e acrescente uma entrada no [Diário das sessões](#diário-das-sessões) com:
   - o que foi feito;
   - as chaves adicionadas ao `.bib`;
   - os resumos criados;
   - as pendências.

8. **Commit.** Faça o commit com mensagem descritiva. O push só acontece com o OK do autor, porque publica o site.

## Regras anti-spoiler

- Nada **fora** dos blocos recolhidos pode nomear ou insinuar o diagnóstico. Isso inclui título, subtítulo, história, pergunta e os títulos dos blocos, que devem continuar neutros.
- Link para o script só **dentro** do bloco "Ver o diagnóstico", porque o script revela o diagnóstico.
- Os nomes dos arquivos de leitura (`caso-a` … `caso-i`) são neutros de propósito, para o endereço da página não entregar o diagnóstico. Não renomeie.
- Há duas pendências conhecidas, que ficam a decidir com o autor:
  - a busca do site indexa o conteúdo dos blocos recolhidos (`search: false` nas páginas de caso resolveria, ao custo de tirá-las da busca);
  - os endereços dos scripts no menu lateral contêm o diagnóstico e aparecem ao passar o mouse (renomear para `script-a` etc. resolveria).

## Pontos de atenção já identificados

Isto **não** é texto pronto para usar. São pontos a conferir na fonte e citar.

- **Esquizotípica (Caso B):** na CID-11 é o transtorno esquizotípico, 6A22, no espectro da esquizofrenia e fora dos transtornos de personalidade. O Cap. 8 já trata disso com fonte.
- **CID-11 em geral:** a CID-11 não tem tipos categoriais de transtorno de personalidade. Ela usa:
  - gravidade (6D10);
  - qualificadores de traço (6D11.0 a 6D11.4);
  - o qualificador de padrão borderline (6D11.5).
- **Códigos do DSM-5-TR:** são os códigos F da CID-10-MC. Os 301.x são da CID-9-MC e aparecem em edições anteriores. Conferir antes de afirmar.
- **Modelo Alternativo (Seção III) do DSM-5:** pelo que consta, mantém só seis tipos (antissocial, evitativa, borderline, narcisista, obsessivo-compulsiva e esquizotípica). Isso afeta os casos A, E e H (dependente, histriônica, paranoide). **Conferir na fonte antes de usar.**
- **Divergências entre o Cap. 8 e os scripts, a decidir com o autor:**
  - **Paranoide (Caso H):** a tabela do capítulo usa afetividade negativa + desapego, e o script usa afetividade negativa + dissocialidade.
  - **Dependente (Caso A):** a tabela do capítulo inclui desapego; vale conferir na literatura.

## Decisões de estilo

Registre aqui as decisões que o autor tomar nas sessões, como extensão de cada bloco, tom ou uso de exemplos.

- *(nenhuma ainda)*

## Progresso

| Caso | Paciente | Página | Script | Diagnóstico | História | 4 blocos | Status |
|---|---|---|---|---|---|---|---|
| A | Marina | `caso-a.qmd` | `dependente.qmd` | TP dependente | — | — | esqueleto |
| B | Otávio | `caso-b.qmd` | `esquizotipica.qmd` | TP esquizotípica | — | — | esqueleto |
| C | Helena | `caso-c.qmd` | `obsessivo.qmd` | TP obsessivo-compulsiva | — | — | esqueleto |
| D | Diogo | `caso-d.qmd` | `antissocial.qmd` | TP antissocial | — | — | esqueleto |
| E | Daniela | `caso-e.qmd` | `histrionica.qmd` | TP histriônica | — | — | esqueleto |
| F | Vivian | `caso-f.qmd` | `narcisista.qmd` | TP narcisista | — | — | esqueleto |
| G | Felipe | `caso-g.qmd` | `esquiva.qmd` | TP evitativa (esquiva) | — | — | esqueleto |
| H | Eurídice | `caso-h.qmd` | `paranoide.qmd` | TP paranoide | — | — | esqueleto |
| I | Pedro | `caso-i.qmd` | `borderline.qmd` | TP borderline | — | — | esqueleto |

Legenda: — = não iniciado · em andamento · pronto.

## Diário das sessões

- **2026-10-02 — Reestruturação.**
  - Os scripts foram para o Apêndice C, com os códigos CID-11 e DSM-5-TR corrigidos.
  - Foram criados os esqueletos `caso-a` … `caso-i`.
  - Foi criado `code/verificar_spoiler.py`.
  - Nenhum texto de caso foi escrito ainda.
