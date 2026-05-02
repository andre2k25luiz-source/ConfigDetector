from flask import Blueprint, request, jsonify

from services.predict_service import predict


predict_route = Blueprint("predict_route", __name__)


@predict_route.route("/predict", methods=["POST"])
def predict():
    try:
        file = request.files["image"]
        path = "temp.jpg"
        file.save(path)

        preds = predict(path)
        return jsonify(preds)

    except Exception as e:
        return jsonify({"erro": str(e)})






