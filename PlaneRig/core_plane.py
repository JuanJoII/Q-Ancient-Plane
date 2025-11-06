import maya.cmds as cmds
from Utils.config import CONFIG

def crear_core_joints():
    """
    Crea los tres joints principales del cuerpo del avión:
    core_plane_joint_001 → core_plane_joint_002 → core_plane_joint_003
    (Cabeza, Fuselaje, Cola)
    """
    joints_creados = {}
    orden_core = [("CABEZA", "core_plane_joint_001"),
                  ("FUSELAJE", "core_plane_joint_002"),
                  ("COLA", "core_plane_joint_003")]

    def centro_bbox(obj):
        bbox = cmds.exactWorldBoundingBox(obj)
        return [(bbox[0] + bbox[3]) / 2.0,
                (bbox[1] + bbox[4]) / 2.0,
                (bbox[2] + bbox[5]) / 2.0]

    padre_anterior = None
    for parte, nombre_joint in orden_core:
        nombre_obj = f"{parte}_GENERADO"
        if not cmds.objExists(nombre_obj):
            print(f"[!] No se encontró la parte: {nombre_obj} → se omite {nombre_joint}")
            continue

        centro = centro_bbox(nombre_obj)
        cmds.select(clear=True)

        if cmds.objExists(nombre_joint):
            cmds.delete(nombre_joint)

        joint = cmds.joint(name=nombre_joint, position=centro, absolute=True)
        joints_creados[parte] = joint
        print(f"[✓] {parte}: {joint} creado en {centro}")

        # Parentar jerárquicamente
        if padre_anterior and cmds.objExists(padre_anterior):
            try:
                cmds.parent(joint, padre_anterior)
            except Exception as e:
                print(f"[!] No se pudo parentar {joint} a {padre_anterior}: {e}")

        padre_anterior = joint

    return joints_creados
