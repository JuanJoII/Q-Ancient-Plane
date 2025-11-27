import maya.cmds as cmds
from Utils.tools import generar_parte
from Utils.emerge import emerge_plane
from PlaneRig.full_rig import crear_rig_completo
from Environment.terrain import crear_terreno_montanoso
from Environment.cloud import crear_campo_nubes
from Materials.materials import aplicar_material_oro, aplicar_material_montanas, aplicar_material_nubes, cambiar_color_montanas_aleatorio
from Materials.select_color import ajustar_color_oro
from Animation.fly_curve import crear_curva_vuelo
from Animation.dyn_fly_curve import crear_curva_dinamica
from Animation.flight_controller import crear_controlador_vuelo, eliminar_vuelo
from Utils.emerge_full_setup import emerge_all_scene

# === IMPORTAR SISTEMA DE ILUMINACIÓN MODULAR ===
from Lights.lights_setup import setup_lights
from Lights.skydome import cambiar_cielo_aleatorio, aplicar_cielo_especifico


def generar_parte_con_material(tipo_parte):
    """Genera una parte del avión y aplica el material automáticamente"""
    nombre_generado = generar_parte(tipo_parte)
    if nombre_generado:
        aplicar_material_oro(nombre_generado)


def generar_avion_completo_con_material():
    """Genera el avión completo y aplica materiales automáticamente"""
    emerge_plane()
    # Aplicar materiales a todas las partes
    partes = ["FUSELAJE_GENERADO", "ALAS_GENERADO", "COLA_GENERADO", "CABEZA_GENERADO", "ORNAMENTACION_GENERADO"]
    for parte in partes:
        if cmds.objExists(parte):
            aplicar_material_oro(parte)


def generar_terreno_con_material(**kwargs):
    """Genera el terreno y aplica el material automáticamente"""
    crear_terreno_montanoso(**kwargs)
    aplicar_material_montanas("terreno")


def generar_cielo_con_material(**kwargs):
    """Genera el cielo y aplica el material automáticamente"""
    crear_campo_nubes(**kwargs)
    aplicar_material_nubes("campo_nubes")


def crear_ui():
    if cmds.window("GeneradorAvion", exists=True):
        cmds.deleteUI("GeneradorAvion")
    
    window = cmds.window(
        "GeneradorAvion",
        title="Generador Procedural de Avión - QAP",
        widthHeight=(340, 700),
    )
    
    # Scroll Layout principal
    main_scroll = cmds.scrollLayout(
        verticalScrollBarThickness=16,
        horizontalScrollBarThickness=0,
        childResizable=True
    )
    
    cmds.columnLayout(adj=True, rowSpacing=8)
    
    # ========================================
    # === ENCABEZADO ===
    # ========================================
    cmds.text(
        label="Q'Ancient Plane",
        align="center",
        height=45,
        font="boldLabelFont",
    )
    
    cmds.text(
        label="Generador procedural de aviones Quimbaya con entorno\ny sistema de animación de vuelo integrado",
        align="center",
        height=35,
        font="smallPlainLabelFont",
    )
    
    cmds.separator(height=15, style="none")
    
    # ========================================
    # === GENERACIÓN RÁPIDA ===
    # ========================================
    
    cmds.button(
        label="🌟 Generar Escena Completa",
        c=lambda *_: emerge_all_scene(),
        backgroundColor=[0.25, 0.45, 0.65],
        height=45,
        annotation="Genera avión, rig, terreno, nubes y luces en un solo clic"
    )

    cmds.button(
        label="✈️ Generar Solo Avión",
        c=lambda *_: generar_avion_completo_con_material(),
        backgroundColor=[0.20, 0.55, 0.40],
        height=40,
        annotation="Genera todas las partes del avión con materiales aplicados"
    )
    
    cmds.separator(height=12, style="in")
    
    # ========================================
    # === CONTROL DE COLOR DEL AVIÓN ===
    # ========================================
    cmds.frameLayout(
        label="🎨 Color del Avión",
        collapsable=True,
        collapse=False,
        marginWidth=10,
        marginHeight=10,
        backgroundColor=[0.22, 0.22, 0.26]
    )
    cmds.columnLayout(adj=True, rowSpacing=6)
    
    cmds.text(label="Ajustar Color Metálico (HSV)", align="left", height=22, font="boldLabelFont")
    
    hue_slider = cmds.floatSliderGrp(
        label="Tono",
        field=True, min=0.0, max=1.0, value=0.12, step=0.01,
        dragCommand=lambda *_: actualizar_color_en_vivo(),
        columnWidth3=[80, 60, 160]
    )
    sat_slider = cmds.floatSliderGrp(
        label="Saturación",
        field=True, min=0.0, max=1.0, value=0.8, step=0.01,
        dragCommand=lambda *_: actualizar_color_en_vivo(),
        columnWidth3=[80, 60, 160]
    )
    val_slider = cmds.floatSliderGrp(
        label="Brillo",
        field=True, min=0.0, max=1.0, value=1.0, step=0.01,
        dragCommand=lambda *_: actualizar_color_en_vivo(),
        columnWidth3=[80, 60, 160]
    )

    def actualizar_color_en_vivo():
        h = cmds.floatSliderGrp(hue_slider, q=True, value=True)
        s = cmds.floatSliderGrp(sat_slider, q=True, value=True)
        v = cmds.floatSliderGrp(val_slider, q=True, value=True)
        ajustar_color_oro(h, s, v)
    
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.separator(height=12, style="in")
    
    # ========================================
    # === PARTES INDIVIDUALES ===
    # ========================================
    cmds.frameLayout(
        label="Generar Partes Individuales",
        collapsable=True,
        collapse=True,
        marginWidth=10,
        marginHeight=8,
        backgroundColor=[0.20, 0.20, 0.24]
    )
    cmds.columnLayout(adj=True, rowSpacing=5)
    
    cmds.button(label="Fuselaje", c=lambda *_: generar_parte_con_material("FUSELAJE"), backgroundColor=[0.30, 0.35, 0.40])
    cmds.button(label="Alas", c=lambda *_: generar_parte_con_material("ALAS"), backgroundColor=[0.30, 0.35, 0.40])
    cmds.button(label="Cabeza", c=lambda *_: generar_parte_con_material("CABEZA"), backgroundColor=[0.30, 0.35, 0.40])
    cmds.button(label="Cola", c=lambda *_: generar_parte_con_material("COLA"), backgroundColor=[0.30, 0.35, 0.40])
    cmds.button(label="Ornamentación", c=lambda *_: generar_parte_con_material("ORNAMENTACION"), backgroundColor=[0.30, 0.35, 0.40])
    
    cmds.setParent("..")
    cmds.setParent("..")
    
    cmds.separator(height=12, style="in")
    
    # ========================================
    # === RIGGING ===
    # ========================================
    cmds.frameLayout(
        label="🦴 Rigging",
        collapsable=True,
        collapse=False,
        marginWidth=10,
        marginHeight=8,
        backgroundColor=[0.22, 0.22, 0.26]
    )
    cmds.columnLayout(adj=True, rowSpacing=5)
    
    cmds.button(
        label="Crear Rig Completo",
        c=lambda *_: crear_rig_completo(),
        backgroundColor=[0.35, 0.45, 0.55],
        height=40,
        annotation="Crea joints, spline IK y controles en un solo paso"
    )
    
    cmds.setParent("..")
    cmds.setParent("..")
    
    cmds.separator(height=12, style="in")

    # ========================================
    # === ILUMINACIÓN ===
    # ========================================
    cmds.frameLayout(
        label="💡 Iluminación",
        collapsable=True,
        collapse=True,
        marginWidth=10,
        marginHeight=8,
        backgroundColor=[0.20, 0.20, 0.24]
    )
    cmds.columnLayout(adj=True, rowSpacing=6)

    cmds.button(
        label="🌟 Configurar Luces Completas",
        bgc=(0.35, 0.45, 0.65),
        height=38,
        c=lambda *_: setup_lights()
    )
    
    cmds.separator(height=8, style="single")
    
    cmds.text(label="Cielos Predefinidos", font="boldLabelFont", align="left", height=22)
    
    cmds.button(
        label="🎲 Cielo Aleatorio",
        bgc=(0.45, 0.55, 0.75),
        height=32,
        c=lambda *_: cambiar_cielo_aleatorio()
    )
    
    cmds.separator(height=6, style="single")
    
    # Grid de cielos predefinidos (2 columnas)
    cmds.rowColumnLayout(
    numberOfColumns=3,
    columnWidth=[(1, 155), (2, 155), (3, 155)],
    columnAttach=[(1, "both", 2), (2, "both", 2), (3, "both", 2)]
    )

    cmds.button(label="☀️ Diurno", bgc=(0.5, 0.7, 0.9), c=lambda *_: aplicar_cielo_especifico("diurno"))
    cmds.button(label="🌅 Atardecer", bgc=(0.9, 0.5, 0.4), c=lambda *_: aplicar_cielo_especifico("atardecer"))
    cmds.button(label="🌙 Noche", bgc=(0.1, 0.15, 0.3), c=lambda *_: aplicar_cielo_especifico("noche"))

    cmds.button(label="🌄 Amanecer", bgc=(0.9, 0.7, 0.5), c=lambda *_: aplicar_cielo_especifico("amanecer"))
    cmds.button(label="⛈️ Tormenta", bgc=(0.3, 0.3, 0.35), c=lambda *_: aplicar_cielo_especifico("tormenta"))
    cmds.button(label="🌆 Crepúsculo", bgc=(0.5, 0.3, 0.6), c=lambda *_: aplicar_cielo_especifico("crepusculo"))

    cmds.button(label="🏜️ Desierto", bgc=(0.9, 0.8, 0.5), c=lambda *_: aplicar_cielo_especifico("desierto"))
    cmds.button(label="🌌 Aurora", bgc=(0.2, 0.5, 0.6), c=lambda *_: aplicar_cielo_especifico("aurora"))
    cmds.button(label="👽 Alienígena", bgc=(0.5, 0.7, 0.9), c=lambda *_: aplicar_cielo_especifico("alienigena"))

    cmds.button(label="🔥 Infierno", bgc=(0.8, 0.3, 0.1), c=lambda *_: aplicar_cielo_especifico("infierno"))

    cmds.setParent("..")

    cmds.setParent('..')

    cmds.setParent("..")
    cmds.setParent("..")
    
    cmds.separator(height=12, style="in")

    # ========================================
    # === ESCENARIO ===
    # ========================================
    cmds.frameLayout(
        label="🏔️ Escenario",
        collapsable=True,
        collapse=True,
        marginWidth=10,
        marginHeight=8,
        backgroundColor=[0.20, 0.20, 0.24]
    )
    cmds.columnLayout(adj=True, rowSpacing=6)
    
    # === TERRENO ===
    cmds.text(label="Terreno Montañoso", font="boldLabelFont", height=22)

    cmds.button(
        label="Generar Terreno",
        c=lambda *_: generar_terreno_con_material(
            subdivisiones=50, escala=150, altura_max=27,
            octavas=4, pos_y=-35, pos_x=0, pos_z=0
        ),
        backgroundColor=[0.25, 0.45, 0.35],
        height=35
    )

    cmds.button(
    label="🎲 Color Metálico Aleatorio",
    c=lambda *_: cambiar_color_montanas_aleatorio(),
    backgroundColor=[0.45, 0.30, 0.55],
    height=32,
    annotation="Cambia el color de las montañas entre 10 paletas metálicas diferentes"
    )
    
    # Opciones avanzadas terreno
    cmds.frameLayout(label="⚙️ Opciones Avanzadas", collapsable=True, collapse=True, marginWidth=5, marginHeight=5)
    cmds.columnLayout(adj=True, rowSpacing=4)
    
    terreno_subdiv = cmds.intSliderGrp(label="Subdivisiones", min=20, max=100, value=50, field=True, columnWidth3=[90, 50, 150])
    terreno_escala = cmds.floatSliderGrp(label="Escala", min=50, max=300, value=150, field=True, columnWidth3=[90, 50, 150])
    terreno_altura = cmds.floatSliderGrp(label="Altura Máx", min=5, max=60, value=27, field=True, columnWidth3=[90, 50, 150])
    terreno_octavas = cmds.intSliderGrp(label="Detalle", min=1, max=8, value=4, field=True, columnWidth3=[90, 50, 150])
    terreno_pos_x = cmds.floatSliderGrp(label="Pos X", min=-100, max=50, value=0, field=True, columnWidth3=[90, 50, 150])
    terreno_pos_y = cmds.floatSliderGrp(label="Pos Y", min=-100, max=50, value=-35, field=True, columnWidth3=[90, 50, 150])
    terreno_pos_z = cmds.floatSliderGrp(label="Pos Z", min=-100, max=50, value=0, field=True, columnWidth3=[90, 50, 150])
    
    cmds.button(
        label="Generar Terreno Personalizado",
        c=lambda *_: generar_terreno_con_material(
            subdivisiones=cmds.intSliderGrp(terreno_subdiv, q=True, v=True),
            escala=cmds.floatSliderGrp(terreno_escala, q=True, v=True),
            altura_max=cmds.floatSliderGrp(terreno_altura, q=True, v=True),
            octavas=cmds.intSliderGrp(terreno_octavas, q=True, v=True),
            pos_x=cmds.floatSliderGrp(terreno_pos_x, q=True, v=True),
            pos_y=cmds.floatSliderGrp(terreno_pos_y, q=True, v=True),
            pos_z=cmds.floatSliderGrp(terreno_pos_z, q=True, v=True)
        ),
        backgroundColor=[0.25, 0.45, 0.35]
    )
    
    cmds.setParent('..')
    cmds.setParent('..')

    cmds.separator(height=10, style="single")

    # === NUBES ===
    cmds.text(label="Campo de Nubes", font="boldLabelFont", height=22)
    
    cmds.button(
        label="Generar Nubes",
        c=lambda *_: generar_cielo_con_material(
            num_nubes=25, radio_distribucion=100,
            altura_min=-18, altura_max=0
        ),
        backgroundColor=[0.35, 0.55, 0.75],
        height=35
    )
    
    # Opciones avanzadas nubes
    cmds.frameLayout(label="⚙️ Opciones Avanzadas", collapsable=True, collapse=True, marginWidth=5, marginHeight=5)
    cmds.columnLayout(adj=True, rowSpacing=4)
    
    nubes_cantidad = cmds.intSliderGrp(label="Cantidad", min=1, max=100, value=25, field=True, columnWidth3=[90, 50, 150])
    nubes_radio = cmds.floatSliderGrp(label="Radio Dist.", min=20, max=300, value=100, field=True, columnWidth3=[90, 50, 150])
    nubes_alt_min = cmds.floatSliderGrp(label="Altura Mín", min=-50, max=20, value=-18, field=True, columnWidth3=[90, 50, 150])
    nubes_alt_max = cmds.floatSliderGrp(label="Altura Máx", min=-20, max=50, value=0, field=True, columnWidth3=[90, 50, 150])
    
    cmds.button(
        label="Generar Nubes Personalizadas",
        c=lambda *_: generar_cielo_con_material(
            num_nubes=cmds.intSliderGrp(nubes_cantidad, q=True, v=True),
            radio_distribucion=cmds.floatSliderGrp(nubes_radio, q=True, v=True),
            altura_min=cmds.floatSliderGrp(nubes_alt_min, q=True, v=True),
            altura_max=cmds.floatSliderGrp(nubes_alt_max, q=True, v=True)
        ),
        backgroundColor=[0.35, 0.55, 0.75]
    )
    
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.setParent("..")
    cmds.setParent("..")
    
    cmds.separator(height=12, style="in")
    
    # ========================================
    # === ANIMACIÓN DE VUELO ===
    # ========================================
    cmds.frameLayout(
        label="✈️ Animación de Vuelo",
        collapsable=True,
        collapse=True,
        marginWidth=10,
        marginHeight=8,
        backgroundColor=[0.20, 0.20, 0.24]
    )
    cmds.columnLayout(adj=True, rowSpacing=8)

    cmds.text(
        label="1. Selecciona tipo de vuelo  →  2. Ajusta duración",
        font="boldLabelFont",
        align="center",
        height=25,
        backgroundColor=[0.25, 0.30, 0.35]
    )

    cmds.separator(height=8, style="none")

    # === VUELO REALISTA ===
    cmds.frameLayout(
        label="Vuelo Realista (Circular/Suave)",
        collapsable=True,
        collapse=False,
        marginWidth=8,
        marginHeight=6,
        backgroundColor=[0.22, 0.28, 0.32]
    )
    cmds.columnLayout(adj=True, rowSpacing=5)

    cmds.button(
        label="Crear Vuelo Realista",
        height=38,
        backgroundColor=[0.30, 0.50, 0.40],
        c=lambda *_: (
            crear_curva_vuelo(
                nombre="curva_vuelo_actual", radio=65, altura_base=15,
                variacion_altura=8, num_puntos=80, ondulaciones=4, tipo="circular"
            ),
            crear_controlador_vuelo(avion="CTRL_Avion", curva="curva_vuelo_actual", duracion=500)
        )
    )

    # Opciones avanzadas realista
    cmds.frameLayout(label="⚙️ Personalizar", collapsable=True, collapse=True, marginWidth=4, marginHeight=4)
    cmds.columnLayout(adj=True, rowSpacing=4)

    real_radio = cmds.floatSliderGrp(l="Radio", min=20, max=200, value=65, field=True, columnWidth3=[80, 50, 150])
    real_altura = cmds.floatSliderGrp(l="Altura Base", min=0, max=100, value=15, field=True, columnWidth3=[80, 50, 150])
    real_variacion = cmds.floatSliderGrp(l="Variación", min=0, max=30, value=8, field=True, columnWidth3=[80, 50, 150])
    real_puntos = cmds.intSliderGrp(l="Puntos", min=30, max=200, value=80, field=True, columnWidth3=[80, 50, 150])
    real_ondulaciones = cmds.intSliderGrp(l="Ondulaciones", min=0, max=15, value=4, field=True, columnWidth3=[80, 50, 150])

    real_tipo = cmds.optionMenu(l="Tipo")
    cmds.menuItem(l="Circular")
    cmds.menuItem(l="Elíptica")
    cmds.menuItem(l="Aleatorio")

    cmds.button(
        label="Aplicar Personalización",
        backgroundColor=[0.30, 0.50, 0.40],
        c=lambda *_: (
            crear_curva_vuelo(
                nombre="curva_vuelo_actual",
                radio=cmds.floatSliderGrp(real_radio, q=True, v=True),
                altura_base=cmds.floatSliderGrp(real_altura, q=True, v=True),
                variacion_altura=cmds.floatSliderGrp(real_variacion, q=True, v=True),
                num_puntos=cmds.intSliderGrp(real_puntos, q=True, v=True),
                ondulaciones=cmds.intSliderGrp(real_ondulaciones, q=True, v=True),
                tipo=cmds.optionMenu(real_tipo, q=True, v=True).lower()
            ),
            crear_controlador_vuelo(avion="CTRL_Avion", curva="curva_vuelo_actual", duracion=500)
        )
    )

    cmds.setParent('..')
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.setParent('..')

    cmds.separator(h=10, style="none")

    # === VUELO EXTREMO ===
    cmds.frameLayout(
        label="Vuelo Extremo (Acrobacias/Loops)",
        collapsable=True,
        collapse=False,
        marginWidth=8,
        marginHeight=6,
        backgroundColor=[0.32, 0.22, 0.28]
    )
    cmds.columnLayout(adj=True, rowSpacing=5)

    cmds.button(
        label="Crear Vuelo EXTREMO",
        height=38,
        backgroundColor=[0.60, 0.30, 0.40],
        c=lambda *_: (
            crear_curva_dinamica(
                nombre="curva_vuelo_actual", radio=60, altura_base=20,
                num_loops=3, num_espirales=2, num_puntos=160, intensidad=1.4
            ),
            crear_controlador_vuelo(avion="CTRL_Avion", curva="curva_vuelo_actual", duracion=500)
        )
    )

    # Opciones avanzadas extremo
    cmds.frameLayout(label="⚙️ Personalizar", collapsable=True, collapse=True, marginWidth=4, marginHeight=4)
    cmds.columnLayout(adj=True, rowSpacing=4)

    ext_radio = cmds.floatSliderGrp(l="Radio", min=30, max=150, value=60, field=True, columnWidth3=[80, 50, 150])
    ext_altura = cmds.floatSliderGrp(l="Altura", min=0, max=80, value=20, field=True, columnWidth3=[80, 50, 150])
    ext_loops = cmds.intSliderGrp(l="Loops", min=0, max=8, value=3, field=True, columnWidth3=[80, 50, 150])
    ext_espirales = cmds.intSliderGrp(l="Espirales", min=0, max=6, value=2, field=True, columnWidth3=[80, 50, 150])
    ext_puntos = cmds.intSliderGrp(l="Puntos", min=80, max=300, value=160, field=True, columnWidth3=[80, 50, 150])
    ext_intensidad = cmds.floatSliderGrp(l="Intensidad", min=0.5, max=3.0, value=1.4, step=0.1, field=True, columnWidth3=[80, 50, 150])

    cmds.button(
        label="Aplicar Personalización",
        backgroundColor=[0.60, 0.30, 0.40],
        c=lambda *_: (
            crear_curva_dinamica(
                nombre="curva_vuelo_actual",
                radio=cmds.floatSliderGrp(ext_radio, q=True, v=True),
                altura_base=cmds.floatSliderGrp(ext_altura, q=True, v=True),
                num_loops=cmds.intSliderGrp(ext_loops, q=True, v=True),
                num_espirales=cmds.intSliderGrp(ext_espirales, q=True, v=True),
                num_puntos=cmds.intSliderGrp(ext_puntos, q=True, v=True),
                intensidad=cmds.floatSliderGrp(ext_intensidad, q=True, v=True)
            ),
            crear_controlador_vuelo(avion="CTRL_Avion", curva="curva_vuelo_actual", duracion=500)
        )
    )

    cmds.setParent('..')
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.setParent('..')

    cmds.separator(h=12, style="single")

    # === CONTROLES DE ANIMACIÓN ===
    cmds.text(
        label="Control de Animación",
        font="boldLabelFont",
        align="left",
        height=25,
        backgroundColor=[0.25, 0.30, 0.35]
    )

    duracion_anim = cmds.intSliderGrp(
        l="Duración (frames)",
        min=100, max=3000, value=600,
        field=True,
        columnWidth3=[110, 60, 130]
    )

    cmds.rowLayout(numberOfColumns=2, columnWidth2=(165, 165), columnAttach=[(1, "both", 2), (2, "both", 2)])
    cmds.button(
        label="▶️ Ajustar Duración",
        height=40,
        backgroundColor=[0.35, 0.50, 0.60],
        c=lambda *_: crear_controlador_vuelo(
            avion="CTRL_Avion",
            curva="curva_vuelo_actual",
            duracion=cmds.intSliderGrp(duracion_anim, q=True, v=True)
        )
    )
    cmds.button(
        label="⏹️ Detener Vuelo",
        height=40,
        backgroundColor=[0.60, 0.35, 0.35],
        c=lambda *_: eliminar_vuelo()
    )
    cmds.setParent('..')

    cmds.setParent('..')
    cmds.setParent('..')

    cmds.separator(height=20, style="none")
        
    cmds.showWindow(window)


if __name__ == "__main__":
    crear_ui()