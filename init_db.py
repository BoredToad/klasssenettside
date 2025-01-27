import peewee
from db import db
from models import User, Item
from csv import DictReader

category_translator = {
    "laptop": "laptop",
    "switch": "switch",
    "server": "server",
    "pc": "pc",
    "diverse": "misc",
    "gaming rigs": "gaming_rig",
    "firewall": "firewall",
    "tastatur": "misc",
    "skjerm": "monitor",
    "mus": "misc"
}

status_translator = {
    "fungerer ikke": "does_not_work",
    "fungerer med problemer": "mostly_works",
    "fungerer": "works"
}

def init_from_csv():
    with open("inventory.csv") as file:
        reader = DictReader(file)
        db.connect()
        db.create_tables([User, Item])

        for row in reader:
            try:
                Item.create(
                    name=row["navn"],
                    category=category_translator[row["kategori"].lower()],
                    manufacturer=row["produsent"],
                    model=row["modell"],
                    specs=row["specs"],
                    notes=row["notat"],
                    status=status_translator[row["tilstand"].lower()],
                )
            except peewee.IntegrityError:
                continue
        
    ...
init_from_csv()

# init_db()

# def query_db():
#     db.connect()
#     # user = User.get(User.username == "bob")
#     user = User.get_by_id(1)
#     print(user.id, user.username, user.password)
# # query_db()

def init_db():
    db.connect()
    db.create_tables([User, Item])

    Item.create(
        name="pc-69",
        category="pc",
        manufacturer="idfk",
        model="someModel",
        specs="",
        notes="",
        status="works",
        loaned_by=User.create(username="bob", password="pass")
    )
    Item.create(
        name="pc-99",
        category="pc",
        manufacturer="idfk",
        model="someModel",
        specs="",
        notes="",
        status="mostly_works",
    )

    # bob = User.create(username="bob", password="pass")
    # bill = User.create(username="bill", password="pass")
