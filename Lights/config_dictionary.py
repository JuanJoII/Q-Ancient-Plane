"""
Configuración de paletas de colores para skydomos
"""

PALETAS_CIELO = {
    "diurno": {
        "nombre": "Cielo Diurno Azul",
        "colores": [
            (0.7, 0.85, 1.0),    # Horizonte claro
            (0.3, 0.6, 0.95),    # Medio
            (0.1, 0.3, 0.7)      # Alto oscuro
        ],
        "intensidad": 0.5
    },
    
    "atardecer": {
        "nombre": "Atardecer Cálido",
        "colores": [
            (1.0, 0.7, 0.4),     # Horizonte naranja
            (0.9, 0.5, 0.6),     # Medio rosa
            (0.3, 0.2, 0.5)      # Alto púrpura
        ],
        "intensidad": 0.45
    },
    
    "noche": {
        "nombre": "Noche Estrellada",
        "colores": [
            (0.05, 0.08, 0.15),  # Horizonte oscuro
            (0.02, 0.05, 0.12),  # Medio muy oscuro
            (0.01, 0.02, 0.08)   # Alto negro azulado
        ],
        "intensidad": 0.15
    },
    
    "amanecer": {
        "nombre": "Amanecer Dorado",
        "colores": [
            (1.0, 0.85, 0.6),    # Horizonte dorado
            (0.8, 0.7, 0.9),     # Medio lavanda
            (0.4, 0.5, 0.8)      # Alto azul suave
        ],
        "intensidad": 0.4
    },
    
    "tormenta": {
        "nombre": "Tormenta Dramática",
        "colores": [
            (0.3, 0.35, 0.4),    # Horizonte gris
            (0.2, 0.22, 0.28),   # Medio gris oscuro
            (0.12, 0.12, 0.18)   # Alto casi negro
        ],
        "intensidad": 0.25
    },
    
    "crepusculo": {
        "nombre": "Crepúsculo Violeta",
        "colores": [
            (0.6, 0.4, 0.8),     # Horizonte violeta
            (0.4, 0.25, 0.6),    # Medio púrpura
            (0.15, 0.1, 0.3)     # Alto morado oscuro
        ],
        "intensidad": 0.35
    },
    
    "desierto": {
        "nombre": "Desierto Cálido",
        "colores": [
            (1.0, 0.9, 0.7),     # Horizonte amarillo cálido
            (0.9, 0.7, 0.5),     # Medio naranja suave
            (0.6, 0.5, 0.7)      # Alto azul cálido
        ],
        "intensidad": 0.5
    },
    
    "aurora": {
        "nombre": "Aurora Boreal",
        "colores": [
            (0.2, 0.6, 0.5),     # Horizonte verde azulado
            (0.3, 0.4, 0.8),     # Medio azul eléctrico
            (0.1, 0.2, 0.4)      # Alto azul oscuro
        ],
        "intensidad": 0.35
    },
    
    "alienigena": {
        "nombre": "Cielo Alienígena",
        "colores": [
            (0.6, 0.9, 0.95),    # Horizonte cyan brillante
            (0.8, 0.4, 0.9),     # Medio magenta
            (0.3, 0.15, 0.5)     # Alto púrpura oscuro
        ],
        "intensidad": 0.45
    },
    
    "infierno": {
        "nombre": "Infierno",
        "colores": [
            (1.0, 0.5, 0.2),     # Horizonte naranja fuego
            (0.8, 0.2, 0.15),    # Medio rojo oscuro
            (0.3, 0.1, 0.05)     # Alto rojo muy oscuro
        ],
        "intensidad": 0.4
    },
}

# Lista de claves para acceso aleatorio
TIPOS_CIELO = list(PALETAS_CIELO.keys())