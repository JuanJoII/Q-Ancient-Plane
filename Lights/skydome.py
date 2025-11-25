"""
Funciones para crear y manipular SkyDome lights con paletas de colores
"""

import random
import maya.cmds as cmds
from .config_dictionary import PALETAS_CIELO, TIPOS_CIELO


# Constantes
SKYDOME_NAME = "SkyDome_Light"
RAMP_NAME = "SkyDome_Ramp"


def crear_skydome_con_variaciones():
    """
    Crea un SkyDome Light con ramp configurable para cielos variados.
    Requiere Arnold (mtoa) cargado.
    
    Returns:
        str: Nombre del skydome creado o None si falla
    """
    if not cmds.pluginInfo('mtoa', query=True, loaded=True):
        cmds.warning("Arnold no está cargado. No se puede crear SkyDome.")
        return None
    
    # Si ya existe, eliminarlo completamente primero
    if cmds.objExists(SKYDOME_NAME):
        print(f"[i] SkyDome '{SKYDOME_NAME}' ya existe. Eliminando para recrear...")
        _eliminar_skydome_completo()
    
    # Crear SkyDome Light
    skydome = cmds.shadingNode('aiSkyDomeLight', asLight=True, name=SKYDOME_NAME)
    cmds.setAttr(f"{skydome}.intensity", 0.4)
    
    # Crear y configurar ramp
    _crear_ramp_cielo()
    
    print("[✓] SkyDome Light con ramp de cielo creado.")
    return SKYDOME_NAME


def _crear_ramp_cielo():
    """
    Crea el ramp de textura para el skydome y lo conecta.
    Configura colores por defecto de cielo diurno.
    """
    # Si el ramp ya existe, eliminarlo primero
    if cmds.objExists(RAMP_NAME):
        cmds.delete(RAMP_NAME)
    
    ramp_sky = cmds.shadingNode("ramp", asTexture=True, name=RAMP_NAME)
    
    # Configurar como V Ramp (vertical)
    cmds.setAttr(f"{ramp_sky}.type", 0)
    cmds.setAttr(f"{ramp_sky}.interpolation", 1)  # Linear
    
    # Aplicar paleta diurna por defecto
    _aplicar_paleta_a_ramp(PALETAS_CIELO["diurno"])
    
    # Conectar ramp al color del skydome
    cmds.connectAttr(f"{ramp_sky}.outColor", f"{SKYDOME_NAME}.color", force=True)


def _eliminar_skydome_completo():
    """
    Elimina completamente el skydome y todos sus nodos asociados (ramp, place2dTexture, etc.)
    """
    elementos_a_eliminar = []
    
    # Agregar el skydome si existe
    if cmds.objExists(SKYDOME_NAME):
        elementos_a_eliminar.append(SKYDOME_NAME)
    
    # Agregar el ramp si existe
    if cmds.objExists(RAMP_NAME):
        elementos_a_eliminar.append(RAMP_NAME)
        
        # También eliminar el place2dTexture conectado al ramp
        conexiones = cmds.listConnections(RAMP_NAME, source=True, destination=False)
        if conexiones:
            for conn in conexiones:
                if cmds.nodeType(conn) == "place2dTexture":
                    elementos_a_eliminar.append(conn)
    
    # Eliminar todos los elementos encontrados
    if elementos_a_eliminar:
        try:
            cmds.delete(elementos_a_eliminar)
            print(f"[✓] Elementos eliminados: {', '.join(elementos_a_eliminar)}")
        except Exception as e:
            cmds.warning(f"Error al eliminar elementos del skydome: {e}")


def cambiar_cielo_aleatorio():
    """
    Cambia el cielo a una paleta aleatoria.
    Crea el skydome si no existe.
    
    Returns:
        str: Nombre de la paleta aplicada o None si falla
    """
    # Si no existe, crearlo primero
    if not cmds.objExists(SKYDOME_NAME):
        crear_skydome_con_variaciones()
    
    if not _verificar_skydome_existe():
        return None
    
    # Seleccionar paleta aleatoria
    tipo_elegido = random.choice(TIPOS_CIELO)
    paleta = PALETAS_CIELO[tipo_elegido]
    
    # Aplicar paleta
    _aplicar_paleta_a_ramp(paleta)
    cmds.setAttr(f"{SKYDOME_NAME}.intensity", paleta["intensidad"])
    
    print(f"[✓] Cielo cambiado a: {paleta['nombre']}")
    return paleta["nombre"]


def aplicar_cielo_especifico(tipo_cielo):
    """
    Aplica un tipo de cielo específico por nombre.
    Crea el skydome si no existe.
    
    Args:
        tipo_cielo (str): Tipo de cielo a aplicar. Opciones:
            "diurno", "atardecer", "noche", "amanecer", "tormenta",
            "crepusculo", "desierto", "aurora", "alienigena", "infierno"
    
    Returns:
        bool: True si se aplicó correctamente, False si falló
    """
    # Si no existe, crearlo primero
    if not cmds.objExists(SKYDOME_NAME):
        crear_skydome_con_variaciones()
    
    if not _verificar_skydome_existe():
        return False
    
    tipo_cielo_lower = tipo_cielo.lower()
    
    if tipo_cielo_lower not in PALETAS_CIELO:
        tipos_disponibles = ", ".join(TIPOS_CIELO)
        cmds.warning(
            f"Tipo de cielo '{tipo_cielo}' no reconocido. "
            f"Disponibles: {tipos_disponibles}"
        )
        return False
    
    paleta = PALETAS_CIELO[tipo_cielo_lower]
    
    # Aplicar paleta
    _aplicar_paleta_a_ramp(paleta)
    cmds.setAttr(f"{SKYDOME_NAME}.intensity", paleta["intensidad"])
    
    print(f"[✓] Cielo configurado como: {paleta['nombre']}")
    return True


def _verificar_skydome_existe():
    """
    Verifica que el skydome y el ramp existan.
    
    Returns:
        bool: True si ambos existen, False si falta alguno
    """
    if not cmds.objExists(SKYDOME_NAME):
        cmds.warning(f"No existe el SkyDome '{SKYDOME_NAME}'. Créalo primero con crear_skydome_con_variaciones().")
        return False
    
    if not cmds.objExists(RAMP_NAME):
        cmds.warning(f"No existe el Ramp '{RAMP_NAME}'.")
        return False
    
    return True


def _aplicar_paleta_a_ramp(paleta):
    """
    Aplica los colores de una paleta al ramp del skydome.
    
    Args:
        paleta (dict): Diccionario con 'colores' (lista de 3 tuplas RGB)
    """
    colores = paleta["colores"]
    
    # Aplicar los 3 colores (horizonte, medio, alto)
    cmds.setAttr(f"{RAMP_NAME}.colorEntryList[0].position", 0.0)
    cmds.setAttr(f"{RAMP_NAME}.colorEntryList[0].color", 
                 *colores[0], type="double3")
    
    cmds.setAttr(f"{RAMP_NAME}.colorEntryList[1].position", 0.5)
    cmds.setAttr(f"{RAMP_NAME}.colorEntryList[1].color", 
                 *colores[1], type="double3")
    
    cmds.setAttr(f"{RAMP_NAME}.colorEntryList[2].position", 1.0)
    cmds.setAttr(f"{RAMP_NAME}.colorEntryList[2].color", 
                 *colores[2], type="double3")


def listar_cielos_disponibles():
    """
    Imprime todos los tipos de cielo disponibles.
    
    Returns:
        list: Lista de tipos de cielo disponibles
    """
    print("\n🌈 Cielos disponibles:")
    for i, tipo in enumerate(TIPOS_CIELO, 1):
        nombre = PALETAS_CIELO[tipo]["nombre"]
        print(f"  {i}. '{tipo}' - {nombre}")
    print()
    return TIPOS_CIELO