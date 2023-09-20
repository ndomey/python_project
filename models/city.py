from app import db

class City(db.Model):
    __tablename__ = "cities"

    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(64))
    country_id = db.Column(db.Integer, db.ForeignKey("countries.id"))
    visited =  db.Column(db.Boolean, default=False)
    def __repr__(self):
        return f"<City {self.id}: {self.city_name} {self.visited}>"