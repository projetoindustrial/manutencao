import sqlite3, json

DB = "/home/claude/inspect1/catalogo_fontes_industriais_v33-ponte-banco-calibracao.db"
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

CLUSTER_MAP = {
    # Fundamentos de Confiabilidade
    "confiabilidade_falhas": "fundamentos",
    "Confiabilidade Estática": "fundamentos",
    "Dados_Confiabilidade_SINTEF": "fundamentos",
    "Confiabilidade_Manutencao": "fundamentos",
    "Manutencao_Geral": "fundamentos",
    "confiabilidade_manutencao_texto": "fundamentos",
    "Benchmark_Agente_IA_Confiabilidade": "fundamentos",
    "Confiabilidade_Dutos": "fundamentos",
    # Sensoriamento & dados de campo
    "Vibration": "sensoriamento",
    "Vibração/Prognóstico": "sensoriamento",
    "Acoustic": "sensoriamento",
    "Deteccao_Acustica_Industrial": "sensoriamento",
    "Temperature": "sensoriamento",
    "Pressure": "sensoriamento",
    "Flow": "sensoriamento",
    "Multi-sensor": "sensoriamento",
    # RUL & diagnóstico com IA
    "RUL": "rul_ia",
    "RUL_Rolamentos": "rul_ia",
    "RUL_Turbomaquinas": "rul_ia",
    "Failures": "rul_ia",
    "Fault_Diagnosis / Cost-Sensitive": "rul_ia",
    "Anomaly_Detection / CPS": "rul_ia",
    "Anomaly_Detection_Processos_Quimicos": "rul_ia",
    "Detecção de Anomalia (benchmark)": "rul_ia",
    "Deteccao_Falhas_Processo": "rul_ia",
    "PHM_Challenges": "rul_ia",
    # IIoT, edge & digital twin
    "Digital Twin & AAS": "iiot_twin",
    "Edge & IIoT": "iiot_twin",
    # IA generativa
    "LLMs para Manutenção": "ia_generativa",
    # Gestão da manutenção
    "Work_Orders": "gestao",
    "work_orders_sinteticos": "gestao",
    # Monitoramento de equipamento (vindas de Equipamento_Datasheets)
    "Electrical": "equipamento",
    "Válvulas": "equipamento",
    "Inspection": "equipamento",
    "Bearings": "rul_ia",
    # Portais/curadorias
    "Curadorias / Portais": "portais",
}
CLUSTER_META = {
    "fundamentos":    {"nome": "Fundamentos de Confiabilidade", "desc": "Estatística de falha, MTBF, handbooks clássicos — a base teórica antes de qualquer sensor."},
    "sensoriamento":  {"nome": "Sensoriamento & Dados de Campo", "desc": "Vibração, acústica, temperatura, pressão, vazão — como a máquina \"fala\" antes de quebrar."},
    "rul_ia":         {"nome": "RUL & Diagnóstico com IA", "desc": "Vida útil remanescente, detecção de falha e anomalia — os datasets clássicos de ML em manutenção."},
    "iiot_twin":      {"nome": "IIoT, Edge & Digital Twin", "desc": "Sensoriamento conectado e réplicas digitais de ativos — o lado \"indústria 4.0\"."},
    "ia_generativa":  {"nome": "IA Generativa aplicada", "desc": "LLMs lendo ordem de serviço, relatório de falha e manual técnico."},
    "gestao":         {"nome": "Gestão da Manutenção", "desc": "Ordens de serviço e dados operacionais — o lado prático de quem gerencia a planta."},
    "equipamento":    {"nome": "Monitoramento de Equipamento", "desc": "Datasheets e fontes de equipamento com viés de monitoramento de condição."},
    "portais":        {"nome": "Portais & Curadorias", "desc": "Hubs que agregam várias fontes de uma vez (ex. PHM Society)."},
}

cur.execute("""
    SELECT s.id, t.nome AS tema, s.subtema, s.nome, s.url, s.oferece, s.status,
           s.risco_legal, s.licenca, s.tipo_fonte
    FROM sources s JOIN temas t ON t.id = s.tema_id
    WHERE s.tema_id = 3
       OR s.id IN (SELECT source_id FROM classificacao_macro WHERE macro_categoria='manutencao_preditiva')
       OR s.id IN (SELECT source_id FROM casos_de_uso WHERE equipamento_alvo='rolamento')
""")
rows = cur.fetchall()

def get_list(table, cols, source_id):
    cur.execute(f"SELECT {cols} FROM {table} WHERE source_id=?", (source_id,))
    return cur.fetchall()

sources = []
for r in rows:
    sid = r["id"]
    macro = [m["macro_categoria"] for m in get_list("classificacao_macro", "macro_categoria", sid)]
    micro = [{"tag": m["tag_uso"], "frase": m["frase_uso"]} for m in get_list("classificacao_micro", "tag_uso, frase_uso", sid)]
    casos = [{"equipamento": c["equipamento_alvo"], "nota": c["nota_curta"]} for c in get_list("casos_de_uso", "equipamento_alvo, nota_curta", sid)]
    cluster = CLUSTER_MAP.get(r["subtema"], "fundamentos")
    sources.append(dict(
        id=sid, tema=r["tema"], subtema=r["subtema"], nome=r["nome"], url=r["url"],
        oferece=r["oferece"], status=r["status"], risco_legal=r["risco_legal"],
        licenca=r["licenca"], tipo_fonte=r["tipo_fonte"], macro_categorias=macro,
        tags_uso=micro, casos_de_uso=casos, cluster=cluster,
    ))

# "Comece por aqui": curadoria manual dos 6 datasets mais citados na literatura de PHM/RUL
# (evita duplicata de variante do mesmo dataset, ex. 2x CWRU, 2x FEMTO)
DESTAQUES_NOMES = [
    "NASA FEMTO/PRONOSTIA Bearing Dataset",
    "CWRU Bearing Dataset (Zenodo - Corrected & Cleaned)",
    "XJTU-SY Bearing Dataset",
    "Paderborn University Bearing Dataset",
    "KAIST Bearing Datasets (Run-to-Failure)",
    "IMS Bearings Dataset (NASA Open Data Portal / PCoE)",
]
destaques = [s["id"] for s in sources if s["nome"] in DESTAQUES_NOMES]

out = {
    "gerado_em": "2026-09-27",
    "total": len(sources),
    "clusters": CLUSTER_META,
    "destaques": destaques[:8],
    "sources": sources,
}
with open("/home/claude/site_manutencao/data.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

print("total fontes:", len(sources))
print("destaques 'comece por aqui':", len(destaques))
for d in destaques:
    print(" -", next(s["nome"] for s in sources if s["id"]==d))
from collections import Counter
print(Counter(s["cluster"] for s in sources))
