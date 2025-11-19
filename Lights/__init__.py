"""
Módulo de iluminación para Maya
Proporciona configuración de luces y skydomos con paletas variadas
"""

from .lights_setup import setup_lights
from .skydome import (
    crear_skydome_con_variaciones,
    cambiar_cielo_aleatorio,
    aplicar_cielo_especifico
)
from .config_dictionary import PALETAS_CIELO

__all__ = [
    'setup_lights',
    'crear_skydome_con_variaciones',
    'cambiar_cielo_aleatorio',
    'aplicar_cielo_especifico',
    'PALETAS_CIELO'
]

__version__ = '1.0.0'