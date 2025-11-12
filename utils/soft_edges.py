import maya.cmds as cmds

def soften_edges_en_grupo(nombre_grupo, angle=180, keep_history=False, verbose=True):
    """
    Aplica polySoftEdge a todas las mallas dentro de un grupo.
    """
    grupos = cmds.ls(nombre_grupo, long=True) or []
    if not grupos:
        if verbose:
            cmds.warning(f"No se encontró ningún nodo que coincida con '{nombre_grupo}'.")
        return []

    applied = []
    for grp in grupos:
        meshes = cmds.listRelatives(grp, allDescendents=True, type='mesh', fullPath=True) or []
        if not meshes:
            if verbose:
                cmds.warning(f"El grupo '{grp}' no contiene mallas (meshes).")
            continue

        transforms = []
        for mesh in meshes:
            parents = cmds.listRelatives(mesh, parent=True, fullPath=True) or []
            for p in parents:
                if p not in transforms:
                    transforms.append(p)

        for t in transforms:
            try:
                cmds.polySoftEdge(t, angle=angle, ch=keep_history)
                applied.append(t)
                if verbose:
                    print(f"Soften edge aplicado a: {t}")
            except Exception as e:
                cmds.warning(f"No se pudo aplicar soften edge a {t}: {e}")

    if verbose:
        print(f"Soften edge aplicado a {len(applied)} objeto(s).")
    return applied