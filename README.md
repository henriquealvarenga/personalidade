# Personalidade: Uma Breve Introdução

> 2ª edição — 2026

Livro-texto sobre personalidade para o ensino de psicopatologia no Curso de
Medicina da Universidade Federal de São João del-Rei (UFSJ). Em apêndice
opcional, o ensaio filosófico-literário *A descoberta às avessas* problematiza
o próprio conceito.

**Autor:** Henrique Alvarenga da Silva
**Edição:** 2ª edição (2026); a 1ª edição circulou em 2020 como material didático interno
**Site publicado:** <https://henriquealvarenga.github.io/personalidade/>

---

## Construção

O livro é escrito em [Quarto](https://quarto.org/), com bibliografia em BibTeX
validada via *script* Python contra a Crossref API, e publicado automaticamente
em GitHub Pages via GitHub Actions a cada *push* na branch `main`.

Para renderizar localmente:

```bash
quarto render            # HTML + EPUB
quarto preview           # servidor local com hot reload
```

A validação bibliográfica roda independente do render:

```bash
python code/validate_bib.py          # rápida (sem rede)
python code/deep_validate_bib.py     # profunda (Crossref API)
```

---

## Licença

Conteúdo do livro: **CC BY-NC-SA 4.0** — Creative Commons
Atribuição-NãoComercial-CompartilhaIgual.

Código (scripts de validação, workflow, tema): **MIT**.

---

## Créditos de imagens

**Capa**

Fotografia **"Sephia photography of person"** (legenda do autor: *Trippin*) de
**Matúš Kovačovský** (Bratislava, Eslováquia, 30 de abril de 2017), em múltipla
exposição com filtro cromático verde e magenta. Publicada no Unsplash sob a
Licença Unsplash (uso livre, inclusive comercial; atribuição não obrigatória,
mantida aqui por reconhecimento). A sobreposição tipográfica (título, subtítulo,
edição, autor) sobre a fotografia foi feita por Henrique Alvarenga da Silva.

- Autoria da fotografia: [Matúš Kovačovský (\@ohamko)](https://unsplash.com/@ohamko?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
- Título no Unsplash: *Sephia photography of person*
- Legenda do autor: *Trippin*
- Fonte: [Unsplash](https://unsplash.com/photos/sephia-photography-of-person-eIvLuyDjCQI?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
- URL canônica: <https://unsplash.com/photos/sephia-photography-of-person-eIvLuyDjCQI>
- Licença: [Unsplash License](https://unsplash.com/license)

---

## Contato

📧 <henrique@ufsj.edu.br>
🔗 <https://github.com/henriquealvarenga/personalidade>
