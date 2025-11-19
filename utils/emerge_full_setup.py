from Utils.emerge import emerge_plane
from Materials.lights_setup import setup_lights
from PlaneRig.create_joints import crear_rig_completo
from PlaneRig.spline_auto_rig import build_spine_from_core_joints
from Environment.terrain import crear_terreno_montanoso
from Environment.cloud import crear_campo_nubes
from Materials.materials import aplicar_material_oro, aplicar_material_montanas, aplicar_material_nubes

import maya.cmds as cmds

def emerge_all_scene(clear_scene=True):
    if clear_scene:
        all_objects = cmds.ls(dag=True, long=True)
        default_cameras = {'front', 'persp', 'side', 'top'}
        to_delete = [obj for obj in all_objects 
                    if not (obj.startswith('|') and any(cam in obj for cam in default_cameras))]
        
        if to_delete:
            cmds.delete(to_delete)
    
    emerge_plane()
    setup_lights()
    crear_rig_completo()
    build_spine_from_core_joints()
    crear_terreno_montanoso()
    crear_campo_nubes(num_nubes=25)
    
    partes = ["FUSELAJE_GENERADO", "ALAS_GENERADO", "COLA_GENERADO", "CABEZA_GENERADO", "ORNAMENTACION_GENERADO"]
    for parte in partes:
        aplicar_material_oro(parte)
    
    aplicar_material_montanas("terreno")
    aplicar_material_nubes("campo_nubes")
    

if __name__ == '__main__':
    emerge_all_scene()
