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


def generar_parte(parte):
    # === 1. ELIMINAR EXISTENTE ===
    nombre_final = f"{parte}_GENERADO"
    if cmds.objExists(nombre_final):
        try:
            cmds.delete(nombre_final)
            print(f"Eliminado anterior: {nombre_final}")
        except:
            pass

    # === 2. OBTENER VARIANTE ===
    variantes = obtener_variantes(parte)
    if not variantes:
        cmds.warning(f"No hay modelos .ma para {parte}")
        return

    archivo = random.choice(variantes)
    ruta = os.path.join(CARPETA_MODELOS, archivo)

    # === 3. IMPORTAR CON NAMESPACE TEMPORAL ===
    ns_temp = f"tmp_{parte}_{random.randint(1000, 9999)}"
    antes = set(cmds.ls(assemblies=True))
    try:
        cmds.file(ruta, i=True, namespace=ns_temp, force=True)
        print(f"Importado: {archivo} con namespace {ns_temp}")
    except Exception as e:
        cmds.warning(f"Error importando {archivo}: {e}")
        return

    # === 4. DETECTAR OBJETOS NUEVOS ===
    despues = set(cmds.ls(assemblies=True))
    nuevos = list(despues - antes)

    if not nuevos:
        cmds.warning("No se detectó ningún objeto nuevo tras importar")
        return

    # Usar el primer objeto como principal
    obj = nuevos[0]
    try:
        transform = cmds.rename(obj, nombre_final)
    except:
        transform = obj

    # === 5. TRAER LOS OBJECTSETS AL ROOT (fuera del namespace) ===
    sets_en_namespace = cmds.ls(f"{ns_temp}:*", type="objectSet")
    for old_set in sets_en_namespace:
        nombre_limpio = old_set.split(":", 1)[-1]
        if cmds.objExists(nombre_limpio):
            cmds.delete(nombre_limpio)
        try:
            nuevo_set = cmds.rename(old_set, nombre_limpio)
            print(f"Set transferido: {nuevo_set}")
        except Exception as e:
            print(f"No se pudo transferir {old_set}: {e}")

    # === 6. ELIMINAR NAMESPACE ===
    try:
        cmds.namespace(removeNamespace=ns_temp, deleteNamespaceContent=False)
    except:
        pass

    # Resetear jerarquía y transformaciones
    # --- Resetear jerarquía y transformaciones ---
    padres = cmds.listRelatives(transform, parent=True)
    if padres:
        try:
            cmds.parent(transform, world=True)
            print(f"{transform} desparentado del grupo {padres[0]}")
        except Exception as e:
            print(f"No se pudo desparentar {transform}: {e}")

    # Freeze transforms
    cmds.makeIdentity(transform, apply=True, t=True, r=True, s=True, n=False)
    cmds.xform(transform, pivots=(0, 0, 0), worldSpace=True)

    # === 7. APLICAR TRANSFORMACIONES ===
    if parte in CONFIG:
        data = CONFIG[parte]
        cmds.move(*data.get("posicion", [0, 0, 0]), transform)
        cmds.rotate(*data.get("rotacion", [0, 0, 0]), transform)
        cmds.scale(*data.get("escala", [1, 1, 1]), transform)

    # === 8. CORREGIR NORMALES ===
    shapes = cmds.listRelatives(transform, shapes=True, fullPath=True)
    if shapes:
        cmds.polyNormal(shapes[0], normalMode=0, userNormalMode=0, ch=False)

    # === 9. APLICAR DEFORMACIONES ===
    aplicar_deformaciones(parte, transform)

    print(f"{parte} generado correctamente → {nombre_final}")
    return transform
