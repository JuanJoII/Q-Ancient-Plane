import maya.cmds as cmds
from Utils.tools import generar_parte
from Utils.emerge import emerge_plane
from PlaneRig import create_joints, spline_auto_rig
from Environment.terrain import crear_terreno_montanoso
from Environment.cloud import crear_campo_nubes


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
    
    cmds.setParent("..")  # Salir columnLayout interno
    cmds.setParent("..")  # Salir frameLayout
    
    cmds.separator(height=12, style="in")
    
    # Botón final
    
    cmds.setParent("..")
    cmds.showWindow("GeneradorAvion")

if __name__ == "__main__":
    crear_ui()
