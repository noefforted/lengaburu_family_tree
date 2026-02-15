from __future__ import annotations
from .person import Person, Gender
from ..relationships.factory import RelationFactory
from ..core.exceptions import PersonNotFoundError, ChildAdditionFailedError

class FamilyTree:
    def __init__(self) -> None:
        self.members = {}
        self.registry = RelationFactory.get_all_strategies()

    def add_person(self, name: str, gender_str: str) -> Person:
        gender = Gender.MALE if gender_str == "Male" else Gender.FEMALE
        person = Person(name, gender)
        self.members[name] = person
        return person

    def marry(self, name1: str, name2: str) -> None:
        p1, p2 = self.members.get(name1), self.members.get(name2)
        if p1 and p2:
            p1.set_spouse(p2)
            p2.set_spouse(p1)

    def add_child(self, mother_name: str, child_name: str, gender: str) -> str:
            mother = self.members.get(mother_name)
            if not mother: return "PERSON_NOT_FOUND"
            if mother.gender != Gender.FEMALE: return "CHILD_ADDITION_FAILED"
            
            
            child = Person(child_name, Gender.MALE if gender == "Male" else Gender.FEMALE)
            
            mother.add_child(child)
                
            self.members[child_name] = child
            return "CHILD_ADDED"

    def get_relationship(self, name: str, rel_type: str) -> str:
        person = self.members.get(name)
        if not person: return "PERSON_NOT_FOUND"
        strategy = self.registry.get(rel_type)
        if not strategy: return "NONE"
        
        results = strategy.find(person)
        if not results: return "NONE"
        return " ".join([p.name for p in results])