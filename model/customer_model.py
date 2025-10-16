from datetime import datetime

from bson import ObjectId


class Customer:
    def __init__(self, _id, name, email, phone, created_at, updated_at, is_active):
        self._id = _id
        self.name = name
        self.email = email
        self.phone = phone
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_active = is_active

    @classmethod
    def from_dto_create(cls, dto):
        return cls(
            _id=None,
            name=dto.name,
            email=dto.email,
            phone=dto.phone,
            created_at=datetime.now(),
            updated_at=None,
            is_active=True)

    @classmethod
    def from_dto_update(cls, dto, _id):
        return cls(
            _id=_id,
            name=dto.name,
            email=dto.email,
            phone=dto.phone,
            created_at=None,
            updated_at=datetime.now(),
            is_active=True)

    @classmethod
    def from_mongo(cls, data: dict):
        """Crear modelo a partir de documento MongoDB"""
        return cls(
            _id=data['_id'],
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            is_active=data["is_active"])

    def to_dict(self):
        """Convertir a dict listo para guardar en MongoDB"""
        data = {
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_active": self.is_active
        }
        if self._id:
            data["_id"] = ObjectId(self._id)
        return data
