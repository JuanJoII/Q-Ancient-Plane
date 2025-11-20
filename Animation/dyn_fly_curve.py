import maya.cmds as cmds
import math
import random

def crear_curva_dinamica(nombre="curva_vuelo", radio=60, altura_base=20,
                            num_loops=2, num_espirales=2, num_puntos=100,
                            intensidad=1.2):
    """
    Crea una curva tipo montaña rusa con loops, espirales y giros extremos
    
    Args:
        nombre: Nombre de la curva
        radio: Radio base de la trayectoria
        altura_base: Altura central del recorrido
        num_loops: Número de loops verticales (volteretas)
        num_espirales: Número de espirales tipo sacacorchos
        num_puntos: Cantidad de puntos (más = más suave)
        intensidad: Multiplicador de dramatismo (0.5 = suave, 2.0 = extremo)
    """
    
    # Eliminar curva previa si existe
    if cmds.objExists(nombre):
        print(f"Eliminando curva previa: {nombre}")
        cmds.delete(nombre)
    
    puntos = []
    segmentos = []
    
    # Calcular cuántos puntos por segmento
    puntos_por_loop = int(num_puntos * 0.15) if num_loops > 0 else 0
    puntos_por_espiral = int(num_puntos * 0.2) if num_espirales > 0 else 0
    puntos_normales = num_puntos - (num_loops * puntos_por_loop) - (num_espirales * puntos_por_espiral)
    
    segmentos.append(("normal", puntos_normales))
    
    # Distribuir loops y espirales
    for _ in range(num_loops):
        segmentos.append(("loop", puntos_por_loop))
    for _ in range(num_espirales):
        segmentos.append(("espiral", puntos_por_espiral))
    
    # Mezclar aleatoriamente los segmentos especiales
    random.shuffle(segmentos[1:])
    
    punto_actual = 0
    angulo_acumulado = 0
    
    for tipo_segmento, cantidad_puntos in segmentos:
        for i in range(cantidad_puntos):
            progreso = punto_actual / num_puntos
            angulo_base = progreso * 2 * math.pi
            
            if tipo_segmento == "normal":
                # Vuelo normal con ondulaciones
                x = math.cos(angulo_base) * radio
                z = math.sin(angulo_base) * radio
                y = altura_base + math.sin(angulo_base * 3) * (10 * intensidad)
                
            elif tipo_segmento == "loop":
                # Loop vertical (voltereta)
                progreso_loop = i / cantidad_puntos
                angulo_loop = progreso_loop * 2 * math.pi
                
                # Posición base en el círculo principal
                x_base = math.cos(angulo_base) * radio
                z_base = math.sin(angulo_base) * radio
                
                # Radio del loop
                radio_loop = radio * 0.3 * intensidad
                
                # Crear el loop en el plano vertical
                x = x_base + math.cos(angulo_loop) * radio_loop * 0.3
                y = altura_base + math.sin(angulo_loop) * radio_loop
                z = z_base
                
            elif tipo_segmento == "espiral":
                # Espiral tipo sacacorchos
                progreso_espiral = i / cantidad_puntos
                vueltas = 3  # Número de vueltas completas en la espiral
                angulo_espiral = progreso_espiral * vueltas * 2 * math.pi
                
                # Radio de la espiral (decrece hacia el centro)
                radio_espiral = radio * 0.4 * intensidad * (1 - progreso_espiral * 0.3)
                
                # Posición en espiral
                x = math.cos(angulo_base) * radio + math.cos(angulo_espiral) * radio_espiral
                z = math.sin(angulo_base) * radio + math.sin(angulo_espiral) * radio_espiral
                y = altura_base + (progreso_espiral - 0.5) * 15 * intensidad
            
            puntos.append((x, y, z))
            punto_actual += 1
    
    # Agregar punto final que conecte con el inicio
    puntos.append(puntos[0])
    
    # Crear la curva NURBS
    curva = cmds.curve(p=puntos, degree=3, name=nombre)
    
    # Cerrar la curva
    cmds.closeCurve(curva, ch=False, preserveShape=False, replaceOriginal=True)
    
    # Reconstruir para suavizar
    cmds.rebuildCurve(
        curva,
        ch=False,
        rpo=True,
        rt=0,
        end=1,
        kr=0,
        kcp=False,
        kep=True,
        kt=False,
        spans=num_puntos,
        degree=3,
        tolerance=0.01
    )
    
    print(f"Curva tipo montaña rusa '{nombre}' creada con {num_loops} loops y {num_espirales} espirales")
    return curva

if __name__ == '__main__':
    crear_curva_dinamica()