import os, json, random
import maya.cmds as cmds

CARPETA_MODELOS = r"C:\Users\STEF\Documents\Universidad\09_Noveno_Semestre\TechnicalArt\PF_AvionesQuimbaya\modelos"
CONFIG_JSON = r"C:\Users\STEF\Documents\Universidad\09_Noveno_Semestre\TechnicalArt\PF_AvionesQuimbaya\Q-Ancient-Plane\axiomas\plane_config.json"

with open(CONFIG_JSON, 'r') as f:
    CONFIG = json.load(f)

COLORES_PARTES = {
    "FUSELAJE": [0.7, 0.7, 0.8],      # Gris azulado
    "ALAS": [0.85, 0.85, 0.9],         # Gris claro
    "CABEZA": [0.9, 0.75, 0.6],        # Beige/crema
    "COLA": [0.8, 0.65, 0.5],          # Marrón claro
    "ORNAMENTACION": [0.9, 0.8, 0.3]   # Dorado
}

def crear_y_asignar_material(obj, parte):
    """
    Crea un material Lambert y lo asigna al objeto
    """
    nombre_material = f"MAT_{parte}"
    nombre_sg = f"{nombre_material}_SG"
    
    # Verificar si el material ya existe, si no crearlo
    if not cmds.objExists(nombre_material):
        material = cmds.shadingNode('lambert', asShader=True, name=nombre_material)
        shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=nombre_sg)
        cmds.connectAttr(f"{material}.outColor", f"{shading_group}.surfaceShader", force=True)
        
        # Asignar color predeterminado
        color = COLORES_PARTES.get(parte, [0.5, 0.5, 0.5])
        cmds.setAttr(f"{material}.color", *color, type="double3")
        print(f"Material {nombre_material} creado con color {color}")
    else:
        shading_group = nombre_sg
        print(f"Material {nombre_material} ya existe, reutilizando")
    
    # Asignar el material al objeto
    cmds.select(obj)
    cmds.hyperShade(assign=nombre_material)
    print(f"Material {nombre_material} asignado a {obj}")

def obtener_variantes(parte):
    prefijo = parte.lower() + "_QAP_"
    return [f for f in os.listdir(CARPETA_MODELOS) if f.startswith(prefijo) and f.endswith(".obj")]

def generar_parte(parte):
    variantes = obtener_variantes(parte)
    if not variantes:
        cmds.warning(f"No se encontraron modelos para {parte}")
        return

    # Si ya existe una versión generada de esta parte, eliminarla antes de importar la nueva
    nombre_existente = f"{parte}_GENERADO"
    if cmds.objExists(nombre_existente):
        cmds.delete(nombre_existente)
        print(f"Se eliminó la versión anterior de {parte}")

    # Importar el nuevo modelo
    archivo = random.choice(variantes)
    ruta = os.path.join(CARPETA_MODELOS, archivo)

    antes = set(cmds.ls(assemblies=True))
    cmds.file(ruta, i=True, type="OBJ", ignoreVersion=True, ra=True, mergeNamespacesOnClash=False, options="mo=1", pr=True)
    despues = set(cmds.ls(assemblies=True))
    nuevos = list(despues - antes)

    if not nuevos:
        cmds.warning(f"No se detectó objeto tras importar {archivo}")
        return

    obj = nuevos[0]

    # Corregir normales
    cmds.polyNormal(obj, normalMode=0, userNormalMode=0, ch=False)

    # Aplicar transformaciones
    data = CONFIG[parte]
    cmds.move(*data["posicion"], obj)
    cmds.rotate(*data["rotacion"], obj)
    cmds.scale(*data["escala"], obj)

    # Renombrar el objeto generado
    cmds.rename(obj, nombre_existente)
    print(f"{parte} generado desde {archivo}")
