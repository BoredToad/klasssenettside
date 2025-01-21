from flask import Flask, render_template
from auth import auth_bp, get_username_from_id

app = Flask(__name__)
app.config.from_mapping(SECRET_KEY='dev')
app.register_blueprint(auth_bp)

# this adds functions and variables that can be used in the templates
@app.context_processor
def processor():
    return dict(
        get_username_from_id=get_username_from_id,
        int=int
    )

@app.route("/")
def index() -> str:
    return render_template("homepage.jinja")

@app.route("/rules")
def rules():
    return render_template("homepage.jinja")

# this is some change
