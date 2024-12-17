from flask import Flask, jsonify, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random


app = Flask(__name__)


# ---------------------------------------------- CREATE DB -------------------------------------------------------------
class Base(DeclarativeBase):
    pass


# ---------------------------------------------- Connect to Database ---------------------------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# -------------------------------------------- Cafe TABLE Configuration ------------------------------------------------
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


# --------------------------------------------------- HOME PAGE --------------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")


# --------------------------------------------- HTTP GET - Read Record -------------------------------------------------
@app.route("/random", methods=['GET'])
def get_random_cafe():
    result = db.session.execute(db.select(Cafe)).scalars().all()
    random_cafe = random.choice(result)
    if random_cafe:
        return jsonify(cafe={
            "id": random_cafe.id,
            "name": random_cafe.name,
            "map_url": random_cafe.map_url,
            "img_url": random_cafe.img_url,
            "location": random_cafe.location,
            "has_sockets": random_cafe.has_sockets,
            "has_toilet": random_cafe.has_toilet,
            "has_wifi": random_cafe.has_wifi,
            "can_take_calls": random_cafe.can_take_calls,
            "seats": random_cafe.seats,
            "coffee_price": (random_cafe.coffee_price).encode("utf-8").decode("unicode_escape")
        })

    else:
        return "Error 404"


@app.route("/all", methods=["GET"])
def display_all():
    all_cafes = []
    result = db.session.execute(db.select(Cafe)).scalars().all()

    for data in result:
        all_cafes.append(
            {
                "id": data.id,
                "name": data.name,
                "map_url": data.map_url,
                "img_url": data.img_url,
                "location": data.location,
                "has_sockets": data.has_sockets,
                "has_toilet": data.has_toilet,
                "has_wifi": data.has_wifi,
                "can_take_calls": data.can_take_calls,
                "seats": data.seats,
                "coffee_price": data.coffee_price
            }
        )

    return jsonify(cafes=[cafe.to_dict() for cafe in result])


@app.route("/search/<loc>")
def search(loc):
    searching = db.session.execute(db.select(Cafe).where(Cafe.location == loc)).scalar()
    if searching:
        return jsonify(cafe=[searching.to_dict()])
    else:
        return jsonify(error={"Not Found": "Sorry we don't have a cafe at that location"})


# ---------------------------------------------HTTP POST - Create Record -----------------------------------------------
@app.route("/add", methods=["POST"])
def add():
    new_cafe = Cafe(
        name=request.form.get('name'),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("location"),
        has_sockets=bool(request.form.get("has_sockets")),
        has_toilet=bool(request.form.get("has_toilet")),
        has_wifi=bool(request.form.get("has_wifi")),
        can_take_calls=bool(request.form.get("can_take_calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price")



    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"Success": "The new data added "})


# -------------------------------------------- HTTP PUT/PATCH - Update Record ------------------------------------------
@app.route("/update_price/<int:id_>", methods=["PATCH"])
def update_coffee_price(id_):

    new_price = request.args.get("new_price")
    coffe_price_id = db.session.execute(db.select(Cafe).where(Cafe.id == id_)).scalars().all()
    if coffe_price_id:
        for price in coffe_price_id:
            price.coffee_price = new_price
            db.session.commit()
            return jsonify(response={"success": "coffee price updated successful."}), 200
    else:
        return jsonify(response={"Error": "There was a problem because this id not in database"}), 404


# ----------------------------------------------HTTP DELETE - Delete Record --------------------------------------------
@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete(cafe_id):
    our_api_key = "TopSecretAPIKey"
    api_key = request.args.get("api-key")

    if our_api_key == api_key:
        the_cafe = Cafe.query.filter_by(id=cafe_id).first()
        if the_cafe:
            db.session.delete(the_cafe)
            db.session.commit()
            return jsonify(response={"Success": "The Cafe deleted successful."}), 200
        else:
            return jsonify(response={"Error": "Sorry That id of cafe not in database"}), 404
    else:
        return jsonify(response={"API Error": "Sorry you dont have the currect api key"}), 403


# ------------------------------------------------ RUN FLASK APP -------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
