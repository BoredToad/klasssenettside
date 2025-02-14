from itertools import count
from flask import Flask, render_template
from auth import auth_bp, get_username_from_id
from students import students, read_and_sort_csv, even_or_odd
from inventory import inventory_bp

app = Flask(__name__)
app.config.from_mapping(SECRET_KEY='dev')
app.register_blueprint(auth_bp)
app.register_blueprint(inventory_bp)

# this adds functions and variables that can be used in the templates
@app.context_processor
def processor():
    return dict(
        read_and_sort_csv=read_and_sort_csv,
        even_or_odd=even_or_odd,
        get_username_from_id=get_username_from_id,
        int=int,
        zip=zip,
        count=count,
    )

@app.route("/")
def index() -> str:
    return render_template("homepage.jinja")

@app.route("/rules")
def rules():
    return render_template("rulespage.jinja")

app.route("/students")(students)
