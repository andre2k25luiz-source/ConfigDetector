from ultralytics import YOLO
import shutil
import os


def treinar_modelo(data_path):
    model = YOLO("yolov8n.pt")

    results = model.train(
        data=data_path,
        epochs=10,
        imgsz=640
    )

    # 3. Mover o melhor modelo (melhor usar caminho relativo do results)
    best_path = "runs/detect/train/weights/best.pt"

    os.makedirs("models", exist_ok=True)
    shutil.copy(best_path, "models/best.pt")





    