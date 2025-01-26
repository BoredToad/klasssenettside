from db import db
from models import User, Item

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

init_db()

# def query_db():
#     db.connect()
#     # user = User.get(User.username == "bob")
#     user = User.get_by_id(1)
#     print(user.id, user.username, user.password)
# # query_db()
