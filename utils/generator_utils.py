import cv2
import numpy as np
import os
import random

def remove_background(image):
    # 1. Converte para escala de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 2. Aplica um leve desfoque para reduzir ruído nas bordas
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # 3. Threshold de Otsu: ele calcula o melhor limiar sozinho 
    # (melhor que o fixo 240 que você estava usando)
    _, mask = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # 4. Operação Morfológica (Closing): Fecha pequenos buracos dentro do objeto
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    # 5. Opcional: Dilatar levemente para garantir que não cortamos as bordas do objeto
    mask = cv2.dilate(mask, kernel, iterations=1)
    
    return mask

def generate_dataset(input_path, backgrounds_dir, output_dir, num_images=200, train_ratio=0.8):
    # cria estrutura YOLO
    for split in ["train", "val"]:
        os.makedirs(f"{output_dir}/images/{split}", exist_ok=True)
        os.makedirs(f"{output_dir}/labels/{split}", exist_ok=True)

    obj = cv2.imread(input_path)
    mask = remove_background(obj)

    ys, xs = np.where(mask > 0)
    x_min, x_max = xs.min(), xs.max()
    y_min, y_max = ys.min(), ys.max()

    obj_crop = obj[y_min:y_max, x_min:x_max]
    mask_crop = mask[y_min:y_max, x_min:x_max]
    
    obj_aspect = obj_crop.shape[0] / obj_crop.shape[1]

    bg_files = [f for f in os.listdir(backgrounds_dir) if f.endswith((".jpg", ".png"))]

    for i in range(num_images):
        # decide se vai pra treino ou validação
        split = "train" if random.random() < train_ratio else "val"

        bg = cv2.imread(os.path.join(backgrounds_dir, random.choice(bg_files)))
        bg = cv2.resize(bg, (640, 640))
        h_bg, w_bg, _ = bg.shape

        scale = random.uniform(0.2, 0.5)
        new_w = int(w_bg * scale)
        new_h = int(new_w * obj_aspect)

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

        # salva imagem no split correto
        cv2.imwrite(f"{output_dir}/images/{split}/{img_name}", bg)

        # bbox YOLO
        x_center = (x_offset + new_w / 2) / w_bg
        y_center = (y_offset + new_h / 2) / h_bg
        w = new_w / w_bg
        h = new_h / h_bg

        # salva label no split correto
        with open(f"{output_dir}/labels/{split}/{img_name.replace('.jpg','.txt')}", "w") as f:
            f.write(f"0 {x_center} {y_center} {w} {h}")