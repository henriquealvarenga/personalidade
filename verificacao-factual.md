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
| V-01 | `05-personalidade-e-saude.qmd:7` | Kotov 2010 citado como prova de que o traço é "preditor de incidência ao longo do tempo" | "estimates of concurrent associations rather than causal effects", porque os dados são quase todos transversais (Kotov 2010, p. 803) | C1 | alta | conferido (reconfirmado no Lote 1) |
| V-02 | `02-construcao-da-personalidade.qmd:5` | Kitamura 1999 citado como apoio à influência das experiências precoces na personalidade; Kitamura 2003 só acha associações pontuais; nenhuma das quatro fontes diz "diferentes para cada função cerebral" | "Contrary to our expectation [...] no early life experiences were correlated with any of the TCI scores" (Kitamura 1999, p. 653); Kitamura 2003, p. 323; para "cada função", Knudsen 2004, p. 1421 | C1 | alta | conferido (reconfirmado no Lote 1) |
| V-03 | `critica-interdisciplinar.qmd:35`; `descoberta-as-avessas.qmd:10` | Mischel 1968 lido como situacionismo puro ("os outros 90%? Situação") | Mischel chama o debate de "absurd conceptual split" e a leitura do livro de "substitution problem" (Mischel 2009, p. 283) | C4 | alta | conferido |
| V-04 | `descoberta-as-avessas.qmd:10`; `13-personalidade-como-narrativa.qmd:37, 66` | Nader 2000 e Schiller 2010 (memória de medo condicionado) aplicados à memória autobiográfica ("reconstruída a cada lembrança") | o efeito vale para a memória de medo reativada (Schiller 2010, p. 1; Nader 2000, p. 722). As duas entradas estão `pending-verification` | C4 | média | a conferir |
| V-05 | `04-plasticidade.qmd:13` | quadro "0,5 a 0,7" sem fonte; "ao longo de décadas" errado (os valores são para intervalos de 6,7 anos e caem em décadas); demais afirmações do quadro sem fonte | Roberts 2000, p. 3: 0,31 (infância), 0,54 (faculdade), 0,64 (30 anos), 0,74 (50–70 anos), intervalo fixo de 6,7 anos; p. 16: 0,49 em 10 anos, 0,41 em 20, 0,25 em 40. Resto: Hopwood 2018 (PDF pp. 6–8); fármacos: Widiger 2013, p. 172 | C5 | média | conferido (Lote 1) |
| V-06 | `03-periodos-criticos.qmd:13` | trauma infantil "consistentemente associado" a TP, sem fonte; "consistentemente" exagera | Paris, em Livesley 2001, cap. 10, pp. 231–237 (não 238): fator de risco, não causa; abuso físico "less consistent". Butcher 2013, pp. 352–353. Cailhol 2020, pp. 5–6 (só TPB) | C5 | média | conferido (Lote 1) |
| V-07 | `08-transtornos.qmd:27` | "a eficácia do tratamento de outros transtornos é reduzida quando há comorbidade com TP", sem fonte | Butcher 2013, p. 358 (`pending-verification`); para a depressão, Paris 2007, p. 38, já citado no parágrafo | C5 | média | conferido (Lote 1) |
| V-08 | `10-tratamento.qmd:15` | a DBT "transformou o prognóstico do TPB de 'intratável' para 'altamente tratável'", sem dados; exagera | a melhora do prognóstico veio dos seguimentos naturalísticos (DSM-5-TR, p. 755; Gunderson 2009, pp. 530, 534; Cailhol 2020, p. 4); a DBT tem evidência de baixa qualidade (Storebø 2020, p. 2) | C4 | média | conferido (Lote 1) |
| V-09 | `07-tracos.qmd:15, 27` | "psicoticismo" como polo oposto da abertura; "Lucidez" como polo saudável da abertura | DSM-5-TR, p. 893, pareia psicoticismo × lucidez; Kotov 2021, p. 19.13: relação "unsettled"; quando proposta, a ligação é com abertura alta (Widiger 2013, p. 286), o inverso da tabela; o psicoticismo de Eysenck é outro construto (Corr 2009, p. 326) e aparece em `atividade-2-visoes-ia/01-leitura-preparatoria.qmd:25` sem distinção | C3/C6 | média | conferido (Lote 1) |
| V-10 | `08-transtornos.qmd:17, 42` | CID-10 com "oito" tipos de TP: o número está certo, mas convém explicar a contagem | Reed 2019, p. 16, diz "dez"; WHO 1992, p. 198: oito tipos com nome (F60.0–F60.7), subtipos F60.30/31, F60.8 "outros", F60.9 "não especificado" | C6 | baixa | conferido (Lote 1) |
| V-11 | `08-transtornos.qmd:73` | esquizotípico "antes classificado junto com eles" | a CID-10 diz "formerly classified with the personality disorders" (p. 201); `bach_categorical_2018`, p. 8: "never been classified as such in the ICD"; como TP, entrou no DSM-III (Dolan-Sewell et al., em Livesley 2001, p. 89). Nuance a decidir | C4 | baixa | conferido (Lote 1) |
| V-12 | `atividade-1-casos/00-introducao.qmd:18` | "condições do Eixo I": anacrônico depois do DSM-5 | DSM-5-TR, pp. 15–16, "Removal of the DSM-IV Multiaxial System" (conferido) | C6 | baixa | conferido |
| V-13 | `caso-b.qmd:51` × `caso-c.qmd:50`, `caso-g.qmd:50` | *Detachment* traduzido ora como "distanciamento", ora como "desapego" | padronizar (a CID-11 em português usa "desapego"? conferir) | C6 | baixa | a conferir |
| V-14 | `11-big-data.qmd:23` | "87 milhões" atribuído a Cadwalladr 2018; uso "sobretudo" em 2016 e no Brexit, sem ressalva | Cadwalladr diz "mais de 50 milhões"; 87 milhões estão em Gross 2018 (pp. R527, R529). A empresa negou o uso em 2016; no Brexit, a ligação é via Vote Leave/AggregateIQ | C1/C4 | média | a conferir |
| V-15 | `11-big-data.qmd:25` | afirmações sobre o art. 22 do GDPR sem fonte no acervo (só link) | buscar o texto do GDPR | C5 | baixa | a conferir |
| V-16 | `11-big-data.qmd:61` | "revisão humana" das decisões automatizadas | a LGPD deixou de exigir revisão humana (Lei 13.853/2019); ANPD 2025, pp. 40 e 44 | C3 | média | a conferir |
| V-17 | `11-big-data.qmd:51–55` | art. 5º do AI Act sem as alíneas a, b (manipulação, vulnerabilidades) e f (emoções no trabalho e no ensino) | UE 2024, p. 51 | C4 (omissão) | baixa | a conferir |
| V-18 | `11-big-data.qmd:47` | Choi 2024 creditado com "sensibilidade clinicamente relevante", "sinalização precoce de recaídas", "ajuste de doses em tempo real" | a revisão não diz isso e exclui populações clínicas e estudos de personalidade | C1 | média | a conferir |
| V-19 | `11-big-data.qmd:17` | `krueger_initial_2012` (construção do PID-5) citado para "redes sociais como laboratório de comportamento" | o artigo não trata disso | C1 | média | a conferir |
| V-20 | `05-personalidade-e-saude.qmd:9, 13` | "conscienciosidade opera **majoritariamente** por mediação comportamental" (05:9), sem fonte. **Reformulado no Lote 1:** os 48% e 4% registrados antes são de anos livres de incapacidade, não de mortalidade; "em parte" (05:13) está certo para os dois traços | Jokela 2020, PDF pp. 7–8: na mortalidade, o ajuste atenuou 25% (conscienciosidade) e 75% (baixa estabilidade emocional); nos anos livres de incapacidade, 48% e 4%. McGeehan 2026, p. 786 | C4 | média | conferido (Lote 1) |
| V-21 | `references.bib` | `rifkin_myers_briggs_2022` sem o coautor Benedict Carey; data diverge do PDF ("Published Oct. 14, 2022, Updated Oct. 18") | Rifkin 2022, p. 1 | C7 | baixa | a conferir |
| V-22 | `references.bib` | `pessoa_desassossego_pizarro_2010`: chave da edição Pizarro, mas o PDF local é outro e-book, com outra paginação | — | C7 | baixa | a conferir |
| V-23 | `merzenich_plasticity_2014` (caps. 4 e Apêndice II) | autores com afiliação comercial (Posit Science), não mencionada | Merzenich 2014, p. 1 (afiliações) e p. 16 (declaração de conflito de interesse: os autores desenvolvem os programas descritos). Decisão editorial | — | baixa | conferido (Lote 1) |

Nota sobre fontes: Dobbert 2007 está no `.bib` mas não é citado; o agente que o leu o considerou pouco confiável (atribui a Eysenck um *checklist* que é a PCL de Hare, PDF p. 151). Não usar como fonte de teorias.

### Lote 1

Levantamento de 2026-10-04: cinco agentes (caps. 1–3, 4–5, 6–7, 8, 9–10), e todos os itens C1, C3 e C4 reconferidos pelo coordenador no texto da fonte. Os itens V do ponto de partida que caem no Lote 1 continuam na tabela acima. O texto completo de cada item (trecho do livro, citações da fonte com página e proposta de correção) está na página de decisão, <https://claude.ai/artifact/ULA13Dpft76yPmgHpyVhoH>, coleção `itens` do banco de dados (leitura com `ArtifactData`); as decisões do autor ficam na coleção `decisoes`. Aqui vai o resumo.

| ID | Arquivo:linha | Problema | Fonte (páginas) | Cat. | Grav. | Situação | Decisão do autor |
|---|---|---|---|---|---|---|---|
| L1-01 | `01-introducao.qmd:8`; `05-personalidade-e-saude.qmd:5`; `06-taxonomia.qmd:9` | A história dos quatro temperamentos diverge entre os caps. 1, 5 e 6; Stelmack nuança (Hipócrates: humores e doença; Galeno: nove temperamentos; tipologia de caráter dos séculos XVIII–XIX). | Stelmack 1991, pp. 255, 256, 259–260 | C3/C4 | média | conferido | |
| L1-02 | `01-introducao.qmd:8` | Wundt é do século XIX (Wundt 1886); "1.500 anos" não está em Stelmack. | Stelmack 1991, pp. 260–261 | C3 | média | conferido | |
| L1-03 | `01-introducao.qmd:14` | "Todas essas teorias" exagera: Cloninger formula como hipótese e lembra que os pressupostos não são compartilhados. | Cloninger 2009, p. 5 | C4 | média | conferido | |
| L1-04 | `01-introducao.qmd:16` | Funde ciência × humanismo com idiográfico × nomotético; Cloninger trata em separado. | Cloninger 2009, pp. 7–8, 11 | C4 | baixa | conferido | |
| L1-05 | `02-construcao-da-personalidade.qmd:7` | Chama de "períodos críticos" o que o cap. 3 chama de períodos sensíveis. | — | C6 | baixa | conferido | |
| L1-06 | `03-periodos-criticos.qmd:5–9` | Para Knudsen, o crítico é uma classe especial de sensível (irreversível), não um tipo paralelo. | Knudsen 2004, p. 1412 | C4 | baixa | conferido | |
| L1-07 | `03-periodos-criticos.qmd:7` | Hubel e Wiesel sem citação; "semanas" → meses; "logo depois"; profundidade → visão estereoscópica. | Knudsen 2004, pp. 1413, 1421; Takesian 2013, p. 6 | C5 | média | conferido | |
| L1-08 | `03-periodos-criticos.qmd:7` | GABA marca a abertura do período crítico; os freios, o fechamento (e são reversíveis). | Takesian 2013, pp. 3–4 | C1 | baixa | conferido | |
| L1-09 | `03-periodos-criticos.qmd:9` | N = 669.498: "quase", não "mais de" 670 mil. | Hartshorne 2018, p. 263 | C3 | baixa | conferido | |
| L1-10 | `03-periodos-criticos.qmd:9, 11` | Hartshorne fala em período crítico; mede aprendizado de gramática (2ª língua), não "aquisição nativa". | Hartshorne 2018, p. 263 e ms. p. 12; Knudsen 2004, p. 1421 | C4 | baixa | conferido | |
| L1-11 | `03-periodos-criticos.qmd:9` | Sem fonte; Takesian descreve período crítico pré-frontal em camundongos. | Takesian 2013, p. 15; Gogtay 2004, p. 8177 | C5 | baixa | conferido | |
| L1-12 | `03-periodos-criticos.qmd:11` | "Metade da terceira década" não está nas fontes (Gogtay: 4–21 anos; Mills: estabiliza na terceira década). | Gogtay 2004, pp. 8174, 8176; Mills 2016 | C4 | média | conferido | |
| L1-13 | `03-periodos-criticos.qmd:15–18`; `09-epidemiologia.qmd:28–34`; `10-tratamento.qmd:28–36` | Três quadros "[VERIFICAR]" visíveis no site; o do cap. 10 atribui à CID-11 uma orientação terapêutica que ela não dá. | CDDR, p. 554 | forma | baixa | conferido | |
| L1-14 | `04-plasticidade.qmd:9` | As fontes medem sintomas e funcionamento; Hadjipavlou diz que os traços persistem. | Hadjipavlou 2010, pp. 202, 208; Storebø 2020, p. 1 | C1 | alta | conferido | |
| L1-15 | `04-plasticidade.qmd:18` | Merzenich 2014 não fala em 1980–90 nem em piano; "radicalmente" omite a ressalva. | Merzenich 2014, p. 2 | C1 | média | conferido | |
| L1-16 | `04-plasticidade.qmd:20` | Frase incompleta; "complexas" × "completas" no apêndice. | — | forma | baixa | conferido | |
| L1-17 | `04-plasticidade.qmd:18, 27` | Salto de mapas sensoriais para traços; nenhuma fonte liga os dois. | Merzenich 2014, pp. 2–5 | C4 | média | conferido | |
| L1-18 | `05-personalidade-e-saude.qmd:9` | Resumo de Willroth dá 0,83/1,22; resultados e figura dão 0,82/1,12. | Willroth 2025, manuscrito, PDF pp. 2, 27, 29 | C3 | média | conferido | |
| L1-19 | `05-personalidade-e-saude.qmd:9` | McGeehan não corrobora a amabilidade. | McGeehan 2026, p. 786 | C4 | baixa | conferido | |
| L1-20 | `05-personalidade-e-saude.qmd:11` | Desfecho é morte por infarto; depressão = sintomas na HADS; não replica a diferença entre os sexos. | Karlsen 2024, pp. 1352, 1361, 1365 | C4 | média | conferido | |
| L1-21 | `05-personalidade-e-saude.qmd:11` | "2023 e 2025" com uma só citação; "inferência causal" mais forte que "putative". | Rukh 2023, p. 856; Zhang 2025 | C4 | baixa | conferido | |
| L1-22 | `05-personalidade-e-saude.qmd:11` | RM não mede valor preditivo; Zhang achou efeito também do escore global. | Zhang 2025, resumo | C4 | baixa | conferido | |
| L1-23 | `06-taxonomia.qmd:11` | "Violento" não é tipo de Schneider (é abúlico); "perverso" = desalmado; "carente de autoestima" × "que busca valorização". | Berrios 1993, p. 22; Livesley 2001, p. 5 | C3 | média | conferido | |
| L1-24 | `06-taxonomia.qmd:11, 15` | "Tornou" → "contribuiu para tornar"; anormal (desvio da média) × psicopática (faz sofrer) fundidos. | Berrios 1993, p. 22; Livesley 2001, p. 5 | C4 | baixa | conferido | |
| L1-25 | `06-taxonomia.qmd:19` | Big Five = Five-Factor Model (FFM), não Five-Factor Theory. | DSM-5-TR, p. 893; Widiger 2013, p. 69 | C3 | média | conferido | |
| L1-26 | `06-taxonomia.qmd:23` | O DSM-III tinha onze TPs (com o passivo-agressivo), não dez. | Widiger 2013, pp. 33, 44; Widiger 2001, pp. 63–64, 68 | C3 | média | conferido | |
| L1-27 | `06-taxonomia.qmd:23`; `08-transtornos.qmd:17` | Cap. 6 dá à CID-10 a estrutura do DSM; cap. 8 a chama de intermediária e de uso parcial por legado. | WHO 1992, pp. 200–202, 207; Prata 2025, p. 4 | C3/C6 | média | conferido | |
| L1-28 | `06-taxonomia.qmd:23`; `07-tracos.qmd:45`; `08-transtornos.qmd:38` | AMPD é híbrido, não puramente dimensional; foi para a Seção III como compromisso após rejeição, não por complexidade nem como prenúncio. | DSM-5-TR, p. 881; Mulder 2019, p. 28; DSM-5 BR, p. 645 | C1/C4 | média | conferido | |
| L1-29 | `06-taxonomia.qmd:27` | Reed fala da maioria dos casos graves, não de todos os pacientes com TP. | Reed 2019, p. 16 | C4 | baixa | conferido | |
| L1-30 | `06-taxonomia.qmd:29`; `08-transtornos.qmd:69` | Bach 2018 não dá essas razões (DBT, "inviável reformar", prognóstico); caps. 6 e 8 divergem entre si. | Bach e First 2018, pp. 5, 12; Reed 2019, p. 16; Mulder 2024, p. 122; CDDR, p. 554 | C1 | média | conferido | |
| L1-31 | `07-tracos.qmd:5` | Definição de personalidade sem fonte. | — | C5 | baixa | conferido | |
| L1-32 | `07-tracos.qmd:9, 49` | 17.953 termos (4.504 estáveis); Goldberg não fala do 16PF; Baumgarten veio antes; frase sobre livros didáticos sem fonte. | Allport e Odbert 1936, pp. 23–26; Goldberg 1993, p. 26; Corr 2009, p. 113 | C4 | baixa | conferido | |
| L1-33 | `07-tracos.qmd:37–41` | Citação literal sem página, com omissão e chave da edição inglesa. | DSM-5-TR, p. 893 | C2 | baixa | conferido | |
| L1-34 | `07-tracos.qmd:43` | Entitled ≠ "autoritária" (senso de merecimento). | Roberts 2017, p. 105 | C3 | baixa | conferido | |
| L1-35 | `08-transtornos.qmd:5` | 1923 → já passou mais de um século. | Berrios 1993, p. 22 | C3 | baixa | conferido | |
| L1-36 | `08-transtornos.qmd:9–15` | Descritores dos grupos não são os do DSM (A = esquisitos ou excêntricos); falta a ressalva sobre validade. | DSM-5 BR, p. 646; DSM-5-TR, p. 734 | C3 | média | conferido | |
| L1-37 | `08-transtornos.qmd:23` | Magallón-Neri não compara estigmas; Catthoor só estigma percebido em adolescentes; Sheehan sustenta com "might". | Magallón-Neri 2013; Catthoor 2015, p. 81; Sheehan 2016, p. 3 | C1 | média | conferido | |
| L1-38 | `08-transtornos.qmd:25` | Zimmerman atribui a relutância à falta de tempo, não ao estigma. | Zimmerman 1999, p. 1572; Sheehan 2016, pp. 4–5; Paris 2007, p. 36 | C4 | média | conferido | |
| L1-39 | `08-transtornos.qmd:31` | Sem fonte; a masoquista só esteve no apêndice do DSM-III-R. | Widiger 2001, pp. 66, 68; Millon 2001, p. 44 | C5 | média | conferido | |
| L1-40 | `08-transtornos.qmd:31` | Contradiz o próprio capítulo: o padrão borderline foi preservado. | CDDR, p. 554 | C6 | média | conferido | |
| L1-41 | `08-transtornos.qmd:33` | Szasz fala de doença mental em geral; as aspas não são citação literal. | Szasz 1974, pp. 5, 262 | C4 | média | conferido | |
| L1-42 | `08-transtornos.qmd:46–51` | Existe 6D10.Z; graduar não é obrigatório. | CDDR, p. 553 | C3 | baixa | conferido | |
| L1-43 | `08-transtornos.qmd:67` | Descrição omite autoimagem e impulsividade. | CDDR, p. 564 | C4 | baixa | conferido | |
| L1-44 | `08-transtornos.qmd:95` | "Hegemônico" o DSM e "hegemonia" da CID-11 no mesmo quadro. | — | C6 | média | conferido | |
| L1-45 | `08-transtornos.qmd (linhas 23, 25, 27, 42, 69, 76, 95)` | Padrão misto de páginas no capítulo. | — | C2 | baixa | conferido | |
| L1-46 | `09-epidemiologia.qmd:7` | "Combinada" é soma (conta em dobro); omite o evitativo, o mais frequente (14,7%). | Zimmerman 2005, pp. 1911–1912 | C1 | média | conferido | |
| L1-47 | `09-epidemiologia.qmd:16, 21, 24` | Legenda diz "população" para coluna clínica; asterisco mal posicionado. | Torgersen 2001, p. 593 | C6 | baixa | conferido | |
| L1-48 | `10-tratamento.qmd:5` | "Poucos estudos" não vale para o borderline; sem fonte. | Hadjipavlou 2010, p. 203; Butcher 2013, p. 360 | C5 | baixa | conferido | |
| L1-49 | `10-tratamento.qmd:15` | Leitura de Linehan: o modelo é transacional e mantém a vulnerabilidade biológica; não "adaptações racionais". | Widiger 2013, pp. 397–398; Gunderson 2009, p. 534 | C4 | média | conferido | |
| L1-50 | `10-tratamento.qmd:19` | Quadro da DBT correto, sem fonte. | Hadjipavlou 2010, p. 205; Gunderson 2009, p. 534 | C5 | baixa | conferido | |
| L1-51 | `10-tratamento.qmd:24` | "Forte evidência" da MBT contradiz a Cochrane (baixa qualidade). | Storebø 2020, pp. 2, 34 | C3 | média | conferido | |
| L1-52 | `10-tratamento.qmd:26` | "Boa evidência" exagera no TPB (poucos ensaios); nada sustenta o grupo C. | Storebø 2020, pp. 20, 39; Lampe 2018, p. 62; Pinto 2022, p. 392 | C4 | média | conferido | |
| L1-53 | `references/references.bib` | Prenomes errados (Kitamura ×2, Stelmack), notes incoerentes (LeDoux, Willroth, Bach), editora de Szasz, título da CID-11, ano de Mulder 2024. | PDFs e Crossref | C7 | baixa | a conferir | |
| L1-54 | `references/references.bib` | Situação das seis pending do lote (+ Linehan): o que confere e o que falta. | Crossref; Open Library; PDFs | C7 | baixa | a conferir | |

**Propostas de correção que citam obras novas no texto** (Paris em Livesley 2001, Widiger 2001, Gunderson 2009, Roberts 2000, Butcher 2013 etc.) passam pela conferência dupla na Fase 3 antes de entrar. Butcher 2013, Corr 2009 e Roberts 2000 estão `pending-verification`; o capítulo de Paris não tem entrada própria no `.bib`.

#### Aguardando páginas do autor (obras fora do acervo)

Em 2026-10-04 o autor decidiu mandar fotos das páginas destes livros. As frases abaixo não foram julgadas; quando as páginas chegarem, conferir e acrescentar itens se for o caso. Entre parênteses, o que outra obra do acervo já confirma.

| Obra | Onde é citada | O que conferir |
|---|---|---|
| `andreasen_introductory_2014` (`pending-verification`) | `08:21`; `09:5` (×2); `10:7` | folha de rosto (ordem dos autores: Black primeiro?; edição); "muitos psiquiatras consideram a abordagem atual de pouca ajuda"; prevalência de 9–16% e de 30–50% (o acervo dá a ordem de grandeza: Volkert 2018, p. 709; Zimmerman 2005, pp. 1911, 1916); terapia de grupo desaconselhada no paranoide (nada no acervo) |
| `linehan_cognitive_1993` | `10:13` (e as ideias de `10:15` e `10:19`) | DBT "nos anos 1980-90" (Corr 2009, p. 808, cita Linehan 1987); teoria biossocial (ver L1-49); módulos, coaching por telefone, 12 meses |
| `schneider_psychopathic_1958` | `06:11` | sumário com os dez tipos e definições de personalidade anormal e psicopática (Berrios 1993, p. 22, e Livesley 2001, p. 5, já conferidos: ver L1-23 e L1-24) |
| `widiger_oxford_2017` | `06:19` | capítulo introdutório (os cinco domínios e a consolidação nos anos 1980 já estão em Goldberg 1993, pp. 26–27; o rótulo "FFT" é o item L1-25). O `.bib` tem o organizador; a suspeita do planejamento era infundada |
| `ledoux_synaptic_self_2002` | `04:24` | a tese do "eu" como coordenação imperfeita de sistemas paralelos; o apêndice (`critica-interdisciplinar.qmd:21`) atribui a LeDoux uma tese mais forte ("ficção sintetizada"); título da edição brasileira (ver L1-53) |
| `doidge_brain_changes_2007` | `04:20` | hemisferectomia e substituição sensorial; "funções complexas" (cap. 4) × "funções completas" (`critica-interdisciplinar.qmd:17`) |
| `laing_divided_self_1960` | `08:33` | a "inversão de perguntas" (as perguntas entre aspas parecem formulação do livro, não citação) |

#### Pistas para os próximos lotes (achadas durante o Lote 1)

- `critica-interdisciplinar.qmd:15` repete as datas de Merzenich e o exemplo do piano (L1-15); `:17`, "funções completas" (Doidge); `:21`, LeDoux; `:72`, a leitura de Linehan (L1-49); `:74`, a personalidade masoquista (L1-39).
- `descoberta-as-avessas.qmd:12` cita Roberts 2000 para estabilidade "ao longo de décadas" (V-05).
- `atividade-2-visoes-ia/01-leitura-preparatoria.qmd:25` usa "psicoticismo" no sentido de Eysenck (V-09).
- A contagem do guia (107 no Lote 1) inclui duas referências cruzadas a tabelas (`@tbl-...`); o lote tem 105 citações bibliográficas. O comando de recontagem tem o mesmo efeito nos outros lotes.

#### Roteiro da Fase 3 (Lote 1)

A unidade de trabalho é o **item**, não o capítulo: cada item é corrigido em todos os locais do campo `local`, mesmo em outros capítulos. Os números de linha mudam com as correções; localizar o trecho pelo texto. Combinado com o autor em 2026-10-04:

| Sessão | Itens | Livros cujas fotos entram aqui |
|---|---|---|
| 1 | V-01, V-02, L1-14 (gravidade alta); L1-01, L1-27, L1-28, L1-30 (vários capítulos) | — |
| 2 | L1-02, L1-03, L1-04, L1-05, L1-06, L1-07, L1-08, L1-09, L1-10, L1-11, L1-12, V-06, L1-13 (caps. 1–3 e quadros VERIFICAR) | — |
| 3 | V-05, L1-15, V-23, L1-16, L1-17, L1-18, L1-19, V-20, L1-20, L1-21, L1-22 (caps. 4–5) | LeDoux, Doidge |
| 4 | L1-23, L1-24, L1-25, L1-26, L1-29, L1-31, L1-32, V-09, L1-33, L1-34 (caps. 6–7) | Schneider, Widiger |
| 5 | L1-35, L1-36, V-10, L1-37, L1-38, V-07, L1-39, L1-40 (cap. 8, linhas 5–31) | Andreasen (08:21) |
| 6 | L1-41, L1-42, L1-43, V-11, L1-44, L1-45 (cap. 8, linhas 33–95) | Laing |
| 7 | L1-46, L1-47, L1-48, V-08, L1-49, L1-50, L1-51, L1-52 (caps. 9–10); L1-53, L1-54 (`.bib`) | Andreasen (09:5, 10:7), Linehan |

## Decisões já tomadas na pauta

A pauta de temas da 2ª edição está em <https://claude.ai/artifact/VVHM9kRSTKSYDVP44DZ67X>. As marcações do autor ficam no banco de dados do artefato (coleção `decisoes`) e podem ser lidas com a ferramenta `ArtifactData`. Em 2026-10-04: 49 temas aceitos, 2 em "talvez" (alexitimia; suicídio e morte prematura), 2 recusados (chatbots; EMBERS e Jornadas de 2013), 22 sem marcação, e as 11 correções aceitas. Desdobradas, elas viraram os itens V-01 a V-23 acima, com exceção de V-20, que veio do tema "o neuroticismo custa mais em incapacidade" (sem marcação na pauta). Nota do autor no tema da Cambridge Analytica: "temos que repensar o cap 11".

Os temas aceitos só serão implementados depois desta verificação, num plano a combinar com o autor.

## Progresso

| Lote | Citações conferidas | Itens achados | Decididos | Corrigidos |
|---|---|---|---|---|
| Ponto de partida | — | 23 | 22 aceitos na pauta (a confirmar); V-20 a decidir | 0 |
| 1 | 105 / 105 (55 sem problema, 40 com problema, 10 dependem de obras fora do acervo) | 54 novos (L1-01 a L1-54; 1 alta, 26 média, 27 baixa) + 11 itens V reconferidos | 0 (página de decisão publicada em 2026-10-04) | 0 |
| 2 | 0 / 40 | — | — | — |
| 3 | 0 / 49 | — | — | — |
| 4 | 0 / 495 | — | — | — |
| 5 | 0 / 26 entradas | — | — | — |

## Diário das sessões

- **2026-10-03/04** — Varredura de temas novos (seis agentes sobre o livro e o acervo), publicada como pauta. Durante a varredura apareceram os itens V-01 a V-23; V-01, V-02, V-03 e V-12 foram conferidos no texto da fonte. Este guia foi criado para a sessão seguinte. Nenhum `.qmd` foi alterado.
- **2026-10-04** — Lote 1, Fase 1. Cinco agentes só leitura conferiram as 105 citações dos caps. 1–10 e as afirmações sem citação; o coordenador reconferiu no texto da fonte todos os itens C1, C3 e C4 e os itens V do lote (nenhum caiu). Resultado: 54 itens novos (L1-01 a L1-54) e 11 itens V reconferidos; V-20 foi reformulado (os 48%/4% de Jokela são de anos livres de incapacidade, não de mortalidade). Itens publicados para decisão do autor em <https://claude.ai/artifact/ULA13Dpft76yPmgHpyVhoH> (coleções `itens` e `decisoes`). Sete obras fora do acervo aguardam fotos das páginas, enviadas pelo autor. Nenhum `.qmd` foi alterado. **Próximo passo:** ler as decisões (`ArtifactData`, coleção `decisoes`), copiar para a coluna "Decisão do autor" e fazer a Fase 3.
