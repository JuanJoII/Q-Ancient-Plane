import maya.cmds as cmds


def eliminar_residuos():
    """
    Elimina TODO lo que no sea un transform con sufijo '_GENERADO'
    """
    generados = cmds.ls("*_GENERADO", type="transform")
    generados_nombres = [g.split("|")[-1] for g in generados] if generados else []

    todos = cmds.ls(type="transform", long=True)
    a_eliminar = []

    for obj in todos:
        nombre = obj.split("|")[-1]
        if nombre not in generados_nombres:
            a_eliminar.append(obj)

    if a_eliminar:
        try:
            cmds.delete(a_eliminar)
            print(f"Eliminados {len(a_eliminar)} objetos residuales")
        except:
            pass
