---
timestamp_utc: 2026-09-27
sessao: criação do site "Manutenção" — projeto irmão do IndústriaEDU
---

# Manutenção — site novo, sem backend

## O que é isso

Um site estático (2 arquivos: `index.html` + `data.json`) que agrega **158 fontes**
do catálogo de dados industriais sobre manutenção e confiabilidade — não só
"manutenção preditiva" (110 fontes), mas o conjunto completo:

- as 110 fontes classificadas como `manutencao_preditiva` no catálogo original, **mais**
- as 12 fontes de confiabilidade "clássica" (estatística de falha, handbooks SINTEF)
  que ficam no mesmo tema mas não têm componente de IA/sensor, **mais**
- 36 fontes de dataset de rolamento (run-to-failure — CWRU, XJTU-SY, Paderborn, KAIST,
  NASA FEMTO/IMS) que estavam catalogadas como "Equipamento" e não apareciam na
  contagem de 110 — achado durante a extração desta sessão, corrigido antes de gerar
  o `data.json` final.

Diferente do "Catálogo de Dados" que já existe dentro do IndústriaEDU (visão genérica,
1.209 fontes, linguagem técnica pra P&D), este site é curado e escrito pro público
geral — landing page com contexto, destaque manual dos 6 datasets mais citados na
literatura de PHM, e navegação por 8 frentes de estudo em vez de 14 temas genéricos.

## Por que não tem backend

122→158 fontes é pouco dado pra justificar Worker + D1 (isso faz sentido pro
catálogo de 1.209+ fontes do IndústriaEDU, que cresce toda semana). Aqui o dado é
curado e muda pouco — `data.json` é gerado uma vez por sessão de atualização e servido
como arquivo estático, junto do `index.html`. Zero custo de hospedagem além do GitHub
Pages, zero dependência de build (sem npm/webpack/etc — é HTML+CSS+JS puro).

## Como publicar

1. Criar um repositório novo no GitHub, ex. `projetoindustrial/manutencao`.
2. Colocar `index.html` e `data.json` na raiz do repositório (mesma pasta).
3. Em Settings → Pages, apontar pra branch `main` / pasta raiz.
4. Pronto: fica em `https://projetoindustrial.github.io/manutencao/`.

Não precisa de `npm install`, não precisa de Actions, não precisa de secret nenhum —
é só HTML/CSS/JS servido direto pelo GitHub Pages.

## Como atualizar o conteúdo depois

O `data.json` foi gerado a partir do `catalogo_fontes_industriais_v33-ponte-banco-
calibracao.db` (o mesmo catálogo que já alimenta o IndústriaEDU) com um script Python
que:
1. Seleciona toda fonte do tema `Confiabilidade_Manutencao` (id 3), **ou** com
   `classificacao_macro.macro_categoria = 'manutencao_preditiva'`, **ou** com
   `casos_de_uso.equipamento_alvo = 'rolamento'`.
2. Agrupa cada fonte numa das 8 frentes de estudo (`cluster`), por `subtema`.
3. Escolhe manualmente 6 destaques pra "Comece por aqui" (lista fixa por nome, pra
   evitar duplicata de variante do mesmo dataset).

Da próxima vez que o catálogo principal for atualizado (nova fonte de manutenção
achada, correção de licença etc.), é só rodar esse mesmo script de novo contra a
versão mais nova do `.db` e substituir o `data.json` — não precisa mexer no
`index.html`.

## Feito na segunda rodada (27-28/09/2026)

- `favicon.svg` (a curva de degradação em miniatura) e `og-image.png` (1200x630, preview
  quando o link é compartilhado) criados e ligados no `<head>` do `index.html`.
  O `og:image` aponta pra `https://projetoindustrial.github.io/manutencao/og-image.png`,
  então só vai aparecer no preview depois do site estar publicado nesse endereço.

## Link de volta: IndústriaEDU → Manutenção

No `Nav.jsx` do IndústriaEDU, um item externo simples (abre em outra aba):

```jsx
<a href="https://projetoindustrial.github.io/manutencao/" target="_blank" rel="noopener">
  Manutenção ↗
</a>
```

Se o `NAV_ITEMS` só aceita itens que trocam de view interna, o mais simples é colocar
esse link no rodapé do site em vez do menu principal.

## Pendências / próximos passos (não bloqueantes)

- Publicar o repositório no GitHub Pages (passo a passo acima).
- Os 6 destaques de "Comece por aqui" foram escolhidos por fama na literatura, não por
  teste com o público — vale revisar depois de ver quem realmente acessa.
- O agrupamento em 8 frentes foi feito por `subtema` (mapeamento manual, `CLUSTER_MAP`
  no script), não por validação fonte a fonte.
