import maya.cmds as cmds
from utils.tools import generar_parte
from utils.emerge import emerge_plane
from rig import create_joints, spline_auto_rig


def crear_ui():
    if cmds.window("GeneradorAvion", exists=True):
        cmds.deleteUI("GeneradorAvion")
    
    cmds.window(
        "GeneradorAvion",
        title="Generador Procedural de Avión - QAP",
        widthHeight=(300, 400),
    )
    
    cmds.columnLayout(adj=True, rowSpacing=6)
    
    # Título principal
    cmds.text(label="Modelo Procedural QAP", align="center", height=25, font="boldLabelFont")
    
    # --- Sección: Generación de partes ---
    cmds.button(label="Generar Fuselaje", c=lambda *_: generar_parte("FUSELAJE"))
    cmds.button(label="Generar Alas", c=lambda *_: generar_parte("ALAS"))
    cmds.button(label="Generar Cabeza", c=lambda *_: generar_parte("CABEZA"))
    cmds.button(label="Generar Cola", c=lambda *_: generar_parte("COLA"))
    cmds.button(label="Generar Ornamentación", c=lambda *_: generar_parte("ORNAMENTACION"))
    cmds.button(label="Emerger Avión", c=lambda *_: emerge_plane())
    
    cmds.separator(height=10, style="in")
    
    # --- Nueva Sección: Rigging ---
    cmds.frameLayout(label="Rigging", collapsable=True, collapse=False, marginWidth=10, marginHeight=8)
    cmds.columnLayout(adj=True, rowSpacing=5)
    
    cmds.button(label="Crear Joints", c=lambda *_: create_joints.crear_rig_completo())
    cmds.button(label="Crear Rig Spline", c=lambda *_: spline_auto_rig.build_spine_from_core_joints())
    
    cmds.setParent("..")  # Salir del columnLayout interno
    cmds.setParent("..")  # Salir del frameLayout
    
    cmds.separator(height=10, style="in")
    
    # Botón final
    
    cmds.setParent("..")
    cmds.showWindow("GeneradorAvion")
