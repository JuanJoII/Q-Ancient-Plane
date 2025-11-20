import maya.cmds as cmds
import math
import random

def crear_curva_vuelo(nombre="curva_vuelo", radio=65, altura_base=15, 
                      variacion_altura=8, num_puntos=50, ondulaciones=4,
                      tipo="circular"):
    """
    Crea una curva suave para que el avión la siga en su vuelo
    
    Args:
        nombre: Nombre de la curva
        radio: Radio de la trayectoria circular
        altura_base: Altura promedio del vuelo
        variacion_altura: Cuánto sube/baja el avión
        num_puntos: Cantidad de puntos de control (más = más suave)
        ondulaciones: Número de subidas/bajadas en el recorrido
        tipo: "circular", "eliptica", o "aleatorio"
    """
    
    # Eliminar curva previa si existe
    if cmds.objExists(nombre):
        print(f"Eliminando curva previa: {nombre}")
        cmds.delete(nombre)
    
    puntos = []
    
    for i in range(num_puntos + 1):  # +1 para cerrar el loop
        # Ángulo actual en el recorrido
        angulo = (i / num_puntos) * 2 * math.pi
        
        # Posición base circular o elíptica
        if tipo == "eliptica":
            x = math.cos(angulo) * radio
            z = math.sin(angulo) * radio * 0.6  # Elipse más estrecha
        elif tipo == "aleatorio":
            # Trayectoria más errática
            variacion = random.uniform(0.7, 1.3)
            x = math.cos(angulo) * radio * variacion
            z = math.sin(angulo) * radio * variacion
        else:  # circular
            x = math.cos(angulo) * radio
            z = math.sin(angulo) * radio
        
        # Variación de altura con ondulaciones suaves (seno)
        fase_altura = (i / num_puntos) * ondulaciones * 2 * math.pi
        y = altura_base + math.sin(fase_altura) * variacion_altura
        
        # Agregar pequeñas variaciones aleatorias para naturalidad
        if tipo == "aleatorio":
            x += random.uniform(-radio * 0.1, radio * 0.1)
            y += random.uniform(-variacion_altura * 0.2, variacion_altura * 0.2)
            z += random.uniform(-radio * 0.1, radio * 0.1)
        
        puntos.append((x, y, z))
    
    # Crear la curva NURBS
    curva = cmds.curve(p=puntos, degree=3, name=nombre)
    
    # Hacer la curva periódica (cerrada) para loop infinito
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
    
    print(f"Curva de vuelo '{nombre}' creada exitosamente")
    return curva

if __name__ == '__main__':
    crear_curva_vuelo()