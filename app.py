import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from routes.main_rote import main_route
from routes.save_yolo_route import save_yolo_route
from routes.train_route import train_route
from routes.predict_route import predict_route

app = Flask(__name__)

app.register_blueprint(main_route)
app.register_blueprint(save_yolo_route)
app.register_blueprint(train_route)
app.register_blueprint(predict_route)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)




