from flask import render_template, Blueprint

main_route = Blueprint("main", __name__)

@main_route.route("/", methods=["GET", "POST"])
def index():
    return render_template('index.html')