from __future__ import annotations
from .base import RelationshipStrategy
from ..models.enums import Gender
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ..models.person import Person

class SiblingStrategy(RelationshipStrategy):
    def find(self, person: Person) -> List[Person]:
        if not person.mother: return []
        return [c for c in person.mother.children if c != person]

class SonStrategy(RelationshipStrategy):
    def find(self, person: Person) -> List[Person]:
        return [c for c in person.children if c.gender == Gender.MALE]

class DaughterStrategy(RelationshipStrategy):
    def find(self, person: Person) -> List[Person]:
        return [c for c in person.children if c.gender == Gender.FEMALE]

class PaternalUncleStrategy(RelationshipStrategy):
    def find(self, person: Person) -> List[Person]:
        if not person.father or not person.father.mother: return []
        return [c for c in person.father.mother.children if c != person.father and c.gender == Gender.MALE]

class MaternalUncleStrategy(RelationshipStrategy):
    def find(self, person: Person) -> List[Person]:
        if not person.mother or not person.mother.mother: return []
        return [c for c in person.mother.mother.children if c != person.mother and c.gender == Gender.MALE]

class PaternalAuntStrategy(RelationshipStrategy):
    def find(self, person: Person) -> List[Person]:
        if not person.father or not person.father.mother: return []
        return [c for c in person.father.mother.children if c != person.father and c.gender == Gender.FEMALE]

class MaternalAuntStrategy(RelationshipStrategy):
    def find(self, person: Person) -> List[Person]:
        if not person.mother or not person.mother.mother: return []
        return [c for c in person.mother.mother.children if c != person.mother and c.gender == Gender.FEMALE]

class SisterInLawStrategy(RelationshipStrategy):
    def find(self, person: Person) -> List[Person]:
        res = []
        if person.mother:
            for s in person.mother.children:
                if s != person and s.gender == Gender.MALE and s.spouse:
                    res.append(s.spouse)
        if person.spouse and person.spouse.mother:
            for s in person.spouse.mother.children:
                if s != person.spouse and s.gender == Gender.FEMALE:
                    res.append(s)
        return res

class BrotherInLawStrategy(RelationshipStrategy):
    def find(self, person: Person) -> List[Person]:
        res = []
        if person.mother:
            for s in person.mother.children:
                if s != person and s.gender == Gender.FEMALE and s.spouse:
                    res.append(s.spouse)
        if person.spouse and person.spouse.mother:
            for s in person.spouse.mother.children:
                if s != person.spouse and s.gender == Gender.MALE:
                    res.append(s)
        return res

class FatherStrategy(RelationshipStrategy):
    def find(self, person: Person) -> List[Person]:
        return [person.father] if person.father else []
    
class GrandsonStrategy(RelationshipStrategy):
    def find(self, person: Person) -> List[Person]:
        grandsons = []
        # Gunakan list anak dari diri sendiri DAN pasangan untuk memastikan kakek/nenek terjaring
        all_children = person.children
        if person.spouse and not all_children:
            all_children = person.spouse.children
            
        for child in all_children:
            # Sama halnya dengan cucu, cek di sisi pasangan si anak jika perlu
            all_grandchildren = child.children
            if child.spouse and not all_grandchildren:
                all_grandchildren = child.spouse.children
                
            for grandchild in all_grandchildren:
                if grandchild.gender == Gender.MALE:
                    grandsons.append(grandchild)
        return grandsons

class MotherStrategy(RelationshipStrategy):
    def find(self, person: Person) -> List[Person]:
        return [person.mother] if person.mother else []

class GrandfatherStrategy(RelationshipStrategy):
    def find(self, person: Person) -> List[Person]:
        res = []
        # Cek kakek dari sisi Ibu
        if person.mother and person.mother.father:
            res.append(person.mother.father)
        # Cek kakek dari sisi Ayah
        if person.father and person.father.father:
            res.append(person.father.father)
        return res

class GrandmotherStrategy(RelationshipStrategy):
    def find(self, person: Person) -> List[Person]:
        res = []
        # Cek nenek dari sisi Ibu
        if person.mother and person.mother.mother:
            res.append(person.mother.mother)
        # Cek nenek dari sisi Ayah
        if person.father and person.father.mother:
            res.append(person.father.mother)
        return res

class GranddaughterStrategy(RelationshipStrategy):
    def find(self, person: Person) -> List[Person]:
        res = []
        # Gunakan logika yang sama dengan Grandson tapi filter Female
        all_children = person.children
        if person.spouse and not all_children:
            all_children = person.spouse.children
            
        for child in all_children:
            grandchildren = child.children
            if child.spouse and not grandchildren:
                grandchildren = child.spouse.children
            for g_child in grandchildren:
                if g_child.gender == Gender.FEMALE:
                    res.append(g_child)
        return res

class GrandchildStrategy(RelationshipStrategy):
    def find(self, person: Person) -> List[Person]:
        # Gabungan dari Grandson dan Granddaughter
        res = []
        all_children = person.children
        if person.spouse and not all_children:
            all_children = person.spouse.children
            
        for child in all_children:
            grandchildren = child.children
            if child.spouse and not grandchildren:
                grandchildren = child.spouse.children
            res.extend(grandchildren)
        return res

class GrandparentStrategy(RelationshipStrategy):
    def find(self, person: Person) -> List[Person]:
        # Gabungan dari Grandfather dan Grandmother
        res = []
        if person.mother:
            if person.mother.mother: res.append(person.mother.mother)
            if person.mother.father: res.append(person.mother.father)
        if person.father:
            if person.father.mother: res.append(person.father.mother)
            if person.father.father: res.append(person.father.father)
        return res
    
class SpouseStrategy(RelationshipStrategy):
    def find(self, person: Person) -> List[Person]:
        # Mengembalikan list berisi pasangan jika ada, jika tidak ada kembalikan list kosong
        return [person.spouse] if person.spouse else []
    
class ChildrenStrategy(RelationshipStrategy):
    def find(self, person: Person) -> List[Person]:
        return person.children
