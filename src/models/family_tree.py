from .person import Person, Gender
from ..relationships.strategies import (
    ChildrenStrategy, SiblingStrategy, SonStrategy, DaughterStrategy,
    PaternalUncleStrategy, MaternalUncleStrategy,
    PaternalAuntStrategy, MaternalAuntStrategy,
    SisterInLawStrategy, BrotherInLawStrategy, 
    FatherStrategy,MotherStrategy, GrandparentStrategy, GrandfatherStrategy, GrandmotherStrategy,
    GrandchildStrategy, GrandsonStrategy, GranddaughterStrategy, SpouseStrategy
)

class FamilyTree:
    def __init__(self):
        self.members = {}
        self.registry = {
            "Siblings": SiblingStrategy(),
            "Son": SonStrategy(),
            "Daughter": DaughterStrategy(),
            "Paternal-Uncle": PaternalUncleStrategy(),
            "Maternal-Uncle": MaternalUncleStrategy(),
            "Paternal-Aunt": PaternalAuntStrategy(),
            "Maternal-Aunt": MaternalAuntStrategy(),
            "Sister-In-Law": SisterInLawStrategy(),
            "Brother-In-Law": BrotherInLawStrategy(),
            "Father": FatherStrategy(),
            "Mother": MotherStrategy(),
            "Grandparent": GrandparentStrategy(),
            "Grandfather": GrandfatherStrategy(),
            "Grandmother": GrandmotherStrategy(),
            "Grandchild": GrandchildStrategy(),
            "Grandson": GrandsonStrategy(),
            "Granddaughter": GranddaughterStrategy(),
            "Spouse": SpouseStrategy(),
            "Children": ChildrenStrategy(),
        }

    def add_person(self, name, gender_str):
        gender = Gender.MALE if gender_str == "Male" else Gender.FEMALE
        person = Person(name, gender)
        self.members[name] = person
        return person

    def marry(self, name1, name2):
        p1, p2 = self.members.get(name1), self.members.get(name2)
        if p1 and p2:
            p1.set_spouse(p2)
            p2.set_spouse(p1)

    def add_child(self, mother_name, child_name, gender):
        mother = self.members.get(mother_name)
        if not mother: return "PERSON_NOT_FOUND"
        if mother.gender != Gender.FEMALE: return "CHILD_ADDITION_FAILED"
        
        child = Person(child_name, Gender.MALE if gender == "Male" else Gender.FEMALE)
        
        # Hubungkan ke Ibu
        child.mother = mother
        mother.children.append(child)
        
        # Hubungkan ke Ayah (Ini yang sering terlewat!)
        if mother.spouse:
            child.father = mother.spouse
            mother.spouse.children.append(child) # Sekarang Arthur punya anak di list-nya!
            
        self.members[child_name] = child
        return "CHILD_ADDED"

    def get_relationship(self, name, rel_type):
        person = self.members.get(name)
        if not person: return "PERSON_NOT_FOUND"
        strategy = self.registry.get(rel_type)
        if not strategy: return "NONE"
        
        results = strategy.find(person)
        if not results: return "NONE"
        return " ".join([p.name for p in results])
