import os, json, random
from dotenv import load_dotenv
import maya.cmds as cmds

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)

CARPETA_MODELOS: str = os.getenv("CARPETA_MODELOS")
CONFIG_JSON: str = os.getenv("CONFIG_JSON")

with open(CONFIG_JSON, 'r') as f:
    CONFIG = json.load(f)

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
