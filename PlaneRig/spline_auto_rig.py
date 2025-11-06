import maya.cmds as cmds
from SplineRig import (
    locators2curve,
    doble_parent,
    create_controls,
    tarjet_curve,
    aim_const,
    parent_const,
    all_tools,
)


def get_joint_chain_by_suffix(suffix="core"):
    """
    Devuelve una cadena de joints que terminan con el sufijo indicado (por defecto 'core'),
    ordenados jerárquicamente de padre a hijo.
    """
    joints = cmds.ls(type="joint") or []
    core_joints = [j for j in joints if j.lower().startswith(suffix.lower())]

    if not core_joints:
        cmds.warning(f"⚠️ No se encontraron joints con el sufijo '{suffix}'.")
        return []

    # Buscar el joint raíz (el que no está parentado a otro de la lista)
    root = None
    for j in core_joints:
        parent = cmds.listRelatives(j, parent=True, type="joint")
        if not parent or parent[0] not in core_joints:
            root = j
            break

    if not root:
        cmds.warning("⚠️ No se encontró un joint raíz para la cadena core.")
        return []

    # Recorrer jerárquicamente desde el root hasta el último hijo
    chain = [root]
    child = cmds.listRelatives(root, children=True, type="joint")
    while child:
        chain.append(child[0])
        child = cmds.listRelatives(child[0], children=True, type="joint")

    print(f"[✓] Cadena detectada automáticamente: {chain}")
    return chain


def build_spine_from_core_joints():
    """Crea el rig de columna automáticamente usando los joints con sufijo 'core'."""
    chain = get_joint_chain_by_suffix("core")
    if not chain:
        return

    num_joints = len(chain)
    base_name = chain[0].split("_")[0]  # inferencia del prefijo (ej: 'plane')
    curve_name = f"{base_name}_curve"

    # Obtener posiciones
    positions = [cmds.xform(j, q=True, ws=True, t=True) for j in chain]

    # Crear curva
    if cmds.objExists(curve_name):
        cmds.delete(curve_name)
    curve = cmds.curve(name=curve_name, degree=1, ep=positions)

    # Pipeline del rig
    locators2curve.create_spine_locators(curve_name=curve_name, num_locs=num_joints)
    doble_parent.connect_locators_to_curve(curve_name=curve_name, num_locs=num_joints)
    create_controls.create_spine_controls(num_ctrls=num_joints)
    tarjet_curve.create_spine_targets(curve_name=curve_name, num_targets=num_joints)
    aim_const.create_spine_target_aims(num_targets=num_joints)
    parent_const.constrain_joints_to_targets(num_pairs=num_joints)

    print(f"✅ Rig de columna generado automáticamente con {num_joints} joints 'core'.")


if __name__ == "__main__":
    build_spine_from_core_joints()
