from PlaneRig import create_joints, spline_auto_rig, cntrl_curve

def crear_rig_completo():
    """Crea el rig completo en un solo paso"""
    create_joints.crear_rig_completo()
    spline_auto_rig.build_spine_from_core_joints()
    cntrl_curve.crear_control_avion()