import cv2
import numpy as np
import os
import random
from rembg import remove
from PIL import Image

def remove_background_ai(input_path):
    # O rembg lida com fundos complexos usando IA
    input_img = Image.open(input_path)
    output_img = remove(input_img)
    # Converte para formato OpenCV (RGBA)
    return cv2.cvtColor(np.array(output_img), cv2.COLOR_RGBA2BGRA)

def generate_dataset(input_path, backgrounds_dir, output_dir, num_images=200, train_ratio=0.8):
    for split in ["train", "val"]:
        os.makedirs(f"{output_dir}/images/{split}", exist_ok=True)
        os.makedirs(f"{output_dir}/labels/{split}", exist_ok=True)

    # Remove o fundo uma única vez para o objeto base
    obj_rgba = remove_background_ai(input_path)
    
    # Extrai o canal alpha para saber onde está o objeto
    alpha = obj_rgba[:, :, 3]
    ys, xs = np.where(alpha > 0)
    x_min, x_max, y_min, y_max = xs.min(), xs.max(), ys.min(), ys.max()
    
    # Crop apenas no objeto para facilitar o redimensionamento
    obj_crop = obj_rgba[y_min:y_max, x_min:x_max]
    obj_aspect = obj_crop.shape[0] / obj_crop.shape[1]

    bg_files = [f for f in os.listdir(backgrounds_dir) if f.lower().endswith((".jpg", ".png", ".jpeg"))]

    for i in range(num_images):
        split = "train" if random.random() < train_ratio else "val"
        
        bg = cv2.imread(os.path.join(backgrounds_dir, random.choice(bg_files)))
        if bg is None: continue
        bg = cv2.resize(bg, (640, 640))
        h_bg, w_bg, _ = bg.shape

        # Escala e redimensionamento
        scale = random.uniform(0.15, 0.45)
        new_w = int(w_bg * scale)
        new_h = int(new_w * obj_aspect)
        
        obj_r = cv2.resize(obj_crop, (new_w, new_h), interpolation=cv2.INTER_AREA)

        # Posição aleatória
        x_offset = random.randint(0, w_bg - new_w)
        y_offset = random.randint(0, h_bg - new_h)

        # Blend usando o canal Alpha (transparência real)
        alpha_r = obj_r[:, :, 3] / 255.0
        alpha_inv = 1.0 - alpha_r

        for c in range(0, 3): # Aplica nos canais B, G, R
            bg[y_offset:y_offset+new_h, x_offset:x_offset+new_w, c] = (
                alpha_r * obj_r[:, :, c] + alpha_inv * bg[y_offset:y_offset+new_h, x_offset:x_offset+new_w, c]
            )

        img_name = f"synth_{i:04d}.jpg"
        cv2.imwrite(f"{output_dir}/images/{split}/{img_name}", bg)

        # Labels YOLO
        x_center = (x_offset + new_w / 2) / w_bg
        y_center = (y_offset + new_h / 2) / h_bg
        w_yolo = new_w / w_bg
        h_yolo = new_h / h_bg

        with open(f"{output_dir}/labels/{split}/{img_name.replace('.jpg','.txt')}", "w") as f:
            f.write(f"0 {x_center:.6f} {y_center:.6f} {w_yolo:.6f} {h_yolo:.6f}")

    print(f"Dataset gerado com sucesso em: {output_dir}")

# Exemplo de uso:
# generate_dataset("meu_objeto.jpg", "./planos_de_fundo", "./meu_dataset_yolo")
