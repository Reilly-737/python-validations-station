from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()


class Station(db.Model, SerializerMixin):
    __tablename__ = "stations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    city = db.Column(db.String(80))
    
    @validates("name")
    def validate_name(self, key, value):
        if len(value) < 3:
            raise ValueError("Name must be at least 3 characters long.")
        return value

    def __repr__(self):
        return f"<Station {self.name}>"


class Platform(db.Model, SerializerMixin):
    __tablename__ = "platforms"

    id = db.Column(db.Integer, primary_key=True)
    platform_num = db.Column(db.Integer)
    station_id = db.Column(db.Integer, db.ForeignKey("stations.id"))
    
    @validates("platform_num")
    def validates_platform_num(self, key, value):
        if not (1 <= value <= 20):
            raise ValueError("Platform number must be in range 1-20 (inclusive).")
        return value
        

    def __repr__(self):
        return f"<Platform {self.name}>"


class Train(db.Model, SerializerMixin):
    __tablename__ = "trains"

    id = db.Column(db.Integer, primary_key=True)
    train_num = db.Column(db.String)
    service_type = db.Column(db.String)
    origin = db.Column(db.String)
    destination = db.Column(db.String)
    
    @validates("train_num", "origin", "destination")
    def validate_string_length(self, key, value):
        if not (3 <= len(value) <= 24):
            raise ValueError(f"{key.capitalize()} must be between 3 and 24 characters long.")
        return value
    @validates("service_type")
    def validate_service_type(self, key, value):
        if value not in ["express", "local"]:
            raise ValueError("Service type must be either 'express' or 'local'.")
        return value 

    def __repr__(self):
        return f"<Train {self.name}>"


class Assignment(db.Model, SerializerMixin):
    __tablename__ = "assignments"

    id = db.Column(db.Integer, primary_key=True)
    arrival_time = db.Column(db.DateTime)
    departure_time = db.Column(db.DateTime)
    train_id = db.Column(db.Integer, db.ForeignKey("trains.id"))
    platform_id = db.Column(db.Integer, db.ForeignKey("platforms.id"))
    
    @validates("arrival_time", "departure_time")
    def validate_time_order(self, key, value):
        if "arrival_time" in self.__dict__ and "departure_time" in self.__dict__:
            if key == "departure_time" and value <= self.arrival_time:
                 raise ValueError("Departure time must be after arrival time.")
   
            time_difference = (self.departure_time - self.arrival_time).seconds / 60
            if time_difference > 20:
                raise ValueError("Time at platform must not exceed 20 minutes.")
        return value

    def __repr__(self):
        return f"<Assignment Train No: {self.train.train_num} Platform: {self.platform.platform_num}>"
