import maya.cmds as cmds
import math
from Utils.seed import generate_seed

def crear_terreno_montanoso(nombre="terreno", subdivisiones=50, escala=150, 
                            altura_max=27, octavas=4, seed=None,
                            pos_x=0, pos_y=-35, pos_z=0):
    """
    Crea un terreno fractal tipo montañoso.
    
    Args:
        nombre: Nombre del objeto.
        subdivisiones: Resolución del plano (más = más detalle).
        escala: Tamaño del terreno.
        altura_max: Altura máxima de las montañas.
        octavas: Niveles de detalle del fractal (más = más detallado).
        seed: Semilla para generación procedural (None = aleatoria).
        pos_x, pos_y, pos_z: Posición del terreno en el espacio 3D.
    """
    # Generar o usar semilla
    if seed is None:
        seed = generate_seed()
    
    print(f"Generando terreno con semilla: {seed}")
    
    # Crear plano base
    plano = cmds.polyPlane(name=nombre, w=escala, h=escala, 
                           sx=subdivisiones, sy=subdivisiones)[0]
    
    # Obtener vértices
    num_vertices = cmds.polyEvaluate(plano, v=True)
    
    # Aplicar desplazamiento fractal a cada vértice
    for i in range(num_vertices):
        pos = cmds.pointPosition(f"{plano}.vtx[{i}]")
        x, y, z = pos
        altura = 0
        amplitud = altura_max
        frecuencia = 1.0 / escala
        
        for octava in range(octavas):
            offset_base = seed + octava * 1000
            offset_multiplier_1 = math.sin(offset_base * 0.001) * 10
            offset_multiplier_2 = math.cos(offset_base * 0.001) * 10
            
            seed_x = x * frecuencia + octava * 100 + offset_multiplier_1
            seed_z = z * frecuencia + octava * 100 + offset_multiplier_2
            
            noise = (math.sin(seed_x * 2.5) * math.cos(seed_z * 3.7) + 
                     math.sin(seed_x * 1.3 + seed_z * 2.1) * 0.5 +
                     math.cos(seed_x * 4.2 - seed_z * 1.8) * 0.25)
            
            altura += noise * amplitud
            amplitud *= 0.5
            frecuencia *= 2
        
        cmds.move(0, altura, 0, f"{plano}.vtx[{i}]", relative=True)
    
    # Suavizar el terreno
    cmds.polySmooth(plano, divisions=1)
    
    # ✅ Mover el terreno a su posición final
    cmds.move(pos_x, pos_y, pos_z, plano, absolute=True)
    
    print(f"Terreno '{nombre}' creado en posición ({pos_x}, {pos_y}, {pos_z})")
    print(f"Semilla usada: {seed}")
    
    return plano


if __name__ == "__main__":
    crear_terreno_montanoso()