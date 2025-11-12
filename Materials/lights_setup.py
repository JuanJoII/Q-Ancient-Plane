import maya.cmds as cmds

def setup_lights():
    print("💡 Configurando luces de escena...")

    # Eliminar luces previas si existen
    existing_lights = cmds.ls(type=["directionalLight", "pointLight", "areaLight", "spotLight"])
    if existing_lights:
        cmds.delete(existing_lights)
        print("[i] Luces anteriores eliminadas.")

    # Luz principal direccional (tipo sol)
    main_light = cmds.directionalLight(name="Main_Directional_Light", intensity=1.2)
    main_light_transform = cmds.listRelatives(main_light, parent=True)[0]
    cmds.setAttr(f"{main_light_transform}.rotateX", -45)
    cmds.setAttr(f"{main_light_transform}.rotateY", 30)
    cmds.setAttr(f"{main_light_transform}.rotateZ", 0)
    print("[✓] Luz direccional principal creada.")

    # Luz de relleno (más suave)
    fill_light = cmds.directionalLight(name="Fill_Light", intensity=0.6)
    fill_light_transform = cmds.listRelatives(fill_light, parent=True)[0]
    cmds.setAttr(f"{fill_light_transform}.rotateX", -20)
    cmds.setAttr(f"{fill_light_transform}.rotateY", -60)
    cmds.setAttr(f"{fill_light_transform}.rotateZ", 0)
    print("[✓] Luz de relleno creada.")

    # Luz trasera (rim light)
    rim_light = cmds.directionalLight(name="Rim_Light", intensity=0.8)
    rim_light_transform = cmds.listRelatives(rim_light, parent=True)[0]
    cmds.setAttr(f"{rim_light_transform}.rotateX", 40)
    cmds.setAttr(f"{rim_light_transform}.rotateY", 180)
    cmds.setAttr(f"{rim_light_transform}.rotateZ", 0)
    print("[✓] Luz trasera creada.")

    # Crear un "skydome" si se usa Arnold
    if cmds.pluginInfo('mtoa', query=True, loaded=True):
        skydome = cmds.shadingNode('aiSkyDomeLight', asLight=True, name="SkyDome_Light")
        cmds.setAttr(f"{skydome}.intensity", 0.3)
        print("[✓] SkyDome Light de Arnold creado.")

    print("✅ Iluminación configurada correctamente.")

# Ejecutar la función
if __name__ == "__main__":
    setup_lights()
