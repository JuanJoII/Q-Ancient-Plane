import maya.cmds as cmds
from Utils.tools import generar_parte
from Utils.emerge import emerge_plane
from PlaneRig import create_joints, spline_auto_rig
from Environment.terrain import crear_terreno_montanoso
from Environment.cloud import crear_campo_nubes
from Materials.materials import aplicar_material_oro, aplicar_material_montanas, aplicar_material_nubes
from Materials.lights_setup import setup_lights
from Materials.select_color import ajustar_color_oro
from Materials.outline import aplicar_outline_toon, ajustar_grosor_outline, ajustar_color_outline
from Utils.emerge_full_setup import emerge_all_scene



def crear_ui():
    if cmds.window("GeneradorAvion", exists=True):
        cmds.deleteUI("GeneradorAvion")
    
    cmds.window(
        "GeneradorAvion",
        title="Generador Procedural de Avión - QAP",
        widthHeight=(300, 400),
    )
    
    cmds.scrollLayout(verticalScrollBarThickness=10, horizontalScrollBarThickness=0)
    cmds.columnLayout(adj=True, rowSpacing=6)
    
    # Título principal
    cmds.text(label="Q'Ancient Plane", align="center", height=50, font="boldLabelFont")
    
    cmds.button(label="Emerger Avión", c=lambda *_: emerge_plane())
    cmds.button(label="Emerger Escena Completa", c=lambda *_: emerge_all_scene())
    cmds.separator(height=20, style="in")
    
    # --- Sección: Generación de partes ---
    cmds.frameLayout(label="Generar Partes", collapsable=True, collapse=False, marginWidth=10, marginHeight=8)
    cmds.columnLayout(adj=True, rowSpacing=5)
    
    cmds.button(label="Generar Fuselaje", c=lambda *_: generar_parte("FUSELAJE"))
    cmds.button(label="Generar Alas", c=lambda *_: generar_parte("ALAS"))
    cmds.button(label="Generar Cabeza", c=lambda *_: generar_parte("CABEZA"))
    cmds.button(label="Generar Cola", c=lambda *_: generar_parte("COLA"))
    cmds.button(label="Generar Ornamentación", c=lambda *_: generar_parte("ORNAMENTACION"))
    
    cmds.setParent("..")  # Salir del columnLayout interno
    cmds.setParent("..")  # Salir del frameLayout
    cmds.separator(height=10, style="in")
    
    # --- Nueva Sección: Rigging ---
    cmds.frameLayout(label="Rigging", collapsable=True, collapse=False, marginWidth=10, marginHeight=8)
    cmds.columnLayout(adj=True, rowSpacing=5)
    
    cmds.button(label="Crear Joints", c=lambda *_: create_joints.crear_rig_completo())
    cmds.button(label="Crear Rig Spline", c=lambda *_: spline_auto_rig.build_spine_from_core_joints())
    
    cmds.setParent("..")  # Salir del columnLayout interno
    cmds.setParent("..")  # Salir del frameLayout
    cmds.separator(height=10, style="in")

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
    cmds.separator(height=10, style="in")
    
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
    
    # --- Nueva Sección: Environment ---
    cmds.frameLayout(label="Escenario", collapsable=True, collapse=False, marginWidth=10, marginHeight=8)
    cmds.columnLayout(adj=True, rowSpacing=6)
    
    cmds.text(label="Terreno Montañoso", font="boldLabelFont")
    
    # Inputs para terreno
    terreno_subdiv = cmds.intSliderGrp(label="Subdivisiones", min=20, max=100, value=50, field=True)
    terreno_escala = cmds.floatSliderGrp(label="Escala", min=50, max=300, value=150, field=True)
    terreno_altura = cmds.floatSliderGrp(label="Altura Máx Montañas", min=5, max=60, value=27, field=True)
    terreno_octavas = cmds.intSliderGrp(label="Detalle", min=1, max=8, value=4, field=True)
    terreno_pos_x = cmds.floatSliderGrp(label="Posición en X", min=-100, max=50, value=-0, field=True)
    terreno_pos_y = cmds.floatSliderGrp(label="Posición en Y", min=-100, max=50, value=-35, field=True)
    terreno_pos_z = cmds.floatSliderGrp(label="Posición en Z", min=-100, max=50, value=-0, field=True)
    
    cmds.button(
        label="Generar Terreno",
        c=lambda *_: crear_terreno_montanoso(
            subdivisiones=cmds.intSliderGrp(terreno_subdiv, q=True, v=True),
            escala=cmds.floatSliderGrp(terreno_escala, q=True, v=True),
            altura_max=cmds.floatSliderGrp(terreno_altura, q=True, v=True),
            octavas=cmds.intSliderGrp(terreno_octavas, q=True, v=True),
            pos_y=cmds.floatSliderGrp(terreno_pos_y, q=True, v=True),
            pos_x=cmds.floatSliderGrp(terreno_pos_x, q=True, v=True),
            pos_z=cmds.floatSliderGrp(terreno_pos_z, q=True, v=True)
        ),
        backgroundColor=[0.3, 0.5, 0.3]
    )
    
    cmds.button(
    label="Aplicar Material de Montañas",
    c=lambda *_: aplicar_material_montanas("terreno"),
    backgroundColor=[0.2, 0.4, 0.2]
    )

    cmds.separator(height=8, style="single")

    cmds.text(label="Campo de Nubes", font="boldLabelFont")

    
    # Inputs para nubes
    nubes_cantidad = cmds.intSliderGrp(label="Nubes", min=1, max=100, value=25, field=True)
    nubes_radio = cmds.floatSliderGrp(label="Radio Dist.", min=20, max=300, value=100, field=True)
    nubes_alt_min = cmds.floatSliderGrp(label="Altura Mín", min=-50, max=20, value=-18, field=True)
    nubes_alt_max = cmds.floatSliderGrp(label="Altura Máx", min=-20, max=50, value=0, field=True)
    
    cmds.button(
        label="Generar Cielo",
        c=lambda *_: crear_campo_nubes(
            num_nubes=cmds.intSliderGrp(nubes_cantidad, q=True, v=True),
            radio_distribucion=cmds.floatSliderGrp(nubes_radio, q=True, v=True),
            altura_min=cmds.floatSliderGrp(nubes_alt_min, q=True, v=True),
            altura_max=cmds.floatSliderGrp(nubes_alt_max, q=True, v=True)
        ),
        backgroundColor=[0.4, 0.6, 0.8]
    )
    
    # --- Material nubes ---
    cmds.button(
    label="Aplicar Material de Nubes",
    c=lambda *_: aplicar_material_nubes("campo_nubes"),
    backgroundColor=[0.3, 0.5, 0.7]
   )
    
    cmds.separator(height=12, style="in")
    
    # Botón final
    
    cmds.setParent("..")
    cmds.showWindow("GeneradorAvion")

if __name__ == "__main__":
    crear_ui()
