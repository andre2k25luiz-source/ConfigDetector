import base64
import os
from flask import request, jsonify, Blueprint
from utils.criar_diretorios_utils import make_dir

save_yolo_route = Blueprint("save_yolo", __name__)

IMAGES_DIR, LABELS_DIR = make_dir()

@save_yolo_route.route("/save_yolo", methods=["POST"])
def save_yolo():
    try:
        data = request.json
        image_b64 = data.get('image_b64')
        filename = data.get('filename')
        labels = data.get('labels') # Lista de strings: ["0 0.5 0.5 0.2 0.2", ...]

        if not image_b64 or not filename:
            return jsonify({"msg": "Dados faltando"}), 400
        
        # --- LÓGICA PARA PEGAR TODOS OS IDs ÚNICOS ---
        # Ex: de "0 0.512 0.432...", ele pega o "0"
        try:
            # Pega o primeiro elemento de cada linha, transforma em set para remover duplicatas
            ids_unicos = sorted(list(set(line.split()[0] for line in labels)))
            # Cria um prefixo como: IDs_0_1_2_
            # prefixo_ids = "IDs_" + "_".join(ids_unicos)
            filename = f"{filename}"
        except Exception as e:
            print(f"Erro ao processar IDs: {e}")

        # 1. Salver a Imagem
        img_path = os.path.join(IMAGES_DIR, f"{filename}.jpg")
        with open(img_path, "wb") as f:
            f.write(base64.b64decode(image_b64))
        
        # 2. SAlvar as Labels (.txt)
        label_path = os.path.join(LABELS_DIR, f"{filename}.txt")
        with open(label_path, "w") as f:
            #Junta a lista de strings com quebras de linha
            f.write("\n".join(labels))
        
        return jsonify({"msg": f"Sucesso! Salvo em {filename}"}), 200


    except Exception as e:
        return jsonify({"msg": f"Erro no servidor: {str(e)}"}), 500




