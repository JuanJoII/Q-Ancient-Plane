import maya.cmds as cmds
import colorsys

def ajustar_color_oro(h, s, v, nombre_material="M_Gold"):
    """
    Ajusta el color base del material de oro según valores HSV en tiempo real.
    """
    if not cmds.objExists(nombre_material):
        cmds.warning(f"[!] No se encontró el material '{nombre_material}'. Aplícalo primero al avión.")
        return

    # Convertir HSV a RGB
    r, g, b = colorsys.hsv_to_rgb(h, s, v)

    try:
        cmds.setAttr(f"{nombre_material}.baseColor", r, g, b, type="double3")
        cmds.setAttr(f"{nombre_material}.specularColor", r, g, b, type="double3")
        print(f"[✓] Color del oro actualizado: RGB({r:.2f}, {g:.2f}, {b:.2f})")
    except:
        cmds.warning(f"No se pudo cambiar el color del material '{nombre_material}'.")
