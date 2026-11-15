# Dados abertos — Manutenção preditiva e confiabilidade

- `catalogo.csv` — uma linha por item, colunas: id, nome, cluster, tema, subtema, url, oferece, status, risco_legal, licenca, tipo_fonte, macro_categorias, tags_uso, casos_de_uso.
- `catalogo.jsonl` — os mesmos itens, um objeto JSON por linha.

Gerados em 2026-11-07 a partir do `data.json` do próprio site. Confira licença e atualidade na fonte antes de reutilizar.

## Significado dos códigos

As colunas `status` e `risco_legal` do CSV e do JSONL guardam códigos; nas páginas em texto eles aparecem traduzidos.

`status` (como foi a verificação da fonte):

| Código | Significado |
|---|---|
| CONFIRMADO | confirmada em duas verificações independentes |
| VERIFICADO | verificada uma vez |
| CONFIRMADO_RESTRICAO_LICENCA | confirmada, mas com restrição de licença |
| AMBIGUO | ambígua: não foi possível decidir se a licença permite o uso |
| BLOQUEADO_FERRAMENTA | não verificada: a ferramenta de verificação foi bloqueada pelo site |
| BLOQUEADO | indisponível na fonte oficial |

`risco_legal` (risco da licença para reutilizar os dados; mesmos rótulos do app):

| Código | Rótulo |
|---|---|
| OK, ABERTO | uso livre |
| AMBIGUO | ambíguo: leia a licença |
| RESTRITO | restrito |
| BLOQUEADO | bloqueado |
