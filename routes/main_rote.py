from flask import request, render_template, Flask, Blueprint

main_route = Blueprint("main", __name__)

@main_route.route("/", methods=["GET", "POST"])
def index():
    return render_template('index.html')