from rig import core_plane, wings_plane

def crear_rig_completo():
    """
    Ejecuta la creación de todo el rig del avión:
    Core (cabeza, fuselaje, cola) + Wings (alas)
    """
    print("\n=== Creando rig completo del avión ===")
    core = core_plane.crear_core_joints()
    wings = wings_plane.crear_wing_joints()

    total = len(core) + len(wings)
    print(f"\n✅ Rig completo creado ({total} joints en total)")
    return {**core, **wings}

if __name__ == "__main__":
    crear_rig_completo()