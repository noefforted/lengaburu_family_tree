from __future__ import annotations
from .base import RelationshipStrategy
from ..models.enums import Gender
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ..models.person import Person

class SiblingStrategy(RelationshipStrategy):
    COMMAND_NAME = "Siblings"
    def find(self, person: Person) -> List[Person]:
        if not person.mother: return []
        return [c for c in person.mother.children if c != person]

class BrotherStrategy(RelationshipStrategy):
    COMMAND_NAME = "Brother"
    def find(self, person: Person) -> List[Person]:
        # Ambil semua saudara, lalu filter yang Male
        if not person.mother: return []
        return [c for c in person.mother.children if c != person and c.gender == Gender.MALE]

class SisterStrategy(RelationshipStrategy):
    COMMAND_NAME = "Sister"
    def find(self, person: Person) -> List[Person]:
        # Ambil semua saudara, lalu filter yang Female
        if not person.mother: return []
        return [c for c in person.mother.children if c != person and c.gender == Gender.FEMALE]

class SisterInLawStrategy(RelationshipStrategy):
    COMMAND_NAME = "Sister-In-Law"
    def find(self, person: Person) -> List[Person]:
        res = set()
        # Jalur 1: Istri dari saudara laki-laki
        if person.mother:
            for sibling in person.mother.children:
                if sibling != person and sibling.gender == Gender.MALE and sibling.spouse:
                    res.add(sibling.spouse)
        
        # Jalur 2: Saudara perempuan dari pasangan
        if person.spouse and person.spouse.mother:
            for s_sibling in person.spouse.mother.children:
                if s_sibling != person.spouse and s_sibling.gender == Gender.FEMALE:
                    res.add(s_sibling)
        
        return list(res)
    
class BrotherInLawStrategy(RelationshipStrategy):
    COMMAND_NAME = "Brother-In-Law"
    def find(self, person: Person) -> List[Person]:
        res = set()
        # Jalur 1: Suami dari saudara perempuan
        if person.mother:
            for sibling in person.mother.children:
                if sibling != person and sibling.gender == Gender.FEMALE and sibling.spouse:
                    res.add(sibling.spouse)
        
        # Jalur 2: Saudara laki-laki dari pasangan
        if person.spouse and person.spouse.mother:
            for b_sibling in person.spouse.mother.children:
                if b_sibling != person.spouse and b_sibling.gender == Gender.MALE:
                    res.add(b_sibling)
        
        return list(res)
    
class SonStrategy(RelationshipStrategy):
    COMMAND_NAME = "Son"
    def find(self, person: Person) -> List[Person]:
        return [c for c in person.children if c.gender == Gender.MALE]

class DaughterStrategy(RelationshipStrategy):
    COMMAND_NAME = "Daughter"
    def find(self, person: Person) -> List[Person]:
        return [c for c in person.children if c.gender == Gender.FEMALE]

class PaternalUncleStrategy(RelationshipStrategy):
    COMMAND_NAME = "Paternal-Uncle"
    def find(self, person: Person) -> List[Person]:
        if not person.father or not person.father.mother: return []
        return [c for c in person.father.mother.children if c != person.father and c.gender == Gender.MALE]

class MaternalUncleStrategy(RelationshipStrategy):
    COMMAND_NAME = "Maternal-Uncle"
    def find(self, person: Person) -> List[Person]:
        if not person.mother or not person.mother.mother: return []
        return [c for c in person.mother.mother.children if c != person.mother and c.gender == Gender.MALE]

class PaternalAuntStrategy(RelationshipStrategy):
    COMMAND_NAME = "Paternal-Aunt"
    def find(self, person: Person) -> List[Person]:
        if not person.father or not person.father.mother: return []
        return [c for c in person.father.mother.children if c != person.father and c.gender == Gender.FEMALE]

class MaternalAuntStrategy(RelationshipStrategy):
    COMMAND_NAME = "Maternal-Aunt"
    def find(self, person: Person) -> List[Person]:
        if not person.mother or not person.mother.mother: return []
        return [c for c in person.mother.mother.children if c != person.mother and c.gender == Gender.FEMALE]

class FatherStrategy(RelationshipStrategy):
    COMMAND_NAME = "Father"
    def find(self, person: Person) -> List[Person]:
        return [person.father] if person.father else []
    
class MotherStrategy(RelationshipStrategy):
    COMMAND_NAME = "Mother"
    def find(self, person: Person) -> List[Person]:
        return [person.mother] if person.mother else []

class GrandfatherStrategy(RelationshipStrategy):
    COMMAND_NAME = "Grandfather"
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
    COMMAND_NAME = "Grandmother"
    def find(self, person: Person) -> List[Person]:
        res = []
        # Cek nenek dari sisi Ibu
        if person.mother and person.mother.mother:
            res.append(person.mother.mother)
        # Cek nenek dari sisi Ayah
        if person.father and person.father.mother:
            res.append(person.father.mother)
        return res
    
class GrandsonStrategy(RelationshipStrategy):
    COMMAND_NAME = "Grandson"
    def find(self, person: Person) -> List[Person]:
        grandsons = []

        all_children = list(set(person.children + (person.spouse.children if person.spouse else [])))
            
        for child in all_children:
            # Sama halnya dengan cucu, cek di sisi pasangan si anak jika perlu
            all_grandchildren = child.children
            if child.spouse and not all_grandchildren:
                all_grandchildren = child.spouse.children
                
            for grandchild in all_grandchildren:
                if grandchild.gender == Gender.MALE:
                    grandsons.append(grandchild)
        return grandsons

class GranddaughterStrategy(RelationshipStrategy):
    COMMAND_NAME = "Granddaughter"
    def find(self, person: Person) -> List[Person]:
        res = []
        
        all_children = list(set(person.children + (person.spouse.children if person.spouse else [])))
            
        for child in all_children:
            grandchildren = child.children
            if child.spouse and not grandchildren:
                grandchildren = child.spouse.children
            for g_child in grandchildren:
                if g_child.gender == Gender.FEMALE:
                    res.append(g_child)
        return res

class GrandchildStrategy(RelationshipStrategy):
    COMMAND_NAME = "Grandchild"
    def find(self, person: Person) -> List[Person]:
        res = []
        all_children = list(set(person.children + (person.spouse.children if person.spouse else [])))
            
        for child in all_children:
            grandchildren = child.children
            if child.spouse and not grandchildren:
                grandchildren = child.spouse.children
            res.extend(grandchildren)
        return res

class GrandparentStrategy(RelationshipStrategy):
    COMMAND_NAME = "Grandparent"
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
    COMMAND_NAME = "Spouse"
    def find(self, person: Person) -> List[Person]:
        # Mengembalikan list berisi pasangan jika ada, jika tidak ada kembalikan list kosong
        return [person.spouse] if person.spouse else []
    
class ChildrenStrategy(RelationshipStrategy):
    COMMAND_NAME = "Children"
    def find(self, person: Person) -> List[Person]:
        return person.children
    
# --- GREAT-GRANDCHILDREN STRATEGIES ---

class GreatGrandchildStrategy(RelationshipStrategy):
    COMMAND_NAME = "Great-Grandchild"
    def find(self, person: Person) -> List[Person]:
        res = []
        # Telusuri Anak -> Cucu -> Cicit
        for child in person.children:
            for grandchild in child.children:
                res.extend(grandchild.children)
        return res

class GreatGrandsonStrategy(RelationshipStrategy):
    COMMAND_NAME = "Great-Grandson"
    def find(self, person: Person) -> List[Person]:
        # Filter gender Male dari GreatGrandchild
        all_great_grandchildren = GreatGrandchildStrategy().find(person)
        return [c for c in all_great_grandchildren if c.gender == Gender.MALE]

class GreatGranddaughterStrategy(RelationshipStrategy):
    COMMAND_NAME = "Great-Granddaughter"
    def find(self, person: Person) -> List[Person]:
        # Filter gender Female dari GreatGrandchild
        all_great_grandchildren = GreatGrandchildStrategy().find(person)
        return [c for c in all_great_grandchildren if c.gender == Gender.FEMALE]


# --- GREAT-GRANDPARENT STRATEGIES ---

class GreatGrandparentStrategy(RelationshipStrategy):
    COMMAND_NAME = "Great-Grandparent"
    def find(self, person: Person) -> List[Person]:
        res = []
        # Ambil semua Kakek/Nenek terlebih dahulu
        from .strategies import GrandparentStrategy
        grandparents = GrandparentStrategy().find(person)
        
        for gp in grandparents:
            if gp.mother: res.append(gp.mother)
            if gp.father: res.append(gp.father)
        return list(set(res)) # Gunakan set untuk menghindari duplikasi

class GreatGrandfatherStrategy(RelationshipStrategy):
    COMMAND_NAME = "Great-Grandfather"
    def find(self, person: Person) -> List[Person]:
        all_ggp = GreatGrandparentStrategy().find(person)
        return [p for p in all_ggp if p.gender == Gender.MALE]

class GreatGrandmotherStrategy(RelationshipStrategy):
    COMMAND_NAME = "Great-Grandmother"
    def find(self, person: Person) -> List[Person]:
        all_ggp = GreatGrandparentStrategy().find(person)
        return [p for p in all_ggp if p.gender == Gender.FEMALE]
