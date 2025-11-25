import maya.cmds as cmds
from Utils.config import CONFIG

def crear_control_para_joint(joint, lado):
    """
    Crea un control simple (circle) para el joint dado.
    - Crea un grupo offset
    - Alinea grupo con el joint
    - Mete el control dentro del grupo
    - Conecta con parentConstraint
    """

    nombre_ctrl = f"CTRL_wing_{lado}_001"
    nombre_grp = f"GRP_{nombre_ctrl}"

    # Borrar si ya existen
    for obj in (nombre_ctrl, nombre_grp):
        if cmds.objExists(obj):
            cmds.delete(obj)

    # Crear círculo
    ctrl = cmds.circle(n=nombre_ctrl, normal=[1,0,0], radius=3)[0]

    # Crear grupo offset
    grp = cmds.group(ctrl, n=nombre_grp)

    # Mover el grupo al joint
    cmds.delete(cmds.pointConstraint(joint, grp))
    cmds.delete(cmds.orientConstraint(joint, grp))

    # Constrain del control al joint
    cmds.parentConstraint(ctrl, joint, mo=False)

    print(f"[✓] Control '{nombre_ctrl}' creado para el joint '{joint}'")

    return {"ctrl": ctrl, "grp": grp}


def crear_wing_joints():
    """
    Crea los joints de las alas (wing_joint_L_001, wing_joint_R_001)
    usando los locators definidos en CONFIG["ALAS"]["locator_names"].
    Detecta automáticamente los prefijos agregados al importar.
    """
    alas_conf = CONFIG.get("ALAS", {})
    locator_patterns = alas_conf.get("locator_names", []) or []

    joints_creados = {}
    if not locator_patterns:
        print("[i] No se definieron locators en CONFIG['ALAS']['locator_names']")
        return joints_creados

    print(f"[i] Buscando locators definidos en config: {locator_patterns}")

    # Buscar todos los locators que coincidan con los patrones
    todos_candidatos = []
    for pat in locator_patterns:
        matches = cmds.ls(f"*{pat}", type="transform") or []
        todos_candidatos.extend(matches)

    if not todos_candidatos:
        print(f"[!] No se encontró ningún locator que coincida con {locator_patterns}")
        return joints_creados

    # Ordenar locators por X
    pos_x = {}
    for loc in todos_candidatos:
        try:
            p = cmds.xform(loc, q=True, t=True, ws=True)
            pos_x[loc] = p[0]
        except Exception:
            pos_x[loc] = 0.0

    if len(pos_x) >= 2:
        ordenados = sorted(pos_x.items(), key=lambda kv: kv[1])
        left_loc = ordenados[0][0]
        right_loc = ordenados[-1][0]
        mapping = {"L": left_loc, "R": right_loc}
        print(f"[i] Locators detectados por posición: L='{left_loc}', R='{right_loc}'")
    else:
        loc = list(pos_x.keys())[0]
        x = pos_x[loc]
        fus_x = 0.0
        if cmds.objExists("FUSELAJE_GENERADO"):
            try:
                bbox = cmds.exactWorldBoundingBox("FUSELAJE_GENERADO")
                fus_x = (bbox[0] + bbox[3]) / 2.0
            except Exception:
                pass
        lado = "L" if x < fus_x else "R"
        mapping = {lado: loc}
        print(f"[i] Un solo locator detectado ('{loc}'). Asignado a lado '{lado}'")

    # Crear joints y controles
    for lado, loc_name in mapping.items():
        try:
            pos = cmds.xform(loc_name, q=True, t=True, ws=True)
        except Exception as e:
            print(f"[!] Error obteniendo posición del locator {loc_name}: {e}")
            continue

        nombre_joint = f"wing_joint_{lado}_001"
        if cmds.objExists(nombre_joint):
            cmds.delete(nombre_joint)

        cmds.select(clear=True)
        joint = cmds.joint(name=nombre_joint, position=pos, absolute=True)

        # Parent al fuselaje
        if cmds.objExists("core_plane_joint_002"):
            try:
                cmds.parent(joint, "core_plane_joint_002")
            except Exception as e:
                print(f"[!] No se pudo parentar {joint} al fuselaje: {e}")

        print(f"[✓] Joint de ala {lado} creado en {pos} (desde locator '{loc_name}')")

        # Crear control para este joint
        ctrl_info = crear_control_para_joint(joint, lado)

        joints_creados[f"ALA_{lado}"] = {
            "joint": joint,
            "control": ctrl_info["ctrl"],
            "grupo": ctrl_info["grp"],
        }

    return joints_creados

if __name__ == '__main__':
    crear_wing_joints()