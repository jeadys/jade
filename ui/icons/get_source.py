import os


def get_source(icon):
    current_directory = os.path.dirname(os.path.abspath(__file__))

    icon_paths = {
        "arm": os.path.join(current_directory, "biped", "biped_arm_85.png"),
        "leg": os.path.join(current_directory, "biped", "biped_leg_85.png"),
        "spine": os.path.join(current_directory, "biped", "biped_spine_85.png"),
        "hand": os.path.join(current_directory, "biped", "biped_hand_85.png"),
        "foot": os.path.join(current_directory, "biped", "biped_foot_85.png"),
        "head": os.path.join(current_directory, "biped", "biped_head_85.png"),
        "breasts": os.path.join(current_directory, "biped", "biped_breasts_85.png"),
        "buttocks": os.path.join(current_directory, "biped", "biped_buttocks_85.png"),
        "beard": os.path.join(current_directory, "facial", "facial_beard_85.png"),
        "ear": os.path.join(current_directory, "facial", "facial_ear_85.png"),
        "eye": os.path.join(current_directory, "facial", "facial_eye_85.png"),
        "eyebrow": os.path.join(current_directory, "facial", "facial_eyebrow_85.png"),
        "face": os.path.join(current_directory, "facial", "facial_face_85.png"),
        "lips": os.path.join(current_directory, "facial", "facial_lips_85.png"),
        "mouth": os.path.join(current_directory, "facial", "facial_mouth_85.png"),
        "nose": os.path.join(current_directory, "facial", "facial_nose_85.png"),
        "tongue": os.path.join(current_directory, "facial", "facial_tongue_85.png"),
        "joint": os.path.join(current_directory, "joint.png"),
    }

    return icon_paths.get(icon, None)
