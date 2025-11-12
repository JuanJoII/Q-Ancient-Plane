import maya.cmds as cmds
from Utils.tools import generar_parte
from Utils.emerge import emerge_plane
from PlaneRig import create_joints, spline_auto_rig
from Materials.materials import aplicar_material_oro
from Materials.lights_setup import setup_lights
from Materials.select_color import ajustar_color_oro
from Materials.outline import aplicar_outline_toon, ajustar_grosor_outline, ajustar_color_outline



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

    # --- Sección Iluminación ---
    cmds.frameLayout(label="Iluminación", collapsable=True, collapse=False, marginWidth=10, marginHeight=8)
    cmds.columnLayout(adj=True, rowSpacing=5)

    cmds.button(
        label="Generar Luces de Escena",
        bgc=(0.7, 0.7, 0.9),
        height=35,
        c=lambda *_: setup_lights()
    )
    cmds.setParent("..")  
    cmds.setParent("..")  
    
     # --- Sección Materiales ---
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

    cmds.separator(height=10, style="in")

    cmds.text(label="Ajustar Color del Oro", align="left", height=20, font="boldLabelFont")

    # --- Sliders de color (HSV) ---
    hue_slider = cmds.floatSliderGrp(
        label="Hue",
        field=True, min=0.0, max=1.0, value=0.12, step=0.01,
        dragCommand=lambda *_: actualizar_color_en_vivo()
    )
    sat_slider = cmds.floatSliderGrp(
        label="Saturation",
        field=True, min=0.0, max=1.0, value=0.8, step=0.01,
        dragCommand=lambda *_: actualizar_color_en_vivo()
    )
    val_slider = cmds.floatSliderGrp(
        label="Value",
        field=True, min=0.0, max=1.0, value=1.0, step=0.01,
        dragCommand=lambda *_: actualizar_color_en_vivo()
    )

    def actualizar_color_en_vivo():
        h = cmds.floatSliderGrp(hue_slider, q=True, value=True)
        s = cmds.floatSliderGrp(sat_slider, q=True, value=True)
        v = cmds.floatSliderGrp(val_slider, q=True, value=True)
        ajustar_color_oro(h, s, v)

    cmds.setParent("..")
    cmds.setParent("..")
    
   
    cmds.separator(height=10, style="in")

    # --- Sección Outline Toon ---
    cmds.frameLayout(label="Outline Toon", collapsable=True, collapse=False, marginWidth=10, marginHeight=8)
    cmds.columnLayout(adj=True, rowSpacing=5)

    def aplicar_outline_a_todos(*_):
        partes = ["FUSELAJE_GENERADO", "ALAS_GENERADO", "COLA_GENERADO", "CABEZA_GENERADO", "ORNAMENTACION_GENERADO"]
        aplicar_outline_toon(partes, ancho_linea=0.02)

    cmds.button(
        label="Aplicar Outline Toon al Avión",
        bgc=(0.6, 0.8, 0.9),
        height=35,
        c=aplicar_outline_a_todos
    )

    cmds.separator(height=10, style="in")

    cmds.text(label="Ajustar Color del Outline", align="left", height=20, font="boldLabelFont")

    # --- Sliders de color (HSV) ---
    hue_outline_slider = cmds.floatSliderGrp(
        label="Hue",
        field=True, min=0.0, max=1.0, value=0.0, step=0.01,
        dragCommand=lambda *_: actualizar_outline_en_vivo()
    )
    sat_outline_slider = cmds.floatSliderGrp(
        label="Saturation",
        field=True, min=0.0, max=1.0, value=0.0, step=0.01,
        dragCommand=lambda *_: actualizar_outline_en_vivo()
    )
    val_outline_slider = cmds.floatSliderGrp(
        label="Value",
        field=True, min=0.0, max=1.0, value=0.0, step=0.01,
        dragCommand=lambda *_: actualizar_outline_en_vivo()
    )

    # --- Slider de grosor ---
    grosor_outline_slider = cmds.floatSliderGrp(
        label="Grosor",
        field=True, min=0.01, max=0.5, value=0.02, step=0.01,
        dragCommand=lambda *_: actualizar_outline_en_vivo()
    )

    def actualizar_outline_en_vivo():
        h = cmds.floatSliderGrp(hue_outline_slider, q=True, value=True)
        s = cmds.floatSliderGrp(sat_outline_slider, q=True, value=True)
        v = cmds.floatSliderGrp(val_outline_slider, q=True, value=True)
        grosor = cmds.floatSliderGrp(grosor_outline_slider, q=True, value=True)
        
        ajustar_color_outline(h, s, v)
        ajustar_grosor_outline(grosor)

    cmds.setParent("..")
    cmds.setParent("..")



    
    cmds.separator(height=10, style="in")
    
    # Botón final
    
    cmds.setParent("..")
    cmds.showWindow("GeneradorAvion")
