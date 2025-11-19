"""
Configuración principal de luces para escenas de Maya
"""

import maya.cmds as cmds
from .skydome import crear_skydome_con_variaciones


def setup_lights():
    """
    Configura un sistema de iluminación de 3 puntos más skydome.
    Elimina luces previas y crea una configuración profesional.
    """
    print("💡 Configurando luces de escena...")

    # Eliminar luces previas si existen
    _limpiar_luces_existentes()

    # Crear sistema de 3 puntos
    _crear_luz_principal()
    _crear_luz_relleno()
    _crear_luz_trasera()

    # Crear skydome si Arnold está disponible
    if cmds.pluginInfo('mtoa', query=True, loaded=True):
        crear_skydome_con_variaciones()
        print("[✓] SkyDome Light con ramp de cielo creado.")
    else:
        print("[i] Arnold no disponible, skydome omitido.")

    print("✅ Iluminación configurada correctamente.")


def _limpiar_luces_existentes():
    """Elimina todas las luces existentes en la escena"""
    tipos_luces = ["directionalLight", "pointLight", "areaLight", "spotLight"]
    luces_existentes = cmds.ls(type=tipos_luces)
    
    if luces_existentes:
        cmds.delete(luces_existentes)
        print("[i] Luces anteriores eliminadas.")


def _crear_luz_principal():
    """Crea la luz direccional principal (key light)"""
    luz = cmds.directionalLight(name="Main_Directional_Light", intensity=1.2)
    transform = cmds.listRelatives(luz, parent=True)[0]
    
    cmds.setAttr(f"{transform}.rotateX", -45)
    cmds.setAttr(f"{transform}.rotateY", 30)
    cmds.setAttr(f"{transform}.rotateZ", 0)
    
    print("[✓] Luz direccional principal creada.")
    return transform


def _crear_luz_relleno():
    """Crea la luz de relleno (fill light)"""
    luz = cmds.directionalLight(name="Fill_Light", intensity=0.6)
    transform = cmds.listRelatives(luz, parent=True)[0]
    
    cmds.setAttr(f"{transform}.rotateX", -20)
    cmds.setAttr(f"{transform}.rotateY", -60)
    cmds.setAttr(f"{transform}.rotateZ", 0)
    
    print("[✓] Luz de relleno creada.")
    return transform


def _crear_luz_trasera():
    """Crea la luz trasera (rim/back light)"""
    luz = cmds.directionalLight(name="Rim_Light", intensity=0.8)
    transform = cmds.listRelatives(luz, parent=True)[0]
    
    cmds.setAttr(f"{transform}.rotateX", 40)
    cmds.setAttr(f"{transform}.rotateY", 180)
    cmds.setAttr(f"{transform}.rotateZ", 0)
    
    print("[✓] Luz trasera creada.")
    return transform