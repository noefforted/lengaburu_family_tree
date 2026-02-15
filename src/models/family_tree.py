from __future__ import annotations
from .person import Person, Gender
from ..relationships.factory import RelationFactory
from ..core import exceptions

class FamilyTree:
    def __init__(self) -> None:
        self.members = {}
        self.registry = RelationFactory.get_all_strategies()

    def add_person(self, name: str, gender_str: str) -> Person:
        gender = Gender.from_str(gender_str)
        if not gender: return exceptions.InvalidGender.message()

        person = Person(name, gender)
        self.members[name] = person
        return person

    def marry(self, name1: str, name2: str) -> str:
        p1, p2 = self.members.get(name1), self.members.get(name2)
        
        # 1. Pastikan kedua orang terdaftar
        if not p1 or not p2: return exceptions.PersonNotFound.message()
        
        # 2. Cegah menikahi diri sendiri (Unexpected Occurrence)
        if p1 == p2: return exceptions.SelfMarriage.message()
        
        # 3. Cegah poligami (Sesuai mayoritas requirement silsilah)
        if p1.spouse or p2.spouse: return exceptions.CannotPolimory.message()
        
        # 4. Cegah pernikahan sesama jenis (Jika requirement-nya konservatif/biologis)
        if p1.gender == p2.gender: return exceptions.NotSameGenderMarriage.message()

        # Jika lolos semua, baru nikahkan
        p1.set_spouse(p2)
        p2.set_spouse(p1)
        return "MARRIAGE_SUCCESSFUL"

    def add_child(self, mother_name: str, child_name: str, gender_str: str) -> str:
        mother = self.members.get(mother_name)
        if not mother: return exceptions.PersonNotFound.message()
        if mother.gender != Gender.FEMALE: return exceptions.ChildAdditionFailed.message()
        if child_name in self.members: return exceptions.PersonAlreadyExists.message()
        
        gender = Gender.from_str(gender_str)
        if not gender: return exceptions.InvalidGender.message()

        child = Person(child_name, gender)
        
        mother.add_child(child)
            
        self.members[child_name] = child
        return "CHILD_ADDED"

    def get_relationship(self, name: str, relationship_type: str) -> str:
        # 1. Cek apakah orang tersebut ada
        person = self.members.get(name)
        if not person:
            return exceptions.PersonNotFound.message() # "PERSON_NOT_FOUND"

        # 2. Ambil semua strategi dari Factory
        strategies = RelationFactory.get_all_strategies()
        strategy = strategies.get(relationship_type)

        # 3. Handle jika relationship_type tidak terdaftar (Unknownrelationship)
        if not strategy:
            return exceptions.UndefinedRelationship.message() # Atau pesan error lain sesuai asumsi "Good Judgment" Anda

        # 4. Jalankan pencarian
        results = strategy.find(person)
        
        if not results:
            return exceptions.GotNoOne.message() # "NONE"

        # 5. Format output: nama dipisahkan spasi
        return " ".join([p.name for p in results])