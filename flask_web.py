from flask import Flask, request, jsonify, render_template, abort
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    name = request.args.get("name", "Fero")
    return render_template("about.html", name=name)

@app.get("/login")
def login():
    abort(401)

@app.route("/users/0")
def admin():
    return "ADMIN USER LOGGED IN"

@app.route("/users/<int:user_id>")
def get_user(user_id):
    return render_template("user.html", user_id=user_id)

@app.route("/users/42")
def hitchhiker():
    return "DON'T PANIC!"


@app.get("/search")
def search():
    q = request.args.get("q")
    return f"searching for {q}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
