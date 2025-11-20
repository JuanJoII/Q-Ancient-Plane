import maya.cmds as cmds

def crear_control_avion():
    partes_avion = [
        "FUSELAJE_GENERADO",
        "ALAS_GENERADO",
        "COLA_GENERADO",
        "CABEZA_GENERADO",
        "ORNAMENTACION_GENERADO"
    ]

    partes_existentes = [p for p in partes_avion if cmds.objExists(p)]
    if not partes_existentes:
        cmds.warning("No se encontró ninguna parte del avión en la escena.")
        return

    control = cmds.circle(
        name="CTRL_Avion",
        normal=[0, 1, 0],
        radius=5
    )[0]

    grupo = cmds.group(control, name="ROOT_CTRL_Avion")

    centros = []
    for parte in partes_existentes:
        bbox = cmds.exactWorldBoundingBox(parte)
        centro = [
            (bbox[0] + bbox[3]) / 2.0,
            (bbox[1] + bbox[4]) / 2.0,
            (bbox[2] + bbox[5]) / 2.0
        ]
        centros.append(centro)

    centro_avion = [
        sum(c[0] for c in centros) / len(centros),
        sum(c[1] for c in centros) / len(centros),
        sum(c[2] for c in centros) / len(centros)
    ]

    cmds.xform(grupo, ws=True, t=centro_avion)

    cmds.makeIdentity(control, apply=True, translate=True, rotate=True, scale=True)

    # Constraints
    for parte in partes_existentes:
        cmds.parentConstraint(control, parte, mo=True)

    cmds.select(control)
    print("Control creado, transformaciones en cero y asignado correctamente.")


if __name__ == '__main__':
    crear_control_avion()