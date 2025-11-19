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

def aplicar_material_montanas(objeto, nombre_material="M_Montanas"):
    """
    Crea un material aiStandardSurface con variación verde y AO para simular montañas realistas.
    """
    if not cmds.objExists(objeto):
        cmds.warning(f"El objeto '{objeto}' no existe.")
        return

    # Crear material si no existe
    if not cmds.objExists(nombre_material):
        shader = cmds.shadingNode("aiStandardSurface", asShader=True, name=nombre_material)
        sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=nombre_material + "SG")
        cmds.connectAttr(shader + ".outColor", sg + ".surfaceShader", force=True)

        # === Ramp de color base (verde con variaciones) ===
        ramp = cmds.shadingNode("ramp", asTexture=True, name=nombre_material + "_ramp")
        place2d = cmds.shadingNode("place2dTexture", asUtility=True)
        cmds.connectAttr(place2d + ".outUV", ramp + ".uvCoord")

        cmds.setAttr(ramp + ".type", 1)  # Circular para más orgánico
        cmds.setAttr(ramp + ".colorEntryList[0].color", 0.05, 0.18, 0.05, type="double3")  # Verde oscuro
        cmds.setAttr(ramp + ".colorEntryList[0].position", 0.0)
        cmds.setAttr(ramp + ".colorEntryList[1].color", 0.2, 0.4, 0.15, type="double3")    # Verde medio
        cmds.setAttr(ramp + ".colorEntryList[1].position", 0.5)
        cmds.setAttr(ramp + ".colorEntryList[2].color", 0.4, 0.6, 0.25, type="double3")    # Verde claro
        cmds.setAttr(ramp + ".colorEntryList[2].position", 1.0)

        # === Ruido para variar el color del terreno ===
        noise = cmds.shadingNode("aiNoise", asTexture=True, name=nombre_material + "_noise")
        cmds.setAttr(noise + ".scaleX", 3)
        cmds.setAttr(noise + ".scaleY", 3)
        cmds.setAttr(noise + ".scaleZ", 3)
        cmds.setAttr(noise + ".octaves", 5)
        cmds.setAttr(noise + ".amplitude", 0.7)
        cmds.setAttr(noise + ".distortion", 0.2)

        # Mezcla de ramp + noise para más detalle
        mix = cmds.shadingNode("aiMixShader", asShader=True, name=nombre_material + "_mixColor")
        cmds.connectAttr(ramp + ".outColor", mix + ".shader1")
        cmds.connectAttr(noise + ".outColor", mix + ".shader2")
        cmds.setAttr(mix + ".mix", 0.4)

        # === Ambient Occlusion ===
        ao = cmds.shadingNode("aiAmbientOcclusion", asShader=True, name=nombre_material + "_AO")
        cmds.setAttr(ao + ".samples", 16)
        cmds.setAttr(ao + ".spread", 0.8)
        cmds.setAttr(ao + ".falloff", 1.0)

        # Mezclar color base con AO
        layer = cmds.shadingNode("aiMixShader", asShader=True, name=nombre_material + "_finalMix")
        cmds.connectAttr(mix + ".outColor", layer + ".shader1")  # base color
        cmds.connectAttr(ao + ".outColor", layer + ".shader2")   # AO
        cmds.setAttr(layer + ".mix", 0.25)

        # Conectar color al material final
        cmds.connectAttr(layer + ".outColor", shader + ".baseColor")

        # === Ajustes físicos del material ===
        cmds.setAttr(shader + ".specular", 0.15)
        cmds.setAttr(shader + ".specularRoughness", 0.85)
        cmds.setAttr(shader + ".subsurface", 0.1)  # leve dispersión
        cmds.setAttr(shader + ".subsurfaceRadius", 0.2, 0.25, 0.2, type="double3")
        cmds.setAttr(shader + ".subsurfaceColor", 0.25, 0.4, 0.25, type="double3")

        # === Displacement para relieve ===
        displace = cmds.shadingNode("displacementShader", asShader=True, name=nombre_material + "_disp")
        cmds.connectAttr(noise + ".outColorR", displace + ".displacement")
        cmds.connectAttr(displace + ".displacement", sg + ".displacementShader", force=True)
        cmds.setAttr(noise + ".scale", 10)
    
    # === Asignar el material a la geometría ===
    sg = nombre_material + "SG"
    meshes = cmds.listRelatives(objeto, allDescendents=True, type="mesh", fullPath=True) or []
    if not meshes:
        shape = cmds.listRelatives(objeto, shapes=True, type="mesh", fullPath=True)
        if shape:
            meshes = shape

    if not meshes:
        cmds.warning(f"No se encontraron mallas dentro de '{objeto}'.")
        return

    for mesh in meshes:
        cmds.sets(mesh, e=True, forceElement=sg)

    print(f"[✓] Material mejorado de montañas aplicado a '{objeto}'.")
    
def aplicar_material_nubes(objeto, nombre_material="M_Nubes"):
    """
    Crea un material tipo nube con aiNoise procedural
    y lo aplica al objeto indicado.
    """
    if not cmds.objExists(objeto):
        cmds.warning(f"El objeto '{objeto}' no existe.")
        return

    if not cmds.objExists(nombre_material):
        # Crear shader y shading group
        shader = cmds.shadingNode("aiStandardSurface", asShader=True, name=nombre_material)
        sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=nombre_material + "SG")
        cmds.connectAttr(shader + ".outColor", sg + ".surfaceShader", force=True)

        # Crear aiNoise
        noise = cmds.shadingNode("aiNoise", asTexture=True, name=nombre_material + "_noise")

        # --- Ajustes aiNoise ---
        cmds.setAttr(noise + ".octaves", 4)
        cmds.setAttr(noise + ".distortion", 3.0)
        cmds.setAttr(noise + ".lacunarity", 1.7)
        cmds.setAttr(noise + ".amplitude", 1.0)
        cmds.setAttr(noise + ".scaleX", 3.0)
        cmds.setAttr(noise + ".scaleY", 3.0)
        cmds.setAttr(noise + ".scaleZ", 3.0)
        cmds.setAttr(noise + ".color1", 0.7, 0.8, 1.0, type="double3")  # azul muy claro
        cmds.setAttr(noise + ".color2", 1.0, 1.0, 1.0, type="double3")  # blanco
        cmds.setAttr(noise + ".coordSpace", 1)

        # --- Ajustes shader ---
        cmds.setAttr(shader + ".specular", 0.2)
        cmds.setAttr(shader + ".specularRoughness", 0.6)
        cmds.setAttr(shader + ".transmission", 0.3)
        cmds.setAttr(shader + ".subsurface", 0.45)
        cmds.setAttr(shader + ".subsurfaceType", 1)
        cmds.setAttr(shader + ".subsurfaceColor", 1, 1, 1, type="double3")
        cmds.setAttr(shader + ".emission", 0.15)
        cmds.setAttr(shader + ".emissionColor", 0.9, 0.95, 1.0, type="double3")

        # Conectar aiNoise
        cmds.connectAttr(noise + ".outColor", shader + ".transmissionColor", force=True)
        cmds.connectAttr(noise + ".outColor", shader + ".emissionColor", force=True)

    sg = nombre_material + "SG"

    # Buscar todas las mallas dentro del objeto (grupo de nubes)
    meshes = cmds.listRelatives(objeto, allDescendents=True, type="mesh", fullPath=True) or []
    if not meshes:
        cmds.warning(f"No se encontraron mallas dentro de '{objeto}'.")
        return

    for mesh in meshes:
        cmds.sets(mesh, e=True, forceElement=sg)

    print(f"[☁️] Material '{nombre_material}' aplicado a todas las mallas dentro de '{objeto}'.")

if __name__ == '__main__':
    aplicar_material_oro()
    aplicar_material_nubes()
    aplicar_material_montanas()