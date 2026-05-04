import os
import shutil
import random

def split_dataset(dataset_dir, train_ratio=0.8):
    images_dir = os.path.join(dataset_dir, "images")
    labels_dir = os.path.join(dataset_dir, "labels")

    images = [f for f in os.listdir(images_dir) if f.endswith(".jpg")]
    random.shuffle(images)

    split_idx = int(len(images) * train_ratio)
    train_files = images[:split_idx]
    val_files = images[split_idx:]

    # cria pastas
    for split in ["train", "val"]:
        os.makedirs(os.path.join(images_dir, split), exist_ok=True)
        os.makedirs(os.path.join(labels_dir, split), exist_ok=True)

    def move_files(files, split):
        for img in files:
            label = img.replace(".jpg", ".txt")

            shutil.move(
                os.path.join(images_dir, img),
                os.path.join(images_dir, split, img)
            )

            shutil.move(
                os.path.join(labels_dir, label),
                os.path.join(labels_dir, split, label)
            )

    move_files(train_files, "train")
    move_files(val_files, "val")

    print(f"Train: {len(train_files)} | Val: {len(val_files)}")


""""
Não use shutil.move se quiser manter backup → use copy
Sempre embaralhe (random.shuffle) antes de dividir
Para datasets pequenos (tipo 20 imagens), o modelo pode ficar ruim — tente pelo menos 100+ 
"""  


