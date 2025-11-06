import maya.cmds as cmds
from utils.config import CONFIG

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

    # Ordenar los locators por su coordenada X para determinar lados
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
        # solo un locator, asignar según su X vs fuselaje
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
        print(f"[i] Un solo locator detectado ('{loc}'). Asignado a lado '{lado}' (x={x:.3f}, fuselaje_x={fus_x:.3f})")

    # Crear joints según mapping
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
        if cmds.objExists("core_plane_joint_002"):
            try:
                cmds.parent(joint, "core_plane_joint_002")
            except Exception as e:
                print(f"[!] No se pudo parentar {joint} al fuselaje: {e}")

        print(f"[✓] Joint de ala {lado} creado en {pos} (desde locator '{loc_name}')")
        joints_creados[f"ALA_{lado}"] = joint

    return joints_creados