from app import db
# remove comments 
class Country(db.Model):
    __tablename__ = "countries"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    # language = db.Column(db.String(64))
    cities = db.relationship("City", backref="country")

    def __repr__(self):
        return f"<Country {self.id}: {self.name}>"