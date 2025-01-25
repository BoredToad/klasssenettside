from flask import Blueprint, render_template

inventory_bp = Blueprint("inventory", __name__, "/inventory")

@inventory_bp.route("/inventory")
def inventory() -> str:
    return render_template('inventory/inventory.jinja')
