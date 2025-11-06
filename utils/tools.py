import os
import random
import maya.cmds as cmds
from utils.config import CARPETA_MODELOS, CONFIG
from utils.deform import aplicar_deformaciones


def obtener_variantes(parte):
    prefijo = parte.lower() + "_QAP_"
    return [
        f
        for f in os.listdir(CARPETA_MODELOS)
        if f.startswith(prefijo) and f.endswith(".ma")
    ]


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
    cmds.file(ruta, i=True, type="mayaAscii", ignoreVersion=True, ra=True,
              mergeNamespacesOnClash=False, options="v=0;", pr=True)
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

    # Aplicar transformaciones al grupo principal
    data = CONFIG[parte]
    cmds.move(*data.get("posicion", [0, 0, 0]), grupo)
    cmds.rotate(*data.get("rotacion", [0, 0, 0]), grupo)
    cmds.scale(*data.get("escala", [1, 1, 1]), grupo)

    # Corregir normales (solo para geometrías)
    for nodo in nuevos:
        if cmds.nodeType(nodo) == "transform":
            shapes = cmds.listRelatives(nodo, shapes=True) or []
            if any("mesh" in cmds.nodeType(s) for s in shapes):
                try:
                    cmds.polyNormal(nodo, normalMode=0, userNormalMode=0, ch=False)
                except:
                    pass

    print(f"[✓] {parte} generado correctamente con locators preservados")
    return grupo

