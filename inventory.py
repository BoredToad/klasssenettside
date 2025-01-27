from flask import Blueprint, g, redirect, render_template, request, session, url_for
from models import Item, User
from auth import login_required

# note on how to interrupt table in future, the colspan tag is nice
#<tr>
#<th colspan="2" style="background-color:red;">
#<h1>some interruption</h1>
#</th>
#</tr>

inventory_bp = Blueprint("inventory", __name__, "/inventory")

def get_and_filter_items(filters: dict[str, list[str]]) -> list[dict[str, str]]:
    items = Item.select()

    if "search" in filters:
        searched = filters["search"][0]
        if searched:
            items = items.where(
                Item.name.contains(searched) |
                Item.model.contains(searched) |
                Item.manufacturer.contains(searched) |
                Item.specs.contains(searched) |
                Item.notes.contains(searched)
            )

    if "availability" in filters:
        items = items.where(
            (Item.loaned_by.is_null() if "available" in filters["availability"] else False) | # pyright: ignore
            (Item.loaned_by.is_null(False) if "not_available" in filters["availability"] else False) # pyright: ignore
        )
    if "status" in filters:
        items = items.where(
            Item.status.in_(filters["status"]) # pyright: ignore
        )
    if "category" in filters:
        items = items.where(
            Item.category.in_(filters["category"]) # pyright: ignore
        )

    return [
        {
            "id": item, 
            "name": item.name,
            "availability": "available" if not item.loaned_by else "not available",
            "status": item.status,
            "manufacturer": item.manufacturer,
            "model": item.model,
            "category": item.category
        }
        for item in items
    ]

@inventory_bp.route("/inventory", methods=('GET', 'POST'))
def inventory() -> str:
    filters = {}
    if request.method == 'POST':
        filters = { k : request.form.getlist(k) for k in request.form.keys() }
    g.items = get_and_filter_items(filters)

    return render_template('inventory/inventory.jinja')

@inventory_bp.route("/inventory/item/<name>", methods=('GET', 'POST'))
def item(name: str):
    item = Item.get(Item.name == name)

    if request.method == 'GET':
        g.name = item.name;
        g.specs = item.specs;
        g.notes = item.notes;
        g.updated_by = item.updated_by;
        g.last_edited = item.last_edited;
        g.loaned_by = item.loaned_by;
        return render_template("/inventory/item.jinja")

    if "return" in request.form:
        item.loaned_by = None
    elif "loan out" in request.form:
        item.loaned_by = User.get_by_id(session["user_id"])
    item.save()

    return redirect(url_for('inventory.inventory'))

# @inventory_bp.route("/inventory/loan/<name>")
# @login_required
# def loan(name: str):
#     return ""
