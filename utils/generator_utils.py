import cv2
import numpy as np
import os
import random

def remove_background(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    return mask

def generate_dataset(input_path, backgrounds_dir, output_dir, num_images=200):
    os.makedirs(f"{output_dir}/images", exist_ok=True)
    os.makedirs(f"{output_dir}/labels", exist_ok=True)

    obj = cv2.imread(input_path)
    mask = remove_background(obj)

    ys, xs = np.where(mask > 0)
    x_min, x_max = xs.min(), xs.max()
    y_min, y_max = ys.min(), ys.max()

    obj_crop = obj[y_min:y_max, x_min:x_max]
    mask_crop = mask[y_min:y_max, x_min:x_max]
    
    # Proporção original do objeto para não distorcer
    obj_aspect = obj_crop.shape[0] / obj_crop.shape[1]

    bg_files = os.listdir(backgrounds_dir)

    for i in range(num_images):
        bg = cv2.imread(os.path.join(backgrounds_dir, random.choice(bg_files)))
        
        # --- ALTERAÇÃO: Redimensiona o background para um tamanho padrão (ex: 640x640) ---
        bg = cv2.resize(bg, (640, 640))
        h_bg, w_bg, _ = bg.shape

        # --- ALTERAÇÃO: Scale agora é relativo ao tamanho do background ---
        scale = random.uniform(0.2, 0.5) # Objeto ocupará de 20% a 50% da largura do BG
        new_w = int(w_bg * scale)
        new_h = int(new_w * obj_aspect)

        # Garante que o objeto não exceda a altura do background
        if new_h > h_bg:
            new_h = int(h_bg * scale)
            new_w = int(new_h / obj_aspect)

        obj_r = cv2.resize(obj_crop, (new_w, new_h))
        mask_r = cv2.resize(mask_crop, (new_w, new_h))

        x_offset = random.randint(0, w_bg - new_w)
        y_offset = random.randint(0, h_bg - new_h)

        roi = bg[y_offset:y_offset+new_h, x_offset:x_offset+new_w]

        mask_3ch = cv2.merge([mask_r]*3) / 255.0
        roi = (roi * (1 - mask_3ch) + obj_r * mask_3ch).astype(np.uint8)

        bg[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = roi

        img_name = f"{i:04d}.jpg"
        cv2.imwrite(f"{output_dir}/images/{img_name}", bg)

        x_center = (x_offset + new_w / 2) / w_bg
        y_center = (y_offset + new_h / 2) / h_bg
        w = new_w / w_bg
        h = new_h / h_bg

        with open(f"{output_dir}/labels/{img_name.replace('.jpg','.txt')}", "w") as f:
            f.write(f"0 {x_center} {y_center} {w} {h}")
