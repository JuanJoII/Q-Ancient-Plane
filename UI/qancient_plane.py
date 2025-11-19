import maya.cmds as cmds
from Utils.tools import generar_parte
from Utils.emerge import emerge_plane
from PlaneRig import create_joints, spline_auto_rig
from Environment.terrain import crear_terreno_montanoso
from Environment.cloud import crear_campo_nubes
from Materials.materials import aplicar_material_oro, aplicar_material_montanas, aplicar_material_nubes, cambiar_color_montanas_aleatorio
from Materials.select_color import ajustar_color_oro
from Utils.emerge_full_setup import emerge_all_scene

# === IMPORTAR SISTEMA DE ILUMINACIÓN MODULAR ===
from Lights.lights_setup import setup_lights
from Lights.skydome import listar_cielos_disponibles, cambiar_cielo_aleatorio, aplicar_cielo_especifico


def crear_ui():
    if cmds.window("GeneradorAvion", exists=True):
        cmds.deleteUI("GeneradorAvion")
    
    window = cmds.window(
        "GeneradorAvion",
        title="Generador Procedural de Avión - QAP",
        widthHeight=(320, 650),
    )
    
    # Scroll Layout principal para toda la UI
    main_scroll = cmds.scrollLayout(
        verticalScrollBarThickness=16,
        horizontalScrollBarThickness=0,
        childResizable=True
    )
    
    cmds.columnLayout(adj=True, rowSpacing=6)
    
    # Título principal
    cmds.text(label="Q'Ancient Plane", align="center", height=50, font="boldLabelFont")
    
    # === BOTONES DE GENERACIÓN RÁPIDA ===
    cmds.button(
        label="✨ Generar Avión Completo",
        c=lambda *_: emerge_plane(),
        backgroundColor=[0.2, 0.6, 0.4],
        height=40,
        annotation="Genera todas las partes del avión"
    )
    
    cmds.button(
        label="🌟 Generar Escena Completa (Avión + Entorno + Luces)",
        c=lambda *_: emerge_all_scene(),
        backgroundColor=[0.3, 0.5, 0.7],
        height=40,
        annotation="Genera el avión, rig, terreno y nubes"
    )
    
    cmds.separator(height=20, style="in")
    
    # --- Sección: Generación de partes ---
    cmds.frameLayout(label="Generar Partes", collapsable=True, collapse=False, marginWidth=10, marginHeight=8)
    cmds.columnLayout(adj=True, rowSpacing=5)
    
    cmds.button(label="Generar Fuselaje", c=lambda *_: generar_parte("FUSELAJE"))
    cmds.button(label="Generar Alas", c=lambda *_: generar_parte("ALAS"))
    cmds.button(label="Generar Cabeza", c=lambda *_: generar_parte("CABEZA"))
    cmds.button(label="Generar Cola", c=lambda *_: generar_parte("COLA"))
    cmds.button(label="Generar Ornamentación", c=lambda *_: generar_parte("ORNAMENTACION"))
    
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.separator(height=10, style="in")
    
    # --- Sección: Rigging ---
    cmds.frameLayout(label="Rigging", collapsable=True, collapse=False, marginWidth=10, marginHeight=8)
    cmds.columnLayout(adj=True, rowSpacing=5)
    
    cmds.button(label="Crear Joints", c=lambda *_: create_joints.crear_rig_completo())
    cmds.button(label="Crear Rig Spline", c=lambda *_: spline_auto_rig.build_spine_from_core_joints())
    
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.separator(height=10, style="in")

    # ========================================
    # === SECCIÓN ILUMINACIÓN MEJORADA ===
    # ========================================
    cmds.frameLayout(label="💡 Iluminación", collapsable=True, collapse=False, marginWidth=10, marginHeight=8)
    cmds.columnLayout(adj=True, rowSpacing=5)

    # Botón principal de configuración
    cmds.button(
        label="🌟 Configurar Luces Completas",
        bgc=(0.4, 0.5, 0.7),
        height=40,
        c=lambda *_: setup_lights()
    )
    
    cmds.separator(height=8, style="single")
    
    # === CONTROL DE CIELOS ===
    cmds.text(label="Control de Cielo (Skydome)", font="boldLabelFont", align="left")
    
    cmds.button(
        label="🎲 Cielo Aleatorio",
        bgc=(0.5, 0.6, 0.8),
        height=32,
        c=lambda *_: cambiar_cielo_aleatorio()
    )
    
    cmds.separator(height=6, style="single")
    
    # === CIELOS PREDEFINIDOS (Grid 2 columnas) ===
    cmds.text(label="Cielos Predefinidos:", align="left", height=20)
    
    # Fila 1
    cmds.rowLayout(numberOfColumns=2, columnWidth2=(150, 150), columnAttach=[(1, "both", 2), (2, "both", 2)])
    cmds.button(label="☀️ Diurno", bgc=(0.5, 0.7, 0.9), c=lambda *_: aplicar_cielo_especifico("diurno"))
    cmds.button(label="🌅 Atardecer", bgc=(0.9, 0.5, 0.4), c=lambda *_: aplicar_cielo_especifico("atardecer"))
    cmds.setParent('..')
    
    # Fila 2
    cmds.rowLayout(numberOfColumns=2, columnWidth2=(150, 150), columnAttach=[(1, "both", 2), (2, "both", 2)])
    cmds.button(label="🌙 Noche", bgc=(0.1, 0.15, 0.3), c=lambda *_: aplicar_cielo_especifico("noche"))
    cmds.button(label="🌄 Amanecer", bgc=(0.9, 0.7, 0.5), c=lambda *_: aplicar_cielo_especifico("amanecer"))
    cmds.setParent('..')
    
    # Fila 3
    cmds.rowLayout(numberOfColumns=2, columnWidth2=(150, 150), columnAttach=[(1, "both", 2), (2, "both", 2)])
    cmds.button(label="⛈️ Tormenta", bgc=(0.3, 0.3, 0.35), c=lambda *_: aplicar_cielo_especifico("tormenta"))
    cmds.button(label="🌆 Crepúsculo", bgc=(0.5, 0.3, 0.6), c=lambda *_: aplicar_cielo_especifico("crepusculo"))
    cmds.setParent('..')
    
    cmds.separator(height=6, style="single")
    
    # Fila 4
    cmds.rowLayout(numberOfColumns=2, columnWidth2=(150, 150), columnAttach=[(1, "both", 2), (2, "both", 2)])
    cmds.button(label="🏜️ Desierto", bgc=(0.9, 0.8, 0.5), c=lambda *_: aplicar_cielo_especifico("desierto"))
    cmds.button(label="🌌 Aurora", bgc=(0.2, 0.5, 0.6), c=lambda *_: aplicar_cielo_especifico("aurora"))
    cmds.setParent('..')
    
    # Fila 5
    cmds.rowLayout(numberOfColumns=2, columnWidth2=(150, 150), columnAttach=[(1, "both", 2), (2, "both", 2)])
    cmds.button(label="👽 Alienígena", bgc=(0.5, 0.7, 0.9), c=lambda *_: aplicar_cielo_especifico("alienigena"))
    cmds.button(label="🔥 Infierno", bgc=(0.8, 0.3, 0.1), c=lambda *_: aplicar_cielo_especifico("infierno"))
    cmds.setParent('..')
    
    cmds.separator(height=6, style="single")

    cmds.setParent("..")  # Salir del columnLayout de Iluminación
    cmds.setParent("..")  # Salir del frameLayout de Iluminación
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

    cmds.separator(height=8, style="single")
    
    # === OPCIONES AVANZADAS: COLOR DEL ORO ===
    cmds.frameLayout(label="⚙ Opciones Avanzadas - Color", collapsable=True, collapse=True, marginWidth=5, marginHeight=5, borderStyle="etchedIn")
    cmds.columnLayout(adj=True, rowSpacing=5)
    
    cmds.text(label="Ajustar Color del Oro (HSV)", align="left", height=20, font="boldLabelFont")
    
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
    
    cmds.setParent('..')  # Salir del columnLayout
    cmds.setParent('..')  # Salir del frameLayout de opciones avanzadas

    cmds.setParent("..")  # Salir del columnLayout de Materiales
    cmds.setParent("..")  # Salir del frameLayout de Materiales
    cmds.separator(height=10, style="in")

    # --- Sección: Escenario ---
    cmds.frameLayout(label="Escenario", collapsable=True, collapse=False, marginWidth=10, marginHeight=8)
    cmds.columnLayout(adj=True, rowSpacing=6)
    
    # === TERRENO ===
    cmds.text(label="Terreno Montañoso Metálico", font="boldLabelFont")
    
    cmds.button(
        label="Generar Terreno (Valores por Defecto)",
        c=lambda *_: crear_terreno_montanoso(
            subdivisiones=50,
            escala=150,
            altura_max=27,
            octavas=4,
            pos_y=-35,
            pos_x=0,
            pos_z=0
        ),
        backgroundColor=[0.3, 0.5, 0.3]
    )
    
    cmds.button(
        label="Aplicar Material Metálico a Montañas",
        c=lambda *_: aplicar_material_montanas("terreno"),
        backgroundColor=[0.35, 0.35, 0.40],
        height=30
    )
    
    # === NUEVO BOTÓN: Cambiar Color Aleatorio ===
    cmds.button(
        label="🎨 Cambiar Color Metálico Aleatorio",
        c=lambda *_: cambiar_color_montanas_aleatorio(),
        backgroundColor=[0.5, 0.3, 0.6],
        height=30,
        annotation="Cambia el color de las montañas a una paleta metálica aleatoria"
    )
    
    cmds.separator(height=8, style="single")
    
    # === OPCIONES AVANZADAS: TERRENO ===
    cmds.frameLayout(label="⚙ Opciones Avanzadas - Terreno", collapsable=True, collapse=True, marginWidth=5, marginHeight=5, borderStyle="etchedIn")
    cmds.columnLayout(adj=True, rowSpacing=5)
    
    cmds.text(label="Configuración Personalizada del Terreno", align="left", height=20, font="boldLabelFont")
    
    terreno_subdiv = cmds.intSliderGrp(label="Subdivisiones", min=20, max=100, value=50, field=True)
    terreno_escala = cmds.floatSliderGrp(label="Escala", min=50, max=300, value=150, field=True)
    terreno_altura = cmds.floatSliderGrp(label="Altura Máx Montañas", min=5, max=60, value=27, field=True)
    terreno_octavas = cmds.intSliderGrp(label="Detalle", min=1, max=8, value=4, field=True)
    terreno_pos_x = cmds.floatSliderGrp(label="Posición en X", min=-100, max=50, value=0, field=True)
    terreno_pos_y = cmds.floatSliderGrp(label="Posición en Y", min=-100, max=50, value=-35, field=True)
    terreno_pos_z = cmds.floatSliderGrp(label="Posición en Z", min=-100, max=50, value=0, field=True)
    
    cmds.button(
        label="Generar Terreno Personalizado",
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
    
    cmds.setParent('..')  # Salir del columnLayout
    cmds.setParent('..')  # Salir del frameLayout de opciones avanzadas terreno

    cmds.separator(height=12, style="single")

    # === CIELO/NUBES ===
    cmds.text(label="Campo de Nubes", font="boldLabelFont")
    
    cmds.button(
        label="Generar Cielo (Valores por Defecto)",
        c=lambda *_: crear_campo_nubes(
            num_nubes=25,
            radio_distribucion=100,
            altura_min=-18,
            altura_max=0
        ),
        backgroundColor=[0.4, 0.6, 0.8]
    )
    
    cmds.button(
        label="Aplicar Material de Nubes",
        c=lambda *_: aplicar_material_nubes("campo_nubes"),
        backgroundColor=[0.3, 0.5, 0.7]
    )
    
    # === OPCIONES AVANZADAS: CIELO ===
    cmds.frameLayout(label="⚙ Opciones Avanzadas - Cielo", collapsable=True, collapse=True, marginWidth=5, marginHeight=5, borderStyle="etchedIn")
    cmds.columnLayout(adj=True, rowSpacing=5)
    
    cmds.text(label="Configuración Personalizada del Cielo", align="left", height=20, font="boldLabelFont")
    
    nubes_cantidad = cmds.intSliderGrp(label="Nubes", min=1, max=100, value=25, field=True)
    nubes_radio = cmds.floatSliderGrp(label="Radio Dist.", min=20, max=300, value=100, field=True)
    nubes_alt_min = cmds.floatSliderGrp(label="Altura Mín", min=-50, max=20, value=-18, field=True)
    nubes_alt_max = cmds.floatSliderGrp(label="Altura Máx", min=-20, max=50, value=0, field=True)
    
    cmds.button(
        label="Generar Cielo Personalizado",
        c=lambda *_: crear_campo_nubes(
            num_nubes=cmds.intSliderGrp(nubes_cantidad, q=True, v=True),
            radio_distribucion=cmds.floatSliderGrp(nubes_radio, q=True, v=True),
            altura_min=cmds.floatSliderGrp(nubes_alt_min, q=True, v=True),
            altura_max=cmds.floatSliderGrp(nubes_alt_max, q=True, v=True)
        ),
        backgroundColor=[0.4, 0.6, 0.8]
    )
    
    cmds.setParent('..')  # Salir del columnLayout
    cmds.setParent('..')  # Salir del frameLayout de opciones avanzadas cielo
    
    cmds.setParent("..")  # Salir del columnLayout de Escenario
    cmds.setParent("..")  # Salir del frameLayout de Escenario
    
    cmds.showWindow(window)


if __name__ == "__main__":
    crear_ui()