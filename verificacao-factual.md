# Verificação factual do livro

Guia para as sessões de auditoria de erros de citação, de fato e de interpretação em todo o texto publicado. **Leia este arquivo inteiro antes de começar** e, ao terminar, atualize [Progresso](#progresso) e [Diário das sessões](#diário-das-sessões).

Esta verificação é a **primeira etapa** antes de implementar qualquer tema novo da pauta da 2ª edição (ver [Decisões já tomadas](#decisões-já-tomadas-na-pauta)).

**Atenção:** um push na `main` publica o site. Nunca faça push sem o OK do autor.

## Objetivo

Achar, registrar e, com a decisão do autor, corrigir:

| Categoria | Exemplo |
|---|---|
| **C1. Citação que não sustenta a frase** | a fonte não diz aquilo, ou diz o contrário |
| **C2. Página errada ou ausente** | onde o padrão do livro pede página |
| **C3. Fato errado** | número, data, nome, código CID/DSM, mesmo sem citação |
| **C4. Interpretação forçada** | estudo sobre medo condicionado aplicado à memória autobiográfica |
| **C5. Afirmação sem fonte** | frase factual que precisa de citação e não tem |
| **C6. Inconsistência interna** | termos, traduções ou contagens que divergem entre capítulos |
| **C7. Problema no `.bib`** | metadados errados, autor faltando, `pending-verification` |

Gravidade: **alta** (inverte o sentido da fonte ou erra um fato clínico), **média** (impreciso, exagerado, sem fonte), **baixa** (forma, consistência).

## Escopo e ordem dos lotes

Em 2026-10-04 havia **681 citações** em 26 arquivos `.qmd`, e **192 entradas** no `.bib`, 26 delas marcadas `pending-verification`.

| Lote | Arquivos | Citações | Observação |
|---|---|---|---|
| 1 | Partes I e II (caps. 1–10) | 107 | onde a varredura de 2026-10-03 achou mais problemas |
| 2 | Cap. 11, Parte IV (esqueletos dos caps. 12–14), Atividade 2 | 40 | o autor quer "repensar o cap. 11" |
| 3 | Apêndices I e II, `creditos.qmd` | 49 | ensaio e crítica: o risco maior é C4 |
| 4 | Casos A a I (`atividade-1-casos/`) | 495 | já passaram pela conferência dupla de [revisao.md](revisao.md) em 2026-10-03; combinar com o autor se a auditoria será completa ou por amostragem. Para mexer nos casos, ler [revisao.md](revisao.md) antes. |
| 5 | `references/references.bib` | — | as 26 entradas `pending-verification` |

Para recontar: `for f in $(git ls-files '*.qmd' | grep -v _extras); do echo "$(grep -o '@[a-z][a-z0-9_]*' "$f" | wc -l) $f"; done | sort -rn`

## Método

As regras de [CLAUDE.md](CLAUDE.md) e de [revisao.md](revisao.md) (seção "Regras sobre referências") valem aqui: nunca inventar referência; conferir primeiro o resumo (`references/resumos/`), depois o texto integral (`references/texto/`), e só então o PDF, para confirmar página e trecho.

**Fase 1 — levantamento (só leitura, nenhum `.qmd` editado).**
1. Para cada arquivo do lote, listar cada frase com citação e cada afirmação factual sem citação.
2. Conferir cada uma na fonte e registrar na tabela do [Registro](#registro) só o que tiver problema; o que estiver certo entra apenas na contagem do [Progresso](#progresso).
3. Pode-se usar agentes em paralelo (um por arquivo ou grupo pequeno de arquivos), sempre só leitura e com este arquivo como instrução. **Agentes erram:** antes de levar um item ao autor, o coordenador da sessão confere pessoalmente no texto da fonte cada item classificado como C1, C3 ou C4.

**Fase 2 — decisão do autor.** Apresentar os itens do lote ao autor. Ele decide item a item: corrigir, manter ou reescrever. Decisões clínicas e de interpretação são dele.

**Fase 3 — correção.**
- Corrigir só o que o autor aprovou.
- Se a correção exigir referência nova, seguir as regras de referências (conferência dupla), dar entrada no `.bib` e criar o resumo em `references/resumos/`.
- Ao fim de cada lote, rodar `python3 code/validate_bib.py --no-doi` e `rm -rf _book && quarto render --to html` (sem avisos).
- Commit por lote ou por capítulo, com mensagem descritiva. Push só com OK.

## Registro

Situação: **conferido** = conferido no texto da fonte pelo coordenador; **a conferir** = apontado por agente e ainda não reconferido; **aprovado**, **corrigido** ou **mantido** = depois da decisão do autor.

### Ponto de partida: itens achados na varredura de temas (2026-10-03)

O autor aceitou na pauta (2026-10-04) as correções que deram origem a estes itens, exceto V-20, que ainda precisa da decisão dele. **Cada item precisa ser confirmado antes de corrigir.** As páginas vêm dos agentes, lidas nos `.txt`; confira no PDF.

| ID | Arquivo:linha | Problema | O que a fonte diz | Cat. | Grav. | Situação |
|---|---|---|---|---|---|---|
| V-01 | `05-personalidade-e-saude.qmd:7` | Kotov 2010 citado como prova de que o traço é "preditor de incidência ao longo do tempo" | "estimates of concurrent associations rather than causal effects", porque os dados são quase todos transversais (Kotov 2010, p. 803) | C1 | alta | conferido |
| V-02 | `02-construcao-da-personalidade.qmd:5` | Kitamura 1999 citado como apoio à influência das experiências precoces na personalidade | "Contrary to our expectation [...] no early life experiences were correlated with any of the TCI scores" (Kitamura 1999, p. 653) | C1 | alta | conferido |
| V-03 | `critica-interdisciplinar.qmd:35`; `descoberta-as-avessas.qmd:10` | Mischel 1968 lido como situacionismo puro ("os outros 90%? Situação") | Mischel chama o debate de "absurd conceptual split" e a leitura do livro de "substitution problem" (Mischel 2009, p. 283) | C4 | alta | conferido |
| V-04 | `descoberta-as-avessas.qmd:10`; `13-personalidade-como-narrativa.qmd:37, 66` | Nader 2000 e Schiller 2010 (memória de medo condicionado) aplicados à memória autobiográfica ("reconstruída a cada lembrança") | o efeito vale para a memória de medo reativada (Schiller 2010, p. 1; Nader 2000, p. 722). As duas entradas estão `pending-verification` | C4 | média | a conferir |
| V-05 | `04-plasticidade.qmd:13` | quadro "0,5 a 0,7" sem fonte | Roberts 2000, p. 3: 0,31 (infância), 0,54 (faculdade), 0,64 (30 anos), 0,74 (50–70 anos) | C5 | média | a conferir |
| V-06 | `03-periodos-criticos.qmd:13` | trauma infantil "consistentemente associado" a TP, sem fonte | possíveis: Paris, em Livesley 2001, cap. 10, pp. 231–238 (fator de risco, não causa); Cailhol 2020, pp. 5–6 | C5 | média | a conferir |
| V-07 | `08-transtornos.qmd:27` | "a eficácia do tratamento de outros transtornos é reduzida quando há comorbidade com TP", sem fonte | Butcher 2013, p. 358 | C5 | média | a conferir |
| V-08 | `10-tratamento.qmd:15` | a DBT "transformou o prognóstico do TPB de 'intratável' para 'altamente tratável'", sem dados | dados de remissão: Hopwood 2018 (PDF p. 4); Cailhol 2020, p. 4. Avaliar se a frase exagera | C5/C4 | média | a conferir |
| V-09 | `07-tracos.qmd:15, 27` | "psicoticismo" como polo oposto da abertura | DSM-5-TR, p. 893, pareia psicoticismo × lucidez; Kotov 2021 (PDF p. 13): relação "não resolvida"; o psicoticismo de Eysenck é outra coisa (Corr 2009, caps. 20 e 35) | C3/C6 | média | a conferir |
| V-10 | `08-transtornos.qmd:17, 42` | CID-10 com "oito" tipos de TP | Reed 2019, p. 16, diz "dez": explicar a contagem (F60.0–F60.7, subtipos F60.30/31, F60.8, F60.9) | C6 | baixa | a conferir |
| V-11 | `08-transtornos.qmd:73` | esquizotípico "antes classificado junto com eles" | a CID-10 diz "formerly classified with the personality disorders" (p. 201; conferido), mas Bach 2018 ("categorical", p. 8) diz que a CID nunca o classificou como TP; a referência pode ser o DSM-III. Nuance a decidir | C4 | baixa | a conferir |
| V-12 | `atividade-1-casos/00-introducao.qmd:18` | "condições do Eixo I": anacrônico depois do DSM-5 | DSM-5-TR, pp. 15–16, "Removal of the DSM-IV Multiaxial System" (conferido) | C6 | baixa | conferido |
| V-13 | `caso-b.qmd:51` × `caso-c.qmd:50`, `caso-g.qmd:50` | *Detachment* traduzido ora como "distanciamento", ora como "desapego" | padronizar (a CID-11 em português usa "desapego"? conferir) | C6 | baixa | a conferir |
| V-14 | `11-big-data.qmd:23` | "87 milhões" atribuído a Cadwalladr 2018; uso "sobretudo" em 2016 e no Brexit, sem ressalva | Cadwalladr diz "mais de 50 milhões"; 87 milhões estão em Gross 2018 (pp. R527, R529). A empresa negou o uso em 2016; no Brexit, a ligação é via Vote Leave/AggregateIQ | C1/C4 | média | a conferir |
| V-15 | `11-big-data.qmd:25` | afirmações sobre o art. 22 do GDPR sem fonte no acervo (só link) | buscar o texto do GDPR | C5 | baixa | a conferir |
| V-16 | `11-big-data.qmd:61` | "revisão humana" das decisões automatizadas | a LGPD deixou de exigir revisão humana (Lei 13.853/2019); ANPD 2025, pp. 40 e 44 | C3 | média | a conferir |
| V-17 | `11-big-data.qmd:51–55` | art. 5º do AI Act sem as alíneas a, b (manipulação, vulnerabilidades) e f (emoções no trabalho e no ensino) | UE 2024, p. 51 | C4 (omissão) | baixa | a conferir |
| V-18 | `11-big-data.qmd:47` | Choi 2024 creditado com "sensibilidade clinicamente relevante", "sinalização precoce de recaídas", "ajuste de doses em tempo real" | a revisão não diz isso e exclui populações clínicas e estudos de personalidade | C1 | média | a conferir |
| V-19 | `11-big-data.qmd:17` | `krueger_initial_2012` (construção do PID-5) citado para "redes sociais como laboratório de comportamento" | o artigo não trata disso | C1 | média | a conferir |
| V-20 | `05-personalidade-e-saude.qmd:9, 13` | a "mediação comportamental" generalizada para a personalidade | vale para a conscienciosidade (atenuação de 48%), não para o neuroticismo (4%) (Jokela 2020, pp. 7–8) | C4 | média | a conferir |
| V-21 | `references.bib` | `rifkin_myers_briggs_2022` sem o coautor Benedict Carey; data diverge do PDF ("Published Oct. 14, 2022, Updated Oct. 18") | Rifkin 2022, p. 1 | C7 | baixa | a conferir |
| V-22 | `references.bib` | `pessoa_desassossego_pizarro_2010`: chave da edição Pizarro, mas o PDF local é outro e-book, com outra paginação | — | C7 | baixa | a conferir |
| V-23 | `merzenich_plasticity_2014` (caps. 4 e Apêndice II) | autores com afiliação comercial (Posit Science), não mencionada | Merzenich 2014, p. 1. Decisão editorial | — | baixa | a conferir |

Nota sobre fontes: Dobbert 2007 está no `.bib` mas não é citado; o agente que o leu o considerou pouco confiável (atribui a Eysenck um *checklist* que é a PCL de Hare, PDF p. 151). Não usar como fonte de teorias.

### Lote 1

| ID | Arquivo:linha | Problema | O que a fonte diz | Cat. | Grav. | Situação | Decisão do autor |
|---|---|---|---|---|---|---|---|

## Decisões já tomadas na pauta

A pauta de temas da 2ª edição está em <https://claude.ai/artifact/VVHM9kRSTKSYDVP44DZ67X>. As marcações do autor ficam no banco de dados do artefato (coleção `decisoes`) e podem ser lidas com a ferramenta `ArtifactData`. Em 2026-10-04: 49 temas aceitos, 2 em "talvez" (alexitimia; suicídio e morte prematura), 2 recusados (chatbots; EMBERS e Jornadas de 2013), 22 sem marcação, e as 11 correções aceitas. Desdobradas, elas viraram os itens V-01 a V-23 acima, com exceção de V-20, que veio do tema "o neuroticismo custa mais em incapacidade" (sem marcação na pauta). Nota do autor no tema da Cambridge Analytica: "temos que repensar o cap 11".

Os temas aceitos só serão implementados depois desta verificação, num plano a combinar com o autor.

## Progresso

| Lote | Citações conferidas | Itens achados | Decididos | Corrigidos |
|---|---|---|---|---|
| Ponto de partida | — | 23 | 22 aceitos na pauta (a confirmar); V-20 a decidir | 0 |
| 1 | 0 / 107 | — | — | — |
| 2 | 0 / 40 | — | — | — |
| 3 | 0 / 49 | — | — | — |
| 4 | 0 / 495 | — | — | — |
| 5 | 0 / 26 entradas | — | — | — |

## Diário das sessões

- **2026-10-03/04** — Varredura de temas novos (seis agentes sobre o livro e o acervo), publicada como pauta. Durante a varredura apareceram os itens V-01 a V-23; V-01, V-02, V-03 e V-12 foram conferidos no texto da fonte. Este guia foi criado para a sessão seguinte. Nenhum `.qmd` foi alterado.
