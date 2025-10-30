import maya.cmds as cmds
from utils.tools import generar_parte

def crear_ui():
    if cmds.window("GeneradorAvion", exists=True):
        cmds.deleteUI("GeneradorAvion")

    cmds.window("GeneradorAvion", title="Generador Procedural de Avión - QAP", widthHeight=(300, 260))
    cmds.columnLayout(adj=True, rowSpacing=6)
    cmds.text(label="Modelo Procedural QAP", align="center", height=25)

    cmds.button(label="Generar Fuselaje", c=lambda *_: generar_parte("FUSELAJE"))
    cmds.button(label="Generar Alas", c=lambda *_: generar_parte("ALAS"))
    cmds.button(label="Generar Cabeza", c=lambda *_: generar_parte("CABEZA"))
    cmds.button(label="Generar Cola", c=lambda *_: generar_parte("COLA"))
    cmds.button(label="Generar Ornamentación", c=lambda *_: generar_parte("ORNAMENTACION"))

    cmds.setParent("..")
    cmds.showWindow("GeneradorAvion")