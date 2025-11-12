import maya.cmds as cmds

def aplicar_material_oro(objeto, nombre_material="M_Gold"):
    """
    Crea un material tipo 'gold' (AI Standard Surface) y lo aplica
    a todas las mallas dentro del objeto indicado (sin importar jerarquía).
    """
    if not cmds.objExists(objeto):
        cmds.warning(f"El objeto '{objeto}' no existe.")
        return

    # Crear material si no existe
    if not cmds.objExists(nombre_material):
        shader = cmds.shadingNode("aiStandardSurface", asShader=True, name=nombre_material)
        sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=nombre_material + "SG")
        cmds.connectAttr(shader + ".outColor", sg + ".surfaceShader", force=True)

        # --- Preset oro ---
        cmds.setAttr(shader + ".baseColor", 0.9, 0.7, 0.2, type="double3")
        cmds.setAttr(shader + ".metalness", 1.0)
        cmds.setAttr(shader + ".specularRoughness", 0.3)
        cmds.setAttr(shader + ".specularIOR", 1.45)
        cmds.setAttr(shader + ".specularColor", 1.0, 0.9, 0.7, type="double3")

    sg = nombre_material + "SG"

    # Obtener TODAS las formas de malla (shape nodes)
    meshes = cmds.listRelatives(objeto, allDescendents=True, type="mesh", fullPath=True) or []
    if not meshes:
        cmds.warning(f"No se encontraron mallas dentro de '{objeto}'.")
        return

    # Aplicar material a TODAS las mallas encontradas
    for mesh in meshes:
        cmds.sets(mesh, e=True, forceElement=sg)

    print(f"[✓] Material '{nombre_material}' aplicado a todas las mallas dentro de '{objeto}'.")
