import maya.cmds as cmds
import random
import math
from Utils.soft_edges import soften_edges_en_grupo

def crear_nube(nombre="nube", posicion=(0, 0, 0), escala=5, densidad=10):
    """
    Crea una nube volumétrica usando cubos biselados agrupados
    """
    grupo_nube = cmds.group(empty=True, name=nombre)
    
    for i in range(densidad):
        offset_x = random.uniform(-escala, escala)
        offset_y = random.uniform(-escala * 0.3, escala * 0.3)
        offset_z = random.uniform(-escala * 0.7, escala * 0.7)
        tamanio = random.uniform(escala * 0.3, escala * 0.8)
        
        # Crear cubo en lugar de esfera
        cubo = cmds.polyCube(
            w=tamanio, 
            h=tamanio, 
            d=tamanio, 
            sx=1, sy=1, sz=1,
            name=f"{nombre}_parte_{i}"
        )[0]
        
        # Aplicar bevel a las aristas del cubo
        try:
            cmds.polyBevel3(
                cubo,
                fraction=0.2,           # Tamaño del bisel (20% del edge)
                offsetAsFraction=True,
                autoFit=True,
                depth=1,
                mitering=0,             # Sin mitering para bordes más suaves
                miterAlong=0,
                chamfer=True,
                segments=2,             # Segmentos del bisel
                worldSpace=True,
                smoothingAngle=30,
                subdivideNgons=True,
                mergeVertices=True,
                mergeVertexTolerance=0.0001,
                miteringAngle=180,
                angleTolerance=180,
                ch=True
            )
        except Exception as e:
            cmds.warning(f"No se pudo aplicar bevel al cubo {cubo}: {e}")
        
        # Posicionar el cubo
        cmds.move(posicion[0] + offset_x, 
                 posicion[1] + offset_y, 
                 posicion[2] + offset_z, 
                 cubo)
        
        # Rotación aleatoria para más variedad
        cmds.rotate(
            random.uniform(0, 360),
            random.uniform(0, 360),
            random.uniform(0, 360),
            cubo
        )
        
        cmds.parent(cubo, grupo_nube)
    
    return grupo_nube


def crear_campo_nubes(num_nubes=10, radio_distribucion=100, altura_min=-18, altura_max=0):
    """
    Crea múltiples nubes distribuidas alrededor de la escena
    """
    nombre_grupo = "campo_nubes"

    # ELIMINAR GRUPO PREVIO SI EXISTE
    if cmds.objExists(nombre_grupo):
        print(f"Eliminando grupo previo: {nombre_grupo}")
        cmds.delete(nombre_grupo)
    
    grupo_nubes = cmds.group(empty=True, name=nombre_grupo)
    
    for i in range(num_nubes):
        angulo = random.uniform(0, 2 * math.pi)
        distancia = random.uniform(radio_distribucion * 0.3, radio_distribucion)
        
        x = math.cos(angulo) * distancia
        z = math.sin(angulo) * distancia
        y = random.uniform(altura_min, altura_max)
        escala = random.uniform(4, 8)
        
        nube = crear_nube(
            nombre=f"nube_{i+1}", 
            posicion=(x, y, z), 
            escala=escala,
            densidad=random.randint(6, 10)
        )
        
        # Suavizar bordes
        try:
            cmds.polySoftEdge(nube, angle=180, ch=False)
        except Exception as e:
            cmds.warning(f"No se pudo suavizar la nube {nube}: {e}")
        
        cmds.parent(nube, grupo_nubes)
    
    print(f"Campo de nubes creado con {num_nubes} nubes. Grupo: '{nombre_grupo}'")
    soften_edges_en_grupo(nombre_grupo, angle=180, keep_history=False)
    return grupo_nubes


if __name__ == "__main__":
    crear_campo_nubes(num_nubes=25)