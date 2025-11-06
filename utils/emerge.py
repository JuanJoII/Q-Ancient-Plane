import maya.cmds as cmds
from Utils.tools import generar_parte, CONFIG


def emerge_plane():
    """Genera el avión completo aplicando deformaciones procedurales a cada parte."""
    cmds.select(clear=True)
    print("🚀 Generando avión completo...")

    for parte in CONFIG.keys():
        generar_parte(parte)

    print("✅ Avión generado exitosamente.")
