# Manutenção

Catálogo curado de 157 fontes de dado sobre manutenção preditiva e confiabilidade industrial (vibração, temperatura, ordens de serviço, vida útil remanescente), organizado em 8 frentes de estudo, com busca e status de licença por fonte.

**Acesse:** https://projetoindustrial.github.io/manutencao/

- Site estático: `index.html` + `data.json`, sem build e sem backend.
- A página só aponta para os sites originais; não hospeda nem copia os dados.
- A licença exibida é um resumo e pode estar desatualizada: confirme sempre na fonte antes de reutilizar. Fontes ambíguas ou não verificadas aparecem como tal e ficam fora de "só uso livre confirmado".
- Projeto independente, sem vínculo com as organizações citadas.

## Atualizar os dados

`scripts/exportar_manutencao.py` gera o `data.json` a partir do banco do catálogo de fontes industriais (`catalogo-fontes-industriais`). Rode contra o `.db` mais recente (hoje o `v33`, que fica fora deste repositório) e substitua o `data.json`; o `index.html` não precisa mudar. As correções de curadoria em `scripts/curadoria_overrides.json` são reaplicadas automaticamente por `scripts/aplicar_overrides.py`. Detalhes e decisões de curadoria em `LEIAME.md`.

## Relação com outros repositórios

- `fontes-industriais` (catálogo público de fontes abertas): há sobreposição parcial (48 links em comum, medidos em 18/10/2026). Os dois ficam separados de propósito: este tem curadoria e linguagem para o público geral, com foco só em manutenção.
- `industriaedu` e `caderno`: sites irmãos, ligados no menu.
