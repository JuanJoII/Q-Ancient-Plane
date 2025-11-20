import maya.cmds as cmds

def crear_controlador_vuelo(avion="CTRL_Avion", curva="curva_vuelo", duracion=500):
    """
    Crea un sistema de vuelo usando un locator como driver.
    """
    # 1. Eliminar controlador anterior si existe
    if cmds.objExists("FLIGHT_DRIVER"):
        cmds.delete("FLIGHT_DRIVER")
    if cmds.objExists("FLIGHT_DRIVER_constraint"):
        cmds.delete("FLIGHT_DRIVER_constraint")

    # 2. Crear locator driver
    driver = cmds.spaceLocator(name="FLIGHT_DRIVER")[0]
    cmds.hide(driver)

    # 3. pathAnimation en el driver
    motion_path = cmds.pathAnimation(
        driver,
        curva,
        name="flight_motionPath",
        fractionMode=True,
        follow=True,
        followAxis="x",
        upAxis="y",
        worldUpType="vector",
        worldUpVector=(0, 1, 0),
        bank=True,
        bankScale=1.2,
        bankThreshold=25,
        startTimeU=1,
        endTimeU=duracion
    )

    # 4. Hacer cíclico
    u_node = cmds.listConnections(motion_path + ".uValue", type="animCurveTU")
    if u_node:
        cmds.setAttr(u_node[0] + ".preInfinity", 3) 
        cmds.setAttr(u_node[0] + ".postInfinity", 3)

    # 5. Parent constraint del driver al avión
    constraint = cmds.parentConstraint(driver, avion, mo=False, name="FLIGHT_DRIVER_constraint")[0]

    print(f"Controlador de vuelo creado → {duracion} frames | Curva: {curva}")
    return driver, constraint

def eliminar_vuelo():
    """Limpia todo el sistema de vuelo"""
    for obj in ["FLIGHT_DRIVER", "flight_motionPath", "FLIGHT_DRIVER_constraint"]:
        if cmds.objExists(obj):
            try:
                cmds.delete(obj)
            except:
                pass
    print("Vuelo eliminado - avión libre")