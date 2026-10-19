"""Aplica scripts/curadoria_overrides.json sobre a lista de fontes.

Uso 1 (dentro do exportar_manutencao.py): sources = aplicar(sources)
Uso 2 (em um data.json já gerado):  python3 scripts/aplicar_overrides.py data.json
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OVERRIDES = os.path.join(HERE, "curadoria_overrides.json")


def aplicar(sources, caminho=OVERRIDES):
    ov = json.load(open(caminho, encoding="utf-8"))
    excluir = {e["id"] for e in ov.get("excluir", [])}
    campos = ov.get("campos", {})
    ids = {s["id"] for s in sources}
    faltando = [i for i in list(excluir) + list(campos) if i not in ids]
    if faltando:
        print("aviso: ids do overrides não estão nas fontes:", faltando)
    saida = []
    for s in sources:
        if s["id"] in excluir:
            continue
        for k, v in campos.get(s["id"], {}).items():
            if k in ("evidencia", "url_anterior"):
                continue
            s[k] = v
        saida.append(s)
    return saida


if __name__ == "__main__":
    p = sys.argv[1] if len(sys.argv) > 1 else "data.json"
    d = json.load(open(p, encoding="utf-8"))
    antes = len(d["sources"])
    d["sources"] = aplicar(d["sources"])
    d["total"] = len(d["sources"])
    d["destaques"] = [i for i in d.get("destaques", []) if any(s["id"] == i for s in d["sources"])]
    d["ajustado_em"] = "2026-10-18"
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{antes} -> {d['total']} fontes")
