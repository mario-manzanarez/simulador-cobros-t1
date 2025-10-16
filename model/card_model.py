import datetime

from bson import ObjectId


class Card:
    #  _id, cliente_id, pan_masked (ej. ************1234), last4, bin, created_at,
    # updated_at
    def __init__(self, id_card, customer_id, pan_masked,
                 last_4, bin, expiration_date, created_at,
                 updated_at, is_active):
        self.id_card = id_card
        self.customer_id = customer_id
        self.pan_masked = pan_masked
        self.last_4 = last_4
        self.bin = bin
        self.expiration_date = expiration_date
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_active = is_active

    def to_dict(self):
        """Convertir a dict listo para guardar en MongoDB"""
        data = {
            "customer": self.customer_id,
            "pan_masked": self.pan_masked,
            "last_4": self.last_4,
            "bin": self.bin,
            "expiration_date": self.expiration_date,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_active": self.is_active
        }
        if self.id_card:
            data["_id"] = ObjectId(self.id_card)
        return data

    def __str__(self):
        return super().__str__()
