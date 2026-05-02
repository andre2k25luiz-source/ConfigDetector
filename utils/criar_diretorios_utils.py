import os

def make_dir():
    # Configuração de pastas
    UPLOAD_FOLDER = 'dataset'
    IMAGES_DIR = os.path.join(UPLOAD_FOLDER, 'images')
    LABELS_DIR = os.path.join(UPLOAD_FOLDER, 'labels')

    # Garante que as pastas existam
    os.makedirs(IMAGES_DIR, exist_ok=True)
    os.makedirs(LABELS_DIR, exist_ok=True)

    return IMAGES_DIR, LABELS_DIR