from collections.abc import ItemsView
from flask import Blueprint, g, render_template, request
from models import Item

# note on how to interrupt table in future, the colspan tag is nice
#<tr>
#<th colspan="2" style="background-color:red;">
#<h1>some interruption</h1>
#</th>
#</tr>

# Item.category.contains() | whoaifjdisi

availability_helper = lambda item: True if item == "available" else False

inventory_bp = Blueprint("inventory", __name__, "/inventory")

def get_and_filter_items(filters: dict[str, list[str]]) -> list[dict[str, str]]:
    items = Item.select()

    print(f"filters: \n{filters}")

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
            # I'm sad that we HAVE to convert it to a list for it to work
            Item.availability.in_(list(map( # pyright: ignore
                availability_helper,
                filters["availability"]
            )))
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
            "availability": "available" if item.availability else "not available",
            "status": item.status,
            "manufacturer": item.manufacturer,
            "model": item.model,
            "category": item.category
        }
        for item in items
    ]

@inventory_bp.route("/inventory", methods=('GET', 'POST'))
def inventory() -> str:
    filters = { k : request.form.getlist(k) for k in request.form.keys() }
    g.items = get_and_filter_items(filters)

    return render_template('inventory/inventory.jinja')
