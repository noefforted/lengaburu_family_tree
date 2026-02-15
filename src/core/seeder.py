from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models.family_tree import FamilyTree

def seed_data(tree: FamilyTree) -> None:
    # Gen 1
    tree.add_person("King-Arthur", "Male")
    tree.add_person("Queen-Margret", "Female")
    tree.marry("King-Arthur", "Queen-Margret")
    
    # Gen 2
    for c in [("Bill","Male"), ("Charlie","Male"), ("Percy","Male"), ("Ronald","Male"), ("Ginerva","Female")]:
        tree.add_child("Queen-Margret", c[0], c[1])
    
    tree.add_person("Flora", "Female"); tree.marry("Bill", "Flora")
    tree.add_person("Audrey", "Female"); tree.marry("Percy", "Audrey")
    tree.add_person("Helen", "Female"); tree.marry("Ronald", "Helen")
    tree.add_person("Harry", "Male"); tree.marry("Ginerva", "Harry")
    
    # Gen 3
    for c in [("Victoire","Female"), ("Dominique","Female"), ("Louis","Male")]: tree.add_child("Flora", c[0], c[1])
    for c in [("Molly","Female"), ("Lucy","Female")]: tree.add_child("Audrey", c[0], c[1])
    for c in [("Rose","Female"), ("Hugo","Male")]: tree.add_child("Helen", c[0], c[1])
    for c in [("James","Male"), ("Albus","Male"), ("Lily","Female")]: tree.add_child("Ginerva", c[0], c[1])
    
    tree.add_person("Ted", "Male"); tree.marry("Victoire", "Ted")
    tree.add_person("Malfoy", "Male"); tree.marry("Rose", "Malfoy")
    tree.add_person("Darcy", "Female"); tree.marry("James", "Darcy")
    tree.add_person("Alice", "Female"); tree.marry("Albus", "Alice")
    
    # Gen 4
    tree.add_child("Victoire", "Remus", "Male")
    tree.add_child("Rose", "Draco", "Male")
    tree.add_child("Rose", "Aster", "Female")
    tree.add_child("Darcy", "William", "Male")
    tree.add_child("Alice", "Ron", "Male")
    tree.add_child("Alice", "Ginny", "Female")
