"""
Configuración principal de luces para escenas de Maya
"""

import maya.cmds as cmds
from .skydome import crear_skydome_con_variaciones


def setup_lights():
    """
    Configura un sistema de iluminación de 3 puntos más skydome.
    Elimina luces previas y crea una configuración profesional.
    """
    print("💡 Configurando luces de escena...")

    # Eliminar luces previas si existen (incluyendo grupos vacíos)
    _limpiar_luces_existentes()

    # Crear sistema de 3 puntos
    _crear_luz_principal()
    _crear_luz_relleno()
    _crear_luz_trasera()

    # Crear skydome si Arnold está disponible
    if cmds.pluginInfo('mtoa', query=True, loaded=True):
        crear_skydome_con_variaciones()
        print("[✓] SkyDome Light con ramp de cielo creado.")
    else:
        print("[i] Arnold no disponible, skydome omitido.")

    print("✅ Iluminación configurada correctamente.")


def _limpiar_luces_existentes():
    """
    Elimina todas las luces existentes en la escena, incluyendo sus transforms
    y cualquier grupo vacío resultante.
    """
    tipos_luces = ["directionalLight", "pointLight", "areaLight", "spotLight", "aiSkyDomeLight"]
    
    # Obtener todos los nodos de luz
    luces_shape = cmds.ls(type=tipos_luces)
    
    if luces_shape:
        transforms_a_eliminar = []
        
        # Para cada luz (shape node), obtener su transform padre
        for luz in luces_shape:
            # Obtener el transform padre
            parents = cmds.listRelatives(luz, parent=True, fullPath=True)
            if parents:
                transforms_a_eliminar.extend(parents)
        
        # Eliminar los transforms (esto también elimina los shapes)
        if transforms_a_eliminar:
            try:
                cmds.delete(transforms_a_eliminar)
                print(f"[i] {len(transforms_a_eliminar)} luces anteriores eliminadas.")
            except Exception as e:
                cmds.warning(f"Error al eliminar luces: {e}")
    
    # Limpiar grupos vacíos que pudieran haber quedado
    _limpiar_grupos_vacios()


def _limpiar_grupos_vacios():
    """
    Elimina transforms vacíos que no tengan hijos ni shapes.
    Útil para limpiar grupos que quedaron después de eliminar luces.
    """
    all_transforms = cmds.ls(type='transform')
    grupos_vacios = []
    
    for transform in all_transforms:
        # Verificar si es un transform sin children y sin shapes
        children = cmds.listRelatives(transform, children=True, fullPath=True)
        
        # Si no tiene hijos, es candidato para eliminación
        if not children:
            # Verificar que no sea una cámara default o un objeto especial
            if not _es_objeto_protegido(transform):
                grupos_vacios.append(transform)
    
    if grupos_vacios:
        try:
            cmds.delete(grupos_vacios)
            print(f"[i] {len(grupos_vacios)} grupos vacíos eliminados.")
        except Exception as e:
            cmds.warning(f"Algunos grupos no pudieron eliminarse: {e}")


def _es_objeto_protegido(nombre_objeto):
    """
    Verifica si un objeto es parte de la escena default de Maya y no debe eliminarse.
    
    Args:
        nombre_objeto (str): Nombre del objeto a verificar
    
    Returns:
        bool: True si es un objeto protegido, False si puede eliminarse
    """
    objetos_protegidos = [
        'persp', 'top', 'front', 'side',  # Cámaras default
        'perspShape', 'topShape', 'frontShape', 'sideShape',
        'defaultLightSet', 'defaultObjectSet',
        'initialShadingGroup', 'initialParticleSE',
        'defaultRenderGlobals', 'defaultResolution',
        'defaultLightList1', 'defaultShaderList1',
        'postProcessList1', 'defaultRenderUtilityList1',
        'defaultRenderingList1', 'lightLinker1',
        'shapeEditorManager', 'poseInterpolatorManager',
        'layerManager', 'defaultLayer',
        'renderLayerManager', 'defaultRenderLayer',
    ]
    
    # Verificar nombre exacto
    if nombre_objeto in objetos_protegidos:
        return True
    
    # Verificar si contiene algún patrón protegido
    for protegido in objetos_protegidos:
        if protegido in nombre_objeto:
            return True
    
    return False


def _crear_luz_principal():
    """Crea la luz direccional principal (key light)"""
    luz = cmds.directionalLight(name="Main_Directional_Light", intensity=1.2)
    transform = cmds.listRelatives(luz, parent=True)[0]
    
    cmds.setAttr(f"{transform}.rotateX", -45)
    cmds.setAttr(f"{transform}.rotateY", 30)
    cmds.setAttr(f"{transform}.rotateZ", 0)
    
    print("[✓] Luz direccional principal creada.")
    return transform


def _crear_luz_relleno():
    """Crea la luz de relleno (fill light)"""
    luz = cmds.directionalLight(name="Fill_Light", intensity=0.6)
    transform = cmds.listRelatives(luz, parent=True)[0]
    
    cmds.setAttr(f"{transform}.rotateX", -20)
    cmds.setAttr(f"{transform}.rotateY", -60)
    cmds.setAttr(f"{transform}.rotateZ", 0)
    
    print("[✓] Luz de relleno creada.")
    return transform


def _crear_luz_trasera():
    """Crea la luz trasera (rim/back light)"""
    luz = cmds.directionalLight(name="Rim_Light", intensity=0.8)
    transform = cmds.listRelatives(luz, parent=True)[0]
    
    cmds.setAttr(f"{transform}.rotateX", 40)
    cmds.setAttr(f"{transform}.rotateY", 180)
    cmds.setAttr(f"{transform}.rotateZ", 0)
    
    print("[✓] Luz trasera creada.")
    return transform