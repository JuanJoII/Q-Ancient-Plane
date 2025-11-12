import maya.cmds as cmds
from Utils.tools import generar_parte
from Utils.emerge import emerge_plane
from PlaneRig import create_joints, spline_auto_rig
from Materials.materials import aplicar_material_oro
from Materials.lights_setup import setup_lights


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

    # --- Materiales ---
    cmds.frameLayout(label="Materiales", collapsable=True, collapse=False, marginWidth=10, marginHeight=8)
    cmds.columnLayout(adj=True, rowSpacing=5)

    def aplicar_material_a_todos(*_):
        partes = ["FUSELAJE_GENERADO", "ALAS_GENERADO", "COLA_GENERADO", "CABEZA_GENERADO", "ORNAMENTACION_GENERADO"]
        for parte in partes:
            aplicar_material_oro(parte)

    cmds.button(
        label="Aplicar Material de Oro a Todo el Avión",
        bgc=(0.9, 0.8, 0.2),
        height=35,
        c=aplicar_material_a_todos
    )

    # --- Iluminación ---
    cmds.frameLayout(label="Iluminación", collapsable=True, collapse=False, marginWidth=10, marginHeight=8)
    cmds.columnLayout(adj=True, rowSpacing=5)

    cmds.button(
        label="Generar Luces de Escena",
        bgc=(0.7, 0.7, 0.9),
        height=35,
        c=lambda *_: setup_lights()
    )
    
    cmds.separator(height=10, style="in")
    
    # Botón final
    
    cmds.setParent("..")
    cmds.showWindow("GeneradorAvion")
