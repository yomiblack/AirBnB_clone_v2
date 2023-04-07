#!/usr/bin/python3
""" Place instance with a city_id, amenities and reviews """
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
from models.base_model import BaseModel, Base
from os import getenv
from models.review import Review
from sqlalchemy.orm import relationship

STORAGE = getenv("HBNB_TYPE_STORAGE")


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    if STORAGE == "db":
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship('Review',
                               backref='place',
                               cascade="all, delete")

        place_amenity = Table('place_amenity', Base.metadata,
                              Column('place_id', String(60),
                                     ForeignKey('places.id'),
                                     primary_key=True, nullable=False),
                              Column('amenity_id', String(60),
                                     ForeignKey('amenities.id'),
                                     primary_key=True, nullable=False))

        amenities = relationship('Amenity', secondary=place_amenity,
                                 viewonly=False, backref="places")

    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            from models import storage
            list_review = []
            all_rev = storage.all(Review)
            for value in all_rev.values():
                if value.place_id == self.id:
                    list_review.append(value)
            return list_review

        @property
        def amenities(self):
            from models import storage
            from models.amenity import Amenity
            list_amenity = []
            all_ameni = storage.all(Amenity)
            for value in all_ameni.values():
                if value.id == self.amenity_ids:
                    list_amenity.append(value)
            return list_amenity

        @amenities.setter
        def amenities(self, value):
            from models import storage
            from models.amenity import Amenity
            if type(value) == Amenity:
                self.amenity_ids.append(value.id)
