import maya.cmds as cmds
import random
import math

def crear_nube(nombre="nube", posicion=(0, 0, 0), escala=5, densidad=10):
    """
    Crea una nube volumétrica usando esferas agrupadas
    
    Args:
        nombre: Nombre de la nube
        posicion: Posición (x, y, z)
        escala: Tamaño general de la nube
        densidad: Número de esferas (más = más densa)
    """
    grupo_nube = cmds.group(empty=True, name=nombre)
    
    # Crear múltiples esferas para simular volumen
    for i in range(densidad):
        # Posición aleatoria dentro de un volumen elipsoidal
        offset_x = random.uniform(-escala, escala)
        offset_y = random.uniform(-escala * 0.3, escala * 0.3)  # Más plana
        offset_z = random.uniform(-escala * 0.7, escala * 0.7)
        
        # Tamaño aleatorio
        radio = random.uniform(escala * 0.3, escala * 0.8)
        
        # Crear esfera
        esfera = cmds.polySphere(r=radio, sx=12, sy=12, name=f"{nombre}_parte_{i}")[0]
        
        # Posicionar
        cmds.move(posicion[0] + offset_x, 
                 posicion[1] + offset_y, 
                 posicion[2] + offset_z, 
                 esfera)
        
        # Agrupar
        cmds.parent(esfera, grupo_nube)
    
    # Aplicar shader blanco semi-transparente
    shader = cmds.shadingNode('lambert', asShader=True, name=f"{nombre}_shader")
    cmds.setAttr(f"{shader}.color", 0.95, 0.95, 1.0, type='double3')
    cmds.setAttr(f"{shader}.transparency", 0.3, 0.3, 0.3, type='double3')
    
    cmds.select(grupo_nube, hierarchy=True)
    cmds.hyperShade(assign=shader)
    
    return grupo_nube


def crear_campo_nubes(num_nubes=10, radio_distribucion=100, altura_min=-18, altura_max=0):
    """
    Crea múltiples nubes distribuidas alrededor de la escena
    
    Args:
        num_nubes: Cantidad de nubes a crear
        radio_distribucion: Radio del área donde aparecerán las nubes
        altura_min: Altura mínima de las nubes
        altura_max: Altura máxima de las nubes
    """
    grupo_nubes = cmds.group(empty=True, name="campo_nubes")
    
    for i in range(num_nubes):
        # Posición aleatoria en círculo
        angulo = random.uniform(0, 2 * math.pi)
        distancia = random.uniform(radio_distribucion * 0.3, radio_distribucion)
        
        x = math.cos(angulo) * distancia
        z = math.sin(angulo) * distancia
        y = random.uniform(altura_min, altura_max)
        
        # Tamaño aleatorio
        escala = random.uniform(4, 8)
        
        # Crear nube (asumiendo que tu función crear_nube() retorna el nombre del objeto)
        nube = crear_nube(
            nombre=f"nube_{i+1}", 
            posicion=(x, y, z), 
            escala=escala,
            densidad=random.randint(6, 10)
        )
        
        # 🔹 Suavizar los bordes de la nube
        try:
            cmds.polySoftEdge(nube, angle=180, ch=False)
        except Exception as e:
            cmds.warning(f"No se pudo suavizar la nube {nube}: {e}")
        
        # Agrupar
        cmds.parent(nube, grupo_nubes)
    
    print(f"Campo de nubes creado con {num_nubes} nubes suavizadas.")
    return grupo_nubes

def soften_edges_en_grupo(nombre_grupo, angle=180, keep_history=False, verbose=True):
    """
    Aplica polySoftEdge a todas las mallas (meshes) dentro de un grupo dado.
    
    Args:
        nombre_grupo (str): Nombre exacto del grupo o patrón (acepta wildcards, p.e. 'campo_nubes*').
        angle (float): Ángulo de suavizado (por defecto 180 = suavizado total).
        keep_history (bool): Si True, mantiene construction history (ch=True). Por defecto False.
        verbose (bool): Si True, imprime mensajes informativos.
    
    Retorna:
        lista de transforms a los que se aplicó soften edge.
    """
    # Buscar coincidencias (soporta patrones tipo 'nombre*')
    grupos = cmds.ls(nombre_grupo, long=True) or []
    if not grupos:
        if verbose:
            cmds.warning(f"No se encontró ningún nodo que coincida con '{nombre_grupo}'.")
        return []

    applied = []
    for grp in grupos:
        # Obtener todas las shapes tipo mesh descendientes
        meshes = cmds.listRelatives(grp, allDescendents=True, type='mesh', fullPath=True) or []
        if not meshes:
            if verbose:
                cmds.warning(f"El grupo '{grp}' no contiene mallas (meshes).")
            continue

        # Convertir shapes a sus transforms padres (evitar duplicados)
        transforms = []
        for mesh in meshes:
            parents = cmds.listRelatives(mesh, parent=True, fullPath=True) or []
            for p in parents:
                if p not in transforms:
                    transforms.append(p)

        # Aplicar polySoftEdge a cada transform encontrado
        for t in transforms:
            try:
                cmds.polySoftEdge(t, angle=angle, ch=keep_history)
                applied.append(t)
                if verbose:
                    print(f"Soften edge aplicado a: {t} (angle={angle}, ch={keep_history})")
            except Exception as e:
                cmds.warning(f"No se pudo aplicar soften edge a {t}: {e}")

    if verbose:
        if applied:
            print(f"Soften edge aplicado a {len(applied)} transform(s).")
        else:
            print("No se aplicó soften edge a ningún transform.")
    return applied


if __name__ == "__main__":
    crear_campo_nubes(num_nubes=25)
    soften_edges_en_grupo("campo_nubes", angle=180, keep_history=False)