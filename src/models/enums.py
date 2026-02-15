from enum import Enum

class Gender(Enum):
    MALE = "Male"
    FEMALE = "Female"

    @classmethod
    def from_str(cls, label: str):
        return {"Male": cls.MALE, "Female": cls.FEMALE}.get(label)