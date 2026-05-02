from flask import Flask, request, jsonify, Blueprint
import os
import shutil
# Certifique-se de importar suas funções dos arquivos corretos
from utils.generator_utils import generate_dataset 
from services.train_service import treinar_modelo

train_route = Blueprint("train_route", __name__)

@train_route.route("/train", methods=["POST"])
def train():
    file = request.files["image"]

    input_path = "data/input/input.jpg"
    file.save(input_path)

    generate_dataset(
        input_path=input_path,
        backgrounds_dir="data/backgrounds",
        output_dir="data/output",
        num_images=20
    )

    # cria data.yaml
    with open("data/output/data.yaml", "w") as f:
        f.write("""
path: data/output
train: images
val: images
names:
  0: objeto
""")
        
    treinar_modelo(data_path="data/output/data.yaml")

    return jsonify({"status": "modelo treinado"})




