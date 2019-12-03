from mongoengine import connect, DynamicDocument, StringField, DateTimeField, DictField, FloatField
import datetime
connect("helthify")


class Recipe(DynamicDocument):
    name = StringField(required=True, unique=True)
    ingredients = DictField(required=True)
    protein = FloatField()
    carbs = FloatField()
    fat = FloatField()
    F = FloatField()
    inserted_at = DateTimeField(default=datetime.datetime.now)


class Ingrendient(DynamicDocument):
    name = StringField(required=True, unique=True)
