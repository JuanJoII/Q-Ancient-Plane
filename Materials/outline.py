import maya.cmds as cmds
import maya.mel as mel
import colorsys

def aplicar_outline_toon(objetos, ancho_linea=0.02):
    """
    Aplica toon outline a objetos, lo convierte a polígonos y elimina los strokes originales.
    Compatible con Maya 2023-2025.
    """
    if not objetos:
        cmds.warning("[!] No hay objetos para aplicar outline.")
        return

    outline_meshes = []

    # Crear material negro para el outline si no existe
    shader_name = "M_Outline"
    sg_name = "M_OutlineSG"

    if not cmds.objExists(shader_name):
        shader = cmds.shadingNode("lambert", asShader=True, name=shader_name)
        sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=sg_name)
        cmds.connectAttr(f"{shader}.outColor", f"{sg}.surfaceShader", force=True)
        cmds.setAttr(f"{shader}.color", 0, 0, 0, type="double3")
        cmds.setAttr(f"{shader}.incandescence", 0, 0, 0, type="double3")

    for obj in objetos:
        if not cmds.objExists(obj):
            cmds.warning(f"[!] No existe el objeto {obj}")
            continue

        print(f"🎨 Procesando: {obj}")
        cmds.select(obj, r=True)

        # Crear pfxToon moderno (Maya 2025)
        try:
            mel.eval('assignNewPfxToon;')
        except Exception as e:
            cmds.warning(f"[!] Error al crear pfxToon para {obj}: {e}")
            continue

        # Buscar el pfxToon recién creado
        pfx_toon = cmds.listConnections(obj, type="pfxToon")
        if not pfx_toon:
            cmds.warning(f"⚠️ No se encontró pfxToon para {obj}")
            continue

        pfx_toon = pfx_toon[0]
        print(f"✓ pfxToon creado: {pfx_toon}")

        # Ajustar parámetros del outline
        cmds.setAttr(f"{pfx_toon}.lineWidth", ancho_linea)
        cmds.setAttr(f"{pfx_toon}.profileLines", 1)
        cmds.setAttr(f"{pfx_toon}.creaseLines", 0)
        cmds.setAttr(f"{pfx_toon}.borderLines", 1)

        # Buscar strokes conectados al pfxToon
        strokes = cmds.listConnections(pfx_toon, type="stroke")
        if not strokes:
            cmds.warning(f"⚠️ No se encontraron strokes para {pfx_toon}")
            continue

        for stroke in strokes:
            print(f"🔄 Convirtiendo stroke: {stroke}")
            cmds.select(stroke, r=True)

            try:
                # Convertir a polígonos (mantiene detalles y suavizado)
                mel.eval('doPaintEffectsToPoly(1, 1, 1, 1, 100000);')
            except Exception as e:
                cmds.warning(f"[!] Error convirtiendo stroke {stroke}: {e}")
                continue

            # Buscar el último mesh creado
            new_meshes = cmds.ls(sl=True, type="transform")
            if not new_meshes:
                cmds.warning(f"⚠️ No se creó ningún mesh para {stroke}")
                continue

            new_mesh = new_meshes[-1]
            renamed_mesh = cmds.rename(new_mesh, f"{obj}_outline")
            outline_meshes.append(renamed_mesh)

            # Asignar material
            cmds.select(renamed_mesh, r=True)
            cmds.hyperShade(assign=sg_name)

            print(f"✅ Outline convertido y renombrado: {renamed_mesh}")

    # Agrupar outlines
    if outline_meshes:
        if not cmds.objExists("OUTLINES_GROUP"):
            cmds.group(outline_meshes, name="OUTLINES_GROUP")
        else:
            cmds.parent(outline_meshes, "OUTLINES_GROUP")
        print(f"✅ Total de outlines creados: {len(outline_meshes)}")
    else:
        print("⚠️ No se crearon meshes de outline.")

    cmds.select(cl=True)


def aplicar_shader_outline(mesh, color_rgb):
    """
    Aplica un shader lambert negro al mesh del outline.
    """
    shader_name = "M_Outline"
    sg_name = "M_OutlineSG"

    # Crear material si no existe
    if not cmds.objExists(shader_name):
        shader = cmds.shadingNode("lambert", asShader=True, name=shader_name)
        sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=sg_name)
        cmds.connectAttr(f"{shader}.outColor", f"{sg}.surfaceShader", force=True)
    else:
        shader = shader_name
        sg = sg_name

    r, g, b = color_rgb
    cmds.setAttr(f"{shader}.color", r, g, b, type="double3")
    cmds.setAttr(f"{shader}.incandescence", r, g, b, type="double3")

    cmds.sets(mesh, edit=True, forceElement=sg)
    print(f"🎨 Shader '{shader_name}' aplicado a {mesh}")


def ajustar_color_outline(h, s, v, nombre_material="M_Outline"):
    """
    Ajusta el color del outline en tiempo real según valores HSV.
    """
    if not cmds.objExists(nombre_material):
        cmds.warning(f"[!] No se encontró el material '{nombre_material}'. Aplica el outline primero.")
        return

    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    cmds.setAttr(f"{nombre_material}.color", r, g, b, type="double3")
    cmds.setAttr(f"{nombre_material}.incandescence", r, g, b, type="double3")
    print(f"✓ Color del outline actualizado: RGB({r:.2f}, {g:.2f}, {b:.2f})")


def ajustar_grosor_outline(ancho_linea):
    """
    Ajusta el grosor del outline escalando los meshes dentro del grupo OUTLINES_GROUP.
    """
    if not cmds.objExists("OUTLINES_GROUP"):
        cmds.warning("[!] No existe el grupo OUTLINES_GROUP. Aplica el outline primero.")
        return

    outlines = cmds.listRelatives("OUTLINES_GROUP", children=True, type="transform") or []

    for outline in outlines:
        escala = 1.0 + (ancho_linea * 10)
        cmds.setAttr(f"{outline}.scaleX", escala)
        cmds.setAttr(f"{outline}.scaleY", escala)
        cmds.setAttr(f"{outline}.scaleZ", escala)

    print(f"✓ Grosor del outline actualizado: {ancho_linea}")
