from flask import Blueprint, g, render_template, request

inventory_bp = Blueprint("inventory", __name__, "/inventory")

@inventory_bp.route("/inventory", methods=('GET', 'POST'))
def inventory() -> str:
    print("FORM----------------")
    for (key, value) in request.form.items():
        print(f"{key=}, values={request.form.getlist(key)}")


    return render_template('inventory/inventory.jinja')
