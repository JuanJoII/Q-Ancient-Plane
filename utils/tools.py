import os
import random
import maya.cmds as cmds
from Utils.config import CARPETA_MODELOS, CONFIG


def obtener_variantes(parte):
    prefijo = parte.lower() + "_QAP_"
    return [
        f
        for f in os.listdir(CARPETA_MODELOS)
        if f.startswith(prefijo) and f.endswith(".ma")
    ]

def corregir_normales_forzado(objeto):
    """Corrige normales y winding de todas las mallas dentro del objeto."""
    if not cmds.objExists(objeto):
        cmds.warning(f"El objeto '{objeto}' no existe.")
        return

    meshes = cmds.listRelatives(objeto, allDescendents=True, type="mesh", fullPath=True) or []
    if not meshes:
        cmds.warning(f"No se encontraron meshes dentro de '{objeto}'.")
        return

    for mesh in meshes:
        parent = cmds.listRelatives(mesh, parent=True, fullPath=True)[0]
        cmds.makeIdentity(parent, apply=True, translate=True, rotate=True, scale=True)
        cmds.delete(parent, ch=True)
        cmds.polyNormalPerVertex(mesh, unFreezeNormal=True)
        cmds.polyNormal(mesh, normalMode=2, userNormalMode=0, ch=False)
        cmds.polySoftEdge(mesh, angle=180, ch=False)

    cmds.select(clear=True)



def generar_parte(parte, manejar_locators=True):
    variantes = obtener_variantes(parte)
    if not variantes:
        cmds.warning(f"No se encontraron modelos para {parte}")
        return

    nombre_existente = f"{parte}_GENERADO"
    if cmds.objExists(nombre_existente):
        cmds.delete(nombre_existente)
        print(f"Se eliminó la versión anterior de {parte}")

    archivo = random.choice(variantes)
    ruta = os.path.join(CARPETA_MODELOS, archivo)

    antes = set(cmds.ls(assemblies=True))
    cmds.file(
        ruta, i=True, type="mayaAscii", ignoreVersion=True, ra=True,
        mergeNamespacesOnClash=False, options="v=0;", pr=True
    )
    despues = set(cmds.ls(assemblies=True))
    nuevos = list(despues - antes)

    if not nuevos:
        cmds.warning(f"No se detectó objeto tras importar {archivo}")
        return

    # Agrupar todo lo importado bajo un mismo grupo
    grupo = cmds.group(nuevos, n=nombre_existente)
    print(f"[✓] {parte} importado desde {archivo} con {len(nuevos)} nodos")

    # Si manejar_locators=True, preservar locators y no aplicarles transformaciones
    if manejar_locators:
        locators = cmds.ls(f"{nombre_existente}|*LOC*", type="transform")
        if locators:
            print(f"[i] {len(locators)} locators detectados en {parte}: {locators}")
        else:
            print(f"[i] No se detectaron locators en {parte}")
    else:
        # Eliminar locators si no se van a usar
        locs = cmds.ls(f"{nombre_existente}|*LOC*", type="transform")
        if locs:
            cmds.delete(locs)
            print(f"[i] Locators eliminados de {parte}")

    data = CONFIG.get(parte, {})
    cmds.move(*data.get("posicion", [0, 0, 0]), grupo)
    cmds.rotate(*data.get("rotacion", [0, 0, 0]), grupo)
    cmds.scale(*data.get("escala", [1, 1, 1]), grupo)

    corregir_normales_forzado(grupo)

    print(f"[✓] {parte} generado correctamente con forzado aplicado")
    return grupo
