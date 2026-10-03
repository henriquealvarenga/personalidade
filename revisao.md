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
   - **Texto dos PDFs e EPUBs:** `python3 code/extrair_texto_pdfs.py` gera `references/texto/<mesmo nome>.txt`. Rode de novo sempre que entrar PDF ou EPUB novo. A pasta fica fora do git, como os PDFs.
     - Use para procurar em todas as referências de uma vez (`grep -ril "termo" references/texto/`) e para ler trechos longos.
     - Cada página começa com `=== p. N ===`, em que N é a página do arquivo PDF. O número impresso, que é o que vai para o resumo, costuma aparecer logo abaixo da marca ou no pé da página.
     - Páginas escaneadas começam com `[texto de OCR]` e têm erros de reconhecimento (ex.: "wha" por "who"). Citação literal tirada delas é conferida na imagem do PDF.
     - Tabelas, quadros de destaque e páginas em duas colunas saem embaralhados. Para ler uma tabela: `pdftotext -layout -f N -l N "references/PDF/<arquivo>.pdf" -`.
     - **EPUB não tem páginas.** O texto vem dividido em `=== seção N: título ===`, na ordem de leitura. Quando o EPUB reproduz a paginação impressa, ela aparece como `[p. N]` no meio do texto (hoje: Mischel 1968 e Woolf 1925), e é esse número que vai para o resumo. Sem `[p. N]`, a citação com página exige uma edição paginada; o cabeçalho do `.txt` avisa.
     - Os EPUBs do Internet Archive (Szasz 1961, Wittgenstein 1953, James 1890) são OCR automático, uma seção por página escaneada, com erros que o script não tem como corrigir: as imagens não vêm no EPUB. O Szasz é o pior, com cerca de 1 página em 6 com trechos ilegíveis.
     - Antes de anotar a página no resumo, confirme no PDF ou no EPUB.
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
   - **Citações:** no formato Pandoc, `[@chave]` ou `@chave`. O estilo de citação (Vancouver, numérico, definido no `_quarto.yml`) é aplicado automaticamente.
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
- **Lista de referências no fim da página:** fica visível, fora dos blocos recolhidos, e pode nomear o diagnóstico nos títulos das obras (em inglês, por exemplo). Decisão do autor em 2026-10-03: aceitável. O `verificar_spoiler.py` não olha essa lista (`div#refs`; a exclusão foi de fato implementada em 2026-10-03, quando os casos B–I a fizeram falhar).
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
- **Modelo Alternativo (Seção III) do DSM-5-TR:** conferido em `apa_dsm5tr_2022`. Deriva só seis transtornos específicos — antissocial, evitativo, borderline, narcisista, obsessivo-compulsivo e esquizotípico (p. 881); paranoide, esquizoide, histriônico e dependente são representados como "transtorno de personalidade com traços especificados" (PD-TS) (p. 891). Afeta os casos A (feito), E e H. Ver o resumo.
- **Tabela `@tbl-dsm-cid11` do Cap. 8:** revista em 2026-10-03 pelo autor e corrigida com `simon_crosswalk_2023`, que agora é a fonte de todos os perfis de traço.
  - **Dependente (Caso A):** o desapego estava errado (a linha era cópia da evitativa); agora afetividade negativa, com desinibição secundária.
  - **Paranoide (Caso H):** agora afetividade negativa + dissocialidade, com desapego em alguns estudos — coerente com o script. `bach_categorical_2018` (Tabela 6, p. 8) dá os três domínios.
  - Histriônica, evitativa, obsessivo-compulsiva, narcisista e borderline foram completadas; ver o resumo de `simon_crosswalk_2023`.
  - Ao escrever os blocos dos casos C, E, F, G, H e I, usar o perfil da tabela e conferir no resumo.
- **Cap. 9, tabela `@tbl-prevalencia`:** corrigida em 2026-10-03 por decisão do autor. A coluna "População geral" não batia com `torgersen_prevalence_2001`; agora traz os valores ponderados da Tabela 2 do artigo (p. 593), e o asterisco "mais comum nos homens" passou do narcisista para o antissocial e o obsessivo-compulsivo. A coluna clínica (`zimmerman_prevalence_2005`) confere nos dez valores.

## Decisões de estilo

Registre aqui as decisões que o autor tomar nas sessões, como extensão de cada bloco, tom ou uso de exemplos.

- **Extensão dos blocos:** três parágrafos curtos por bloco — decisão do autor (2026-10-03), a partir do Caso A.
- **Ligação com o caso:** cada bloco termina, quando cabe, voltando ao paciente (no Caso A: critérios do DSM-5-TR que Marina preenche, classificação provável na CID-11, a recusa de promoção que não é desapego, a pergunta sobre norma cultural e prejuízo).
- **Citações:** o estilo Vancouver não mostra a página no texto; manter o localizador (`[@chave, p. X]`) mesmo assim, porque fica no código e nos resumos. Disney (2013) é citado sem página (o PDF local é o manuscrito aceito, com paginação própria).

## Progresso

| Caso | Paciente | Página | Script | Diagnóstico | História | 4 blocos | Status |
|---|---|---|---|---|---|---|---|
| A | Marina | `caso-a.qmd` | `dependente.qmd` | TP dependente | pronto | pronto | pronto |
| B | Otávio | `caso-b.qmd` | `esquizotipica.qmd` | TP esquizotípica | pronto* | pronto* | aguarda revisão do autor |
| C | Helena | `caso-c.qmd` | `obsessivo.qmd` | TP obsessivo-compulsiva | pronto* | pronto* | aguarda revisão do autor |
| D | Diogo | `caso-d.qmd` | `antissocial.qmd` | TP antissocial | pronto* | pronto* | aguarda revisão do autor |
| E | Daniela | `caso-e.qmd` | `histrionica.qmd` | TP histriônica | pronto* | pronto* | aguarda revisão do autor |
| F | Vivian | `caso-f.qmd` | `narcisista.qmd` | TP narcisista | pronto* | pronto* | aguarda revisão do autor |
| G | Felipe | `caso-g.qmd` | `esquiva.qmd` | TP evitativa (esquiva) | pronto* | pronto* | aguarda revisão do autor |
| H | Eurídice | `caso-h.qmd` | `paranoide.qmd` | TP paranoide | pronto* | pronto* | aguarda revisão do autor |
| I | Pedro | `caso-i.qmd` | `borderline.qmd` | TP borderline | pronto* | pronto* | aguarda revisão do autor |

Legenda: — = não iniciado · em andamento · pronto.

\* Escritos em 2026-10-03 por subagentes em paralelo, sem as paradas do roteiro (história e lista de fontes mostradas ao autor antes de seguir). O autor revisa os oito antes do push; ver o diário.

## Diário das sessões

- **2026-10-02 — Reestruturação.**
  - Os scripts foram para o Apêndice C, com os códigos CID-11 e DSM-5-TR corrigidos.
  - Foram criados os esqueletos `caso-a` … `caso-i`.
  - Foi criado `code/verificar_spoiler.py`.
  - Nenhum texto de caso foi escrito ainda.
- **2026-10-03 — Caso A (Marina), 1ª sessão.**
  - **História clínica:** escrita e reduzida pelo autor. Verificador de spoiler: OK.
  - **Desapego (Cap. 8):** a tabela `@tbl-dsm-cid11` dava ao transtorno dependente afetividade negativa + desapego (cópia da linha da evitativa). Nenhuma fonte sustenta isso; a linha agora diz afetividade negativa (predominante) + desinibição (secundária), com `simon_crosswalk_2023`. Apoios: CDDR da OMS, pp. 560–561 (dependência é manifestação da afetividade negativa); `bach_categorical_2018`, Tabs. 4–6; `bach_icd11_personality_2018`, Tab. 8; `krueger_initial_2012`, Tab. 3; `gore_dependency_2013`, pp. 167–170.
  - **Chaves novas no `.bib`:** `bach_categorical_2018`, `gore_dependency_2013`, `simon_crosswalk_2023`, `disney_dependent_2013`, `bornstein_reconceptualizing_2011`, `bornstein_costs_2012`, `apa_dsm5tr_2022`. Atualizado o `note` de `bach_icd11_personality_2018`. Backups locais: `references.bib.bak-20261003_133634_pre_caso_a` e `…_135002_pre_caso_a_lote2`.
  - **Resumos criados** (pasta nova `references/resumos/`): `bach_categorical_2018`, `bach_icd11_personality_2018`, `bach_icd11_european_2022`, `gore_dependency_2013`, `krueger_initial_2012`, `simon_crosswalk_2023`, `who_cddr_icd11_2024`.
  - **PDFs renomeados** para o padrão da pasta: Bach2018 (ANZJP), Simon2023, Disney2013, Bornstein2011, Bornstein2012, APA2022 (DSM-5-TR, edição em inglês).
  - **Pendências:**
    - escrever os quatro blocos do Caso A; antes, ler e resumir Disney 2013 (manuscrito aceito, paginação própria), Bornstein 2011, Bornstein 2012 e o capítulo do DSM-5-TR (incluindo a Seção III);
    - decidir a extensão dos blocos (sugestão: 2 a 3 parágrafos cada) e registrar em "Decisões de estilo";
    - Lambrecht, Simon e Bach (2023), *Personal Disord* 15(2):122–127, doi:10.1037/per0000646, o único estudo com traços avaliados pelo clínico, não foi encontrado; é opcional;
    - Cap. 8, linha 17: diz que a CID-10 está "vigente desde 1992"; 1992 é o ano do livro de descrições clínicas (`who_icd10_1992`), que não traz a data de entrada em vigor. Falta fonte para conferir.
- **2026-10-03 — Correções no Cap. 8 (pedidas pelo autor).**
  - **Linha 42:** a CID-11 foi aprovada pela Assembleia Mundial da Saúde em maio de 2019 e entrou em vigor em 1º de janeiro de 2022 (antes dizia "adotada em janeiro de 2022"); abandonou os **oito** tipos da CID-10 (antes, "os dez [...] do sistema anterior", com nomes do DSM). Fontes: `who_cddr_icd11_2024` (p. 1) e `who_icd10_1992` (pp. 201–206), esta agora conferida e fora de pending-verification. A mesma data foi corrigida no callout da linha 95.
  - **Tabela `@tbl-dsm-cid11`:** todas as linhas de traço revistas com `simon_crosswalk_2023` (citada no parágrafo que apresenta a tabela); borderline com o código F60.31 da CID-10.
  - **CID-11 no Brasil (callout da linha 95):** antes dizia "conclusão oficial prevista para 1º de janeiro de 2027, sendo 2026 um ano de transição e capacitação"; a Nota Técnica nº 91/2024 do Ministério da Saúde prevê o **início** do uso nos sistemas de vigilância em janeiro de 2027, com integração plena até 2027 ou 2028, e a CID-10 versão 2019 em uso desde 2025. Buscas em 2026-10-03 não acharam mudança posterior.
  - **Chaves novas no `.bib`:** `brasil_notatecnica91_2024` (PDF guardado em `references/PDF/`), `cfm_cronograma_cid11_2025`. Corrigido o título de `prata_implementation_2025` para o original em português (e o nome do PDF). Backup local: `references.bib.bak-20261003_140135_pre_cid11_brasil`.
  - **Resumos criados:** `brasil_notatecnica91_2024`, `prata_implementation_2025`, `who_icd10_1992`; atualizados `who_cddr_icd11_2024` e `simon_crosswalk_2023`.
  - **Estilo de citação:** o autor trocou para Vancouver; atualizadas as menções no `_quarto.yml` e neste arquivo.
  - **Data de publicação do livro:** o `_quarto.yml` usava `date: today` desde a 2ª edição, e cada render trocava a data exibida. Fixada, por decisão do autor, em `2026-10-03` (exibida como "outubro de 2026"). Não voltar a usar `today`.
- **2026-10-03 — Caso A (Marina), 2ª sessão: caso concluído.**
  - **Quatro blocos escritos** (três parágrafos cada) e aviso "Página em elaboração" retirado. Corrigido "MArina" na história.
  - **Fontes usadas nos blocos:** `maass_personality_disorders_2019`, `disney_dependent_2013`, `who_icd10_1992`, `bornstein_reconceptualizing_2011`, `bornstein_costs_2012`, `apa_dsm5tr_2022`, `volkert_prevalence_2018`, `zimmerman_prevalence_2005`, `who_cddr_icd11_2024`, `simon_crosswalk_2023`, `gore_dependency_2013`. Disney, os dois Bornstein e o DSM-5-TR foram lidos com apoio de subagentes; os trechos usados foram conferidos no texto.
  - **Resumos criados:** `apa_dsm5tr_2022`, `disney_dependent_2013`, `bornstein_reconceptualizing_2011`, `bornstein_costs_2012`, `maass_personality_disorders_2019`, `volkert_prevalence_2018`, `zimmerman_prevalence_2005`.
  - **`.bib`:** corrigido o segundo autor de `volkert_prevalence_2018` (era "Gablónski, Theresa-Maria"; é Thorsten-Christian Gablonski) e o campo `edition` de `apa_dsm5tr_2022`. Backup local: `references.bib.bak-*_pre_volkert`.
  - **Verificação:** `validate_bib` com zero erros; render sem avisos; `verificar_spoiler.py caso-a` OK.
  - **Pendências para o autor:**
    - confirmar a extensão dos blocos (ver "Decisões de estilo");
    - Cap. 9: coluna de Torgersen na tabela de prevalência (ver "Pontos de atenção");
    - classificação de Marina na CID-11 ("provavelmente leve, com afetividade negativa proeminente") é inferência a partir da CDDR, pp. 556 e 560 — conferir se concorda;
    - o estilo/idioma de citação imprime "3º ed." nos livros (deveria ser "3ª ed.");
    - os textos extraídos dos PDFs ficam só na pasta temporária da sessão; o autor pode querer guardá-los numa pasta local fora do git.
- **2026-10-03 — Pontos em aberto resolvidos com o autor.**
  - **Caso A:** devolvida à história a frase em que Marina se cala quando discordam dela (critério 3); o bloco do DSM-5-TR passa a "pelo menos seis" critérios. Classificação na CID-11 (leve, com afetividade negativa proeminente) confirmada pelo autor. No bloco de importância, acrescentada a prevalência de Oslo (1,5%; 2,0% em mulheres e 0,9% em homens) para coerência com o Cap. 9.
  - **Extensão dos blocos:** três parágrafos, decisão do autor (ver "Decisões de estilo").
  - **Cap. 9:** tabela de prevalência corrigida (ver "Pontos de atenção"); a linha 5 dizia que a metanálise de `volkert_prevalence_2018` reuniu "27 estudos" — são dez estudos, publicados em 27 artigos.
  - **Estilo de citação:** `vancouver.csl` ganhou um bloco para o português com o ordinal feminino; as edições saem "3ª ed." (antes "3º ed.").
  - **README:** a 1ª edição passa a ser descrita com formato, ISBN e coleção (conferidos no manuscrito e no registro do ISBN).
  - **Resumo criado:** `torgersen_prevalence_2001`.
- **2026-10-03 — Referências no fim das páginas (livro todo).**
  - O título "Referências" aparecia no fim das páginas sem a lista: em livros com `references.qmd`, o Quarto gera a lista de cada capítulo com `display: none`. Afetava as 16 páginas com citações.
  - Correção: regra em `theme-editorial.scss` que mostra a lista; script `_includes/referencias-locais.html` (incluído no `_quarto.yml`) que aponta cada citação para a lista da própria página, cuja numeração Vancouver bate com a do texto — antes, o "(5)" levava à página geral, onde a obra tem outro número. O script também atualiza o `data-original-href`, senão um script do Quarto desfaz a troca.
  - Testado no Chrome em modo headless: lista visível em todas as páginas; no Caso A, 40 de 40 citações apontam para a própria página; no Cap. 8, 23 de 23.
  - Nos casos, a lista fica visível fora dos blocos recolhidos; o autor aceitou (ver "Regras anti-spoiler").
- **2026-10-03 — Casos B a I, escritos em paralelo (aguardam revisão do autor).**
  - **Como foi feito:** a pedido do autor, oito subagentes escreveram ao mesmo tempo a história e os quatro blocos de um caso cada, com o Caso A como modelo. Cada um editou só o próprio `caso-x.qmd`; as entradas do `.bib` e os resumos ficaram numa área temporária e foram fundidos depois, com deduplicação. As duas paradas do roteiro (mostrar a história e a lista de fontes antes de seguir) foram adiadas: **o autor revisa os oito casos antes do push.** O aviso "Página em elaboração" saiu dos oito.
  - **Extensão:** história de 650 a 745 palavras (Caso A: 580); blocos de 360 a 690 palavras (Caso A: 320 a 385), sempre em três parágrafos. Os blocos de F e I são os mais longos. A decisão era "três parágrafos curtos": o autor decide se encurta.
  - **Chaves novas no `.bib` (8º lote, 25):** `apa_dsm5_br_2014`, `bakkevig_histrionic_2010`, `campbell_narcissistic_2013`, `dolansewell_cooccurrence_2001`, `edmundson_schizotypal_2013`, `fineberg_anankastic_2014`, `ford_sexbias_1989`, `gabbard_narcissism_2016`, `gecaite_anankastia_2021`, `gibbon_psychological_2020`, `jakobsen_antipsychotic_2017`, `kendler_diagnostic_1985`, `khalifa_pharmacological_2020`, `lampe_avoidant_2018`, `lee_mistrustful_2017`, `livesley_conceptual_2001`, `nielsen_psychotherapy_2023`, `novais_historical_2015`, `pinto_ocpd_2022`, `sansone_gender_2011`, `spitzer_crossing_1979`, `triebwasser_paranoid_2013`, `trull_borderline_2013`, `weinberg_narcissistic_2022`, `widiger_official_2001`. Sete foram conferidas **só pelo abstract** (o texto não vai além dele): Bakkevig, Ford, Jakobsen, Kendler, Nielsen, Spitzer e Triebwasser; Gibbon e Khalifa, só pelo resumo da revisão Cochrane. Backup local: `references.bib.bak-20261003_152532_pre_casos_b_i`.
  - **Resumos criados (33):** `apa_dsm5_br_2014`, `bakkevig_histrionic_2010`, `berrios_european_1993`, `campbell_narcissistic_2013`, `dolansewell_cooccurrence_2001`, `edmundson_schizotypal_2013`, `fineberg_anankastic_2014`, `ford_sexbias_1989`, `gabbard_narcissism_2016`, `gecaite_anankastia_2021`, `gibbon_psychological_2020`, `gunderson_ontogeny_2009`, `hadjipavlou_promising_2010`, `jakobsen_antipsychotic_2017`, `kendler_diagnostic_1985`, `khalifa_pharmacological_2020`, `lampe_avoidant_2018`, `lee_mistrustful_2017`, `livesley_conceptual_2001`, `nielsen_psychotherapy_2023`, `novais_historical_2015`, `oyebode_sims_sintomas_2018`, `paris_reluctant_2007`, `pinto_ocpd_2022`, `sansone_gender_2011`, `sheehan_stigma_2016`, `spitzer_crossing_1979`, `storebo_psychological_2020`, `triebwasser_paranoid_2013`, `trull_borderline_2013`, `weinberg_narcissistic_2022`, `widiger_official_2001`, `zimmerman_differences_1999`. Seis foram escritos por dois a quatro casos e fundidos. **Ampliados (12):** `apa_dsm5tr_2022`, `who_cddr_icd11_2024`, `who_icd10_1992`, `maass_personality_disorders_2019`, `simon_crosswalk_2023`, `torgersen_prevalence_2001`, `zimmerman_prevalence_2005`, `volkert_prevalence_2018`, `bornstein_reconceptualizing_2011`, `bach_categorical_2018`, `bach_icd11_personality_2018`, `disney_dependent_2013` (no DSM-5-TR, na CDDR e no Maass, os trechos estão agrupados por transtorno). Divergências entre fontes ficaram marcadas nos resumos com "(divergência: …)", como o ano de Schneider no Maass (1923, 1932 e 1950 em capítulos diferentes; 1923 é a 1ª edição, 1950 a 9ª). Na fusão, o Caso G citava Bornstein p. 235 para a lista dos transtornos mantidos, que está na p. 236: corrigido.
  - **Entradas existentes atualizadas:** `note` de `apa_dsm5tr_2022`, `disney_dependent_2013` e `bornstein_reconceptualizing_2011` (tirado o "Conteúdo ainda não conferido"), `berrios_european_1993` e `sheehan_stigma_2016` (conteúdo conferido); `storebo_psychological_2020` passou a `verified-doi`, com "J{\o}rgensen" corrigido; `who_icd10_1992` com pp. 201–207.
  - **PDFs baixados a pedido do autor** (acesso aberto, das editoras; PMC, Europe PMC, Wiley, Cochrane, APA Publishing e Springer bloqueiam download automático): `Fineberg2014` (SciELO), `Gecaite-Stonciene2021` e `Novais2015` (Frontiers), `Lampe2018` (Dove). Texto extraído. As citações dessas quatro obras continuam sem página (foram lidas em HTML); dá para pôr a página agora.
  - **Erros de página no Caso A, achados pelos agentes e conferidos no PDF:** Volkert, 0,78% na p. 712 (era p. 711); CID-10, inclusões do F60.7 nas pp. 206–207 (era p. 206). Corrigidos no caso e nos resumos; no resumo da CID-10, "pelo menos três traços" está na p. 202 (era p. 201).
  - **Repetição:** o Caso F copiava duas frases do Caso A (proposta de eliminação no DSM-5); reescritas.
  - **`verificar_spoiler.py`:** passou a ignorar a lista de referências (`div#refs`), como a decisão do autor já previa; antes falhava em seis casos por títulos em inglês da lista. Verificação final: `validate_bib` com zero erros; `deep_validate_bib` sem FAIL (os WARN das entradas novas são ano ausente na Crossref para capítulos de livro e o "ø" de Storebø); render sem avisos; spoiler OK nos nove casos.
  - **Para o autor decidir, caso a caso:**
    - **Todos:** a classificação provável na CID-11 (gravidade + qualificadores) é inferência dos agentes a partir da CDDR — B: só 6A22, e só se houver prejuízo; C: leve + anancastia; D: moderado + dissocialidade + desinibição; E: leve + afetividade negativa + desinibição (dissocialidade em dúvida); F: moderado + dissocialidade (ou leve); G: leve + afetividade negativa + desapego; H: moderado + afetividade negativa (dissocialidade se a hostilidade se voltar para fora); I: moderado + afetividade negativa + desinibição + padrão borderline (6D11.5).
    - **Dados acrescentados à história, que não estão no script:** B (nega drogas; nunca teve crise, internação ou tratamento); D ("brigava com frequência na escola"; nega tristeza persistente, medo de ficar só e autolesão); E (achados negativos de humor, sono, autolesão; "nega ideias de morte"); F (sem brigas, mentiras ou problemas com a lei; sem mudança de sono, energia ou ritmo do pensamento); H (admite que um pacote "talvez" tenha se extraviado; nega vozes; cuida sozinha da casa e das contas); I ("da infância, nesta consulta, não conta mais nada"; "nada soa teatral").
    - **Divergências com os capítulos (não alterados):** Cap. 8, quadro "E a esquizotípica?" diz que ela "nunca esteve" entre os TP da CID, mas a CID-10 (p. 201) diz que os transtornos esquizotípicos "foram classificados antes com os transtornos de personalidade" (comentário `CONFERIR` no Caso B); Cap. 8 chama o 6D11.4 de "Anancástico", a CDDR de "anancastia"; Cap. 8 diz que o estigma do borderline é "muito maior", Sheehan diz "entre os mais estigmatizados"; Cap. 8, tabela: a CDDR (p. 563) inclui a dissocialidade entre os domínios que se sobrepõem ao padrão borderline; Cap. 9 dá 20% de borderline em "hospitais clínicos" com `hales_textbook_2014` (pending), o DSM-5-TR (p. 755) dá cerca de 20% em internação psiquiátrica; Cap. 10 atribui a Storebø 2020 a DBT como "padrão-ouro pelas diretrizes", o que a revisão Cochrane não diz; Cap. 10 diz que a TFP tem "evidência em transtornos narcisistas graves", Weinberg 2022 diz que não há ensaio randomizado (comentário `CONFERIR` no Caso F); Cap. 10 diz que antipsicóticos "podem ser úteis" no grupo A, Lee 2017 é mais cético (`jakobsen_antipsychotic_2017` pode dar fonte à frase).
    - **Scripts com inconsistências (não alterados):** B (a ficha diz que Marta é a irmã mais velha; no diálogo, Otávio é o mais velho); E (a ficha dá afetividade negativa + dissocialidade, sem a desinibição da tabela do Cap. 8; o guia fala em namoro de "duas semanas e meia", o diálogo em dois meses e meio); H (a pista 7 liga o critério 7 do DSM à herança, mas o critério trata da fidelidade do cônjuge; o caso dá os critérios 1 a 6).
    - **Outros:** F tem um `FALTA REFERÊNCIA` (Näcke, 1899). Datas divergentes deixadas de fora ou atribuídas: Schneider (1923 em Berrios e Lee; 1932 ou 1950 em Maass), CID-8 (1965 ou 1966), Kretschmer sem ano. G: a ressalva de que o desapego da CDDR inclui não gostar de interação social é leitura do agente, não crítica tirada de fonte. I: a frase de que se relacionar com homens e mulheres não conta como critério (DSM-5-TR, p. 755) — conferir o tom. B: os nomes em português das facetas da Seção III não foram conferidos na edição brasileira (o PDF local só tem a Seção II).
    - **PDFs que valeria ter** (para pôr páginas ou passar do abstract ao texto): Nielsen 2023 (Wiley, aberto), Gabbard 2016, Gibbon 2020, Khalifa 2020, Lee 2017, Pinto 2022, Sansone 2011, Weinberg 2022 (todos no PMC), Bakkevig 2010, Ford 1989, Jakobsen 2017, Kendler 1985, Spitzer 1979, Triebwasser 2013 (acesso institucional).
- **2026-10-03 — Inconsistências dos casos B a I resolvidas (pedido do autor).**
  - **Cap. 8:** quadro "E a esquizotípica?" reescrito — saiu o "nunca esteve entre os transtornos de personalidade da CID"; agora segue a CID-10 (p. 201: o transtorno esquizotípico "foi classificado antes com os transtornos de personalidade" e passou ao F20–F29), com citações para a CID-10, a CDDR (p. 161) e o DSM-5-TR (pp. 103–104). Bach 2018 (p. 8) diz o contrário ("nunca classificados como tais na CID"); prevaleceu a fonte primária. Domínio 6D11.4 passou de "Anancástico" a "Anancastia" nas tabelas (também no Cap. 6, que dizia ainda "afeto negativo", agora "afetividade negativa", e na ficha do Script C). Estigma do borderline: de "muito maior do que os outros" para "um dos mais estigmatizados e o mais estudado quanto ao estigma" (Sheehan, p. 3). Tabela `@tbl-dsm-cid11`, linha do borderline: acrescentada a dissocialidade citada pela CDDR (p. 563).
  - **Cap. 9:** os 20% de borderline em "hospitais clínicos" (`hales_textbook_2014`, pending, sem PDF) viraram 20% em internação psiquiátrica, com o DSM-5-TR (p. 755). Hales deixou de ser citado no livro.
  - **Cap. 10:** antipsicóticos no grupo A — saiu "podem ser úteis"; agora Jakobsen 2017 (só quatro ensaios randomizados no esquizotípico) e Lee 2017 (nenhum ensaio nem medicamento aprovado no paranoide). DBT — saiu "padrão-ouro pelas principais diretrizes (NICE, APA)" e "evidência crescente em outros transtornos de cluster B", sem fonte; agora o que Storebø 2020 diz (um terço de 75 ensaios; superior ao tratamento usual com evidência de baixa qualidade). TFP — saiu "evidência em transtornos narcisistas graves"; agora Weinberg 2022 (nenhuma psicoterapia testada em ensaio randomizado no narcisista). As outras afirmações sem fonte da seção (MBT, terapia do esquema, "transformou o prognóstico do TPB") continuam como estavam, sob o aviso "[VERIFICAR]" do capítulo.
  - **Scripts:** B — a ficha dizia "irmã mais velha", mas no diálogo Otávio é o mais velho; corrigida a ficha, e a história do Caso B diz agora que Marta é mais nova. E — ficha com o perfil CID-11 da tabela do Cap. 8 (dissocialidade, desinibição e afetividade negativa, associações fracas a moderadas); guia com o namoro de "seis encontros em dois meses e meio", como no diálogo. H — a herança passou para a pista 1 (suspeita de ser enganada); a pista 7 agora é a fidelidade do cônjuge, critério que o roteiro não explora (o marido "tinha mentido sobre uma coisa séria").
  - **Caso F:** resolvido o `FALTA REFERÊNCIA` — Näcke cunhou o termo em 1899 e Freud, em 1914, descartou a definição dele, com `rees_narcissists_2022` (Crossref e PubMed; texto integral lido no PMC, citado sem página). Chave nova no `.bib` (9º lote); resumo criado. Backup local: `references.bib.bak-*_pre_rees`.
  - **Comentários `CONFERIR` retirados** dos Casos B e F. Nenhum `FALTA REFERÊNCIA` ou `CONFERIR` restante nos casos.
  - **Verificação:** `validate_bib` com zero erros; render sem avisos; spoiler OK nos nove casos.
  - **PDF a mais para o autor baixar:** `Rees2022 - We other narcissists - self-love in Freud and culture.pdf` (<https://doi.org/10.1080/0950236X.2020.1839956>, acesso aberto, CC BY).
- **2026-10-03 — PDFs das referências dos casos B a I conferidos.**
  - **PDFs postos pelo autor** (15, todos os pedidos; renomeados para o padrão da pasta e com texto extraído): Rees 2022, Kendler 1985, Spitzer 1979, Jakobsen 2017, Nielsen 2023, Sansone 2011, Gibbon 2020, Khalifa 2020, Bakkevig 2010, Ford 1989, Triebwasser 2013, Lee 2017, Gabbard 2016, Weinberg 2022, Pinto 2022. Metadados conferidos na primeira página de cada um contra o `.bib`; completados os prenomes em `spitzer_crossing_1979` (Jean Endicott, Miriam Gibbon) e `kendler_diagnostic_1985` (Kenneth S.). Backup local: `references.bib.bak-*_pre_pdfs_casos`.
  - **Conferência 2 no PDF**, com subagentes por grupo de casos, das 15 obras e também das quatro baixadas antes (Fineberg 2014, Gecaite-Stonciene 2021, Lampe 2018, Novais 2015). As sete que antes só tinham sido conferidas pelo abstract (e as duas Cochrane, só pelo resumo da revisão) agora estão conferidas no texto completo; nenhuma entrada do `.bib` diz mais "conferido só no abstract".
  - **Páginas:** todas as citações dessas 19 obras têm página impressa, menos `lee_mistrustful_2017` (PDF é o manuscrito do autor, paginação própria) e `jakobsen_antipsychotic_2017` (PDF é a versão on-line antecipada, pp. 1–9), que seguem sem página, com as páginas do PDF no resumo. Fineberg é citado com a paginação do suplemento (`S41` etc.; `pages = {S40--S50}` no `.bib`); Novais e Gecaite, artigos de numeração eletrônica, com a página do PDF do artigo.
  - **Frases corrigidas para ficar fiéis à fonte:** Caso C — "o DSM-III incluiu" (não "acentuou") a constrição afetiva (Fineberg); evidência dos ISRS "um pequeno ensaio randomizado com fluvoxamina e dados de ensaios feitos em outros transtornos" (Pinto); Freud e Janet viam os traços como precursores "da neurose obsessiva" (Pinto, p. 394). Caso E — 354 psicólogos avaliaram "histórias clínicas, ou trechos delas" (Ford, p. 302: só 266 receberam as histórias). Caso F — o termo é "na maioria das vezes" (não "quase sempre") pejorativo (Gabbard); "é importante" (não "o primeiro passo é") transformar a motivação de ocasião (Weinberg, p. 374). Caso G — "casamento ou união estável" (Lampe: *married or cohabiting*); "provavelmente" maior chance de ideação e tentativas de suicídio (Lampe, p. 57: *is likely to be associated*). Caso H — essas pessoas "relutam em se oferecer" (não "raramente se oferecem") para estudos (Lee). Cap. 10 — o "só quatro ensaios" de Jakobsen vale para os duplo-cegos controlados com placebo em pacientes com diagnóstico bem definido, entre 16 estudos; frase corrigida. Weinberg ganhou página no Cap. 10 (p. 372).
  - **Verificação:** `validate_bib` com zero erros; render sem avisos; spoiler OK nos nove casos.
- **2026-10-03 — Versão final de Lee 2017.** O autor pôs a versão final da revista (Springer, pp. 151–165) no lugar do manuscrito, que foi apagado (e o `.txt` dele). As 12 citações no Caso H e a do Cap. 10 ganharam as páginas da revista, conferidas trecho a trecho; resumo e `note` atualizados. O "novo" PDF de Jakobsen 2017 era idêntico ao que já estava (mesmo arquivo, versão on-line antecipada, pp. 1–9) e foi apagado; a obra segue citada sem página (Caso B e Cap. 10).
