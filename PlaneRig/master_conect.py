import maya.cmds as cmds

def conectar_spine_al_master(master="CTRL_Avion"):
    """
    Conecta los spineLoc_ctrl_### y los CTRL_wing_L/R_001 al control maestro.
    Crea parentConstraint manteniendo offset.
    """

    if not cmds.objExists(master):
        cmds.warning(f"No existe el control maestro: {master}")
        return

    # -------------------------
    # 1. Spine controls
    # -------------------------
    spine_ctrls = cmds.ls("spineLoc_ctrl_*", type="transform") or []

    for ctrl in spine_ctrls:
        # Eliminar constraints antiguos
        anteriores = cmds.listRelatives(ctrl, type="parentConstraint") or []
        for c in anteriores:
            cmds.delete(c)

        cmds.parentConstraint(master, ctrl, mo=True)
        print(f"✔ {ctrl} conectado al master {master}")


    # -------------------------
    # 2. Wing controls
    # -------------------------
    wing_ctrls = ["CTRL_wing_L_001", "CTRL_wing_R_001"]

    for ctrl in wing_ctrls:
        if not cmds.objExists(ctrl):
            cmds.warning(f"No existe el control de ala: {ctrl}")
            continue

        anteriores = cmds.listRelatives(ctrl, type="parentConstraint") or []
        for c in anteriores:
            cmds.delete(c)

        cmds.parentConstraint(master, ctrl, mo=True)
        print(f"✔ {ctrl} conectado al master {master}")

    print("🎯 Spine y wings conectados correctamente al control maestro.")
