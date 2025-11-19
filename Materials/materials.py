import maya.cmds as cmds
import random

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


def aplicar_material_montanas(objeto, nombre_material="M_Montanas_Metalico"):
    """
    Crea un material aiStandardSurface METÁLICO con variación de color y contraste.
    """
    if not cmds.objExists(objeto):
        cmds.warning(f"El objeto '{objeto}' no existe.")
        return

    # Crear material si no existe
    if not cmds.objExists(nombre_material):
        shader = cmds.shadingNode("aiStandardSurface", asShader=True, name=nombre_material)
        sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=nombre_material + "SG")
        cmds.connectAttr(shader + ".outColor", sg + ".surfaceShader", force=True)

        # === PROPIEDADES METÁLICAS ===
        cmds.setAttr(shader + ".metalness", 0.9)  # ALTO metalness para look metálico
        cmds.setAttr(shader + ".specular", 1.0)
        cmds.setAttr(shader + ".specularRoughness", 0.3)  # Reflejo más definido
        cmds.setAttr(shader + ".specularIOR", 1.5)

        # === Ramp de color base (metálico con variaciones) ===
        ramp = cmds.shadingNode("ramp", asTexture=True, name=nombre_material + "_ramp")
        place2d = cmds.shadingNode("place2dTexture", asUtility=True, name=nombre_material + "_place2d")
        cmds.connectAttr(place2d + ".outUV", ramp + ".uvCoord")

        cmds.setAttr(ramp + ".type", 1)  # Circular
        # Colores metálicos por defecto (bronce/cobre oscuro)
        cmds.setAttr(ramp + ".colorEntryList[0].color", 0.15, 0.12, 0.08, type="double3")  # Oscuro
        cmds.setAttr(ramp + ".colorEntryList[0].position", 0.0)
        cmds.setAttr(ramp + ".colorEntryList[1].color", 0.4, 0.3, 0.2, type="double3")      # Medio
        cmds.setAttr(ramp + ".colorEntryList[1].position", 0.5)
        cmds.setAttr(ramp + ".colorEntryList[2].color", 0.6, 0.5, 0.35, type="double3")     # Claro
        cmds.setAttr(ramp + ".colorEntryList[2].position", 1.0)

        # === Ruido para textura metálica ===
        noise = cmds.shadingNode("aiNoise", asTexture=True, name=nombre_material + "_noise")
        cmds.setAttr(noise + ".scaleX", 5)
        cmds.setAttr(noise + ".scaleY", 5)
        cmds.setAttr(noise + ".scaleZ", 5)
        cmds.setAttr(noise + ".octaves", 6)
        cmds.setAttr(noise + ".amplitude", 0.8)
        cmds.setAttr(noise + ".distortion", 0.3)

        # === Fractal para detalles adicionales (contraste) ===
        fractal = cmds.shadingNode("aiNoise", asTexture=True, name=nombre_material + "_fractal")
        cmds.setAttr(fractal + ".scaleX", 15)
        cmds.setAttr(fractal + ".scaleY", 15)
        cmds.setAttr(fractal + ".scaleZ", 15)
        cmds.setAttr(fractal + ".octaves", 4)
        cmds.setAttr(fractal + ".amplitude", 0.5)

        # Mezclar ruido + fractal para más contraste
        layered = cmds.shadingNode("layeredTexture", asTexture=True, name=nombre_material + "_layered")
        cmds.connectAttr(noise + ".outColor", layered + ".inputs[0].color")
        cmds.connectAttr(fractal + ".outColor", layered + ".inputs[1].color")
        cmds.setAttr(layered + ".inputs[1].blendMode", 6)  # Multiply para contraste

        # Multiplicar ramp por textura procedural
        multiply = cmds.shadingNode("multiplyDivide", asUtility=True, name=nombre_material + "_multiply")
        cmds.connectAttr(ramp + ".outColor", multiply + ".input1")
        cmds.connectAttr(layered + ".outColor", multiply + ".input2")

        # === Ambient Occlusion para sombras en crevices ===
        ao = cmds.shadingNode("aiAmbientOcclusion", asShader=True, name=nombre_material + "_AO")
        cmds.setAttr(ao + ".samples", 20)
        cmds.setAttr(ao + ".spread", 0.9)
        cmds.setAttr(ao + ".falloff", 0.8)

        # Mezclar color con AO
        mix_ao = cmds.shadingNode("blendColors", asUtility=True, name=nombre_material + "_mixAO")
        cmds.connectAttr(multiply + ".output", mix_ao + ".color1")
        cmds.connectAttr(ao + ".outColor", mix_ao + ".color2")
        cmds.setAttr(mix_ao + ".blender", 0.35)

        # Conectar al material
        cmds.connectAttr(mix_ao + ".output", shader + ".baseColor")

        # === Roughness variation para brillo variable ===
        roughness_noise = cmds.shadingNode("aiNoise", asTexture=True, name=nombre_material + "_roughness")
        cmds.setAttr(roughness_noise + ".scaleX", 8)
        cmds.setAttr(roughness_noise + ".scaleY", 8)
        cmds.setAttr(roughness_noise + ".scaleZ", 8)
        cmds.setAttr(roughness_noise + ".octaves", 3)
        
        remap = cmds.shadingNode("remapValue", asUtility=True, name=nombre_material + "_remap")
        cmds.connectAttr(roughness_noise + ".outColorR", remap + ".inputValue")
        cmds.setAttr(remap + ".inputMin", 0.0)
        cmds.setAttr(remap + ".inputMax", 1.0)
        cmds.setAttr(remap + ".outputMin", 0.2)
        cmds.setAttr(remap + ".outputMax", 0.5)
        cmds.connectAttr(remap + ".outValue", shader + ".specularRoughness")

        # === Displacement para relieve ===
        displace = cmds.shadingNode("displacementShader", asShader=True, name=nombre_material + "_disp")
        cmds.connectAttr(noise + ".outColorR", displace + ".displacement")
        cmds.connectAttr(displace + ".displacement", sg + ".displacementShader", force=True)
        cmds.setAttr(displace + ".scale", 0.5)
    
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

    print(f"[✓] Material metálico de montañas aplicado a '{objeto}'.")


def cambiar_color_montanas_aleatorio(nombre_material="M_Montanas_Metalico"):
    """
    Cambia el color del material de las montañas de forma aleatoria entre paletas metálicas.
    """
    if not cmds.objExists(nombre_material):
        cmds.warning(f"El material '{nombre_material}' no existe. Crea el material primero.")
        return
    
    # Paletas de colores metálicos predefinidas
    paletas = [
        # Cobre/Bronce
        [(0.15, 0.12, 0.08), (0.4, 0.3, 0.2), (0.6, 0.5, 0.35)],
        # Hierro/Acero
        [(0.15, 0.15, 0.18), (0.35, 0.35, 0.40), (0.55, 0.55, 0.60)],
        # Oro Viejo
        [(0.25, 0.20, 0.08), (0.50, 0.42, 0.18), (0.70, 0.60, 0.30)],
        # Plata Oscura
        [(0.20, 0.22, 0.25), (0.45, 0.48, 0.52), (0.65, 0.68, 0.72)],
        # Bronce Verde (oxidado)
        [(0.12, 0.18, 0.15), (0.25, 0.40, 0.32), (0.40, 0.55, 0.45)],
        # Titanio
        [(0.18, 0.18, 0.20), (0.38, 0.38, 0.42), (0.58, 0.58, 0.65)],
        # Cobre Rojizo
        [(0.20, 0.10, 0.08), (0.45, 0.22, 0.15), (0.65, 0.35, 0.25)],
    ]
    
    # Seleccionar paleta aleatoria
    paleta = random.choice(paletas)
    
    ramp_name = nombre_material + "_ramp"
    if cmds.objExists(ramp_name):
        cmds.setAttr(ramp_name + ".colorEntryList[0].color", *paleta[0], type="double3")
        cmds.setAttr(ramp_name + ".colorEntryList[1].color", *paleta[1], type="double3")
        cmds.setAttr(ramp_name + ".colorEntryList[2].color", *paleta[2], type="double3")
        
        print(f"[✓] Color de montañas cambiado aleatoriamente a paleta metálica.")
    else:
        cmds.warning(f"No se encontró el ramp '{ramp_name}'.")


def aplicar_material_nubes(objeto, nombre_material="M_Nubes_Metalico"):
    """
    Crea un material metálico para las nubes (cubos biselados)
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

        # Crear aiNoise para textura procedural
        noise = cmds.shadingNode("aiNoise", asTexture=True, name=nombre_material + "_noise")

        # --- Ajustes aiNoise para textura metálica ---
        cmds.setAttr(noise + ".octaves", 6)
        cmds.setAttr(noise + ".distortion", 1.5)
        cmds.setAttr(noise + ".lacunarity", 2.2)
        cmds.setAttr(noise + ".amplitude", 1.0)
        cmds.setAttr(noise + ".scaleX", 2.0)
        cmds.setAttr(noise + ".scaleY", 2.0)
        cmds.setAttr(noise + ".scaleZ", 2.0)
        cmds.setAttr(noise + ".color1", 0.6, 0.65, 0.7, type="double3")  # gris metálico oscuro
        cmds.setAttr(noise + ".color2", 0.85, 0.88, 0.9, type="double3")  # gris metálico claro
        cmds.setAttr(noise + ".coordSpace", 1)  # object space

        # Crear un ramp para controlar la rugosidad
        ramp_roughness = cmds.shadingNode("ramp", asTexture=True, name=nombre_material + "_roughness_ramp")
        cmds.setAttr(ramp_roughness + ".colorEntryList[0].position", 0.0)
        cmds.setAttr(ramp_roughness + ".colorEntryList[0].color", 0.2, 0.2, 0.2, type="double3")
        cmds.setAttr(ramp_roughness + ".colorEntryList[1].position", 1.0)
        cmds.setAttr(ramp_roughness + ".colorEntryList[1].color", 0.4, 0.4, 0.4, type="double3")

        # --- Ajustes shader METÁLICO ---
        cmds.setAttr(shader + ".metalness", 0.95)  # Alto metalness para efecto metálico
        cmds.setAttr(shader + ".specular", 1.0)    # Especular alto
        cmds.setAttr(shader + ".specularRoughness", 0.25)  # Baja rugosidad para reflejos
        cmds.setAttr(shader + ".specularIOR", 1.5)
        
        # Color base metálico
        cmds.setAttr(shader + ".baseColor", 0.7, 0.75, 0.8, type="double3")
        
        # Anisotropía para efecto metálico cepillado (opcional)
        cmds.setAttr(shader + ".specularAnisotropy", 0.3)
        cmds.setAttr(shader + ".specularRotation", 0.25)
        
        # Subsurface desactivado (no aplica para metal)
        cmds.setAttr(shader + ".subsurface", 0.0)
        cmds.setAttr(shader + ".transmission", 0.0)
        
        # Pequeña emisión para darle vida
        cmds.setAttr(shader + ".emission", 0.05)
        cmds.setAttr(shader + ".emissionColor", 0.7, 0.75, 0.8, type="double3")

        # Conectar aiNoise al color base para variación
        cmds.connectAttr(noise + ".outColor", shader + ".baseColor", force=True)
        
        # Conectar ramp a roughness para variación (opcional)
        # cmds.connectAttr(ramp_roughness + ".outColorR", shader + ".specularRoughness", force=True)

    sg = nombre_material + "SG"

    # Buscar todas las mallas dentro del objeto (grupo de nubes)
    meshes = cmds.listRelatives(objeto, allDescendents=True, type="mesh", fullPath=True) or []
    if not meshes:
        cmds.warning(f"No se encontraron mallas dentro de '{objeto}'.")
        return

    for mesh in meshes:
        cmds.sets(mesh, e=True, forceElement=sg)

    print(f"[⚙️] Material metálico '{nombre_material}' aplicado a todas las mallas dentro de '{objeto}'.")

if __name__ == '__main__':
    aplicar_material_oro()
    aplicar_material_nubes()
    aplicar_material_montanas()