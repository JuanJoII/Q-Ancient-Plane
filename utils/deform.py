import maya.cmds as cmds
from Utils.config import CONFIG
import random


def aplicar_deformaciones(parte, objeto_generado):
    """
    Aplica deformaciones a partir de los objectSets definidos en CONFIG[parte]["deformaciones"].
    Cada deformación toma un set de edges o vértices y realiza un escalado aleatorio controlado.
    """

    if parte not in CONFIG or "deformaciones" not in CONFIG[parte]:
        return

    deformaciones = CONFIG[parte]["deformaciones"]
    if not deformaciones:
        return

    for def_data in deformaciones:
        # Saltar deformaciones desactivadas
        if not def_data.get("activo", True):
            print(
                f"[⏭] {parte}: deformación inactiva → {def_data.get('selection_set', 'sin nombre')}"
            )
            continue

        set_name = def_data.get("selection_set")
        if not set_name or not cmds.objExists(set_name):
            print(f"[!] Selection set no encontrado: {set_name}")
            continue

        # Obtener los componentes del set
        componentes = cmds.sets(set_name, query=True)
        if not componentes:
            print(f"[!] Set vacío: {set_name}")
            continue

        # Determinar tipo (edge o vértice)
        edges = [c for c in componentes if ".e[" in c]
        verts = [c for c in componentes if ".vtx[" in c]

        if edges and not verts:
            verts = cmds.polyListComponentConversion(edges, toVertex=True)
            verts = cmds.ls(verts, flatten=True)

        if not verts:
            print(f"[!] No se encontraron vértices en {set_name}")
            continue

        # --- Escalado aleatorio controlado ---
        base_scale = def_data.get("escala", [1, 1, 1])
        rango_random = def_data.get("rango_random", [0.9, 1.1])
        ejes = def_data.get("ejes", [1, 1, 1])

        factor = random.uniform(rango_random[0], rango_random[1])
        escala_final = [base_scale[i] * factor if ejes[i] else 1.0 for i in range(3)]

        # Calcular el centro del grupo de vértices usando bounding box
        bbox = cmds.exactWorldBoundingBox(verts)
        centro = [
            (bbox[0] + bbox[3]) / 2.0,
            (bbox[1] + bbox[4]) / 2.0,
            (bbox[2] + bbox[5]) / 2.0,
        ]

        # Aplicar la escala
        cmds.xform(verts, scale=escala_final, ws=True, pivots=centro)

        print(f"[✓] {parte}: {set_name} escalado {escala_final} (factor {factor:.3f})")

    cmds.select(clear=True)
