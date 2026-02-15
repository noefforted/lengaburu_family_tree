from __future__ import annotations
from .enums import Gender

class Person:
    def __init__(self, name: str, gender: Gender) -> None:
        self.name = name
        self.gender = gender
        self.mother = None
        self.father = None
        self.spouse = None
        self.children = []

    def set_spouse(self, spouse: Person) -> None:
        self.spouse = spouse
        self._sync_children_with_spouse()

    def _sync_children_with_spouse(self) -> None:
        if not self.spouse:
            return
            
        for child in self.children:
            if self.gender == Gender.FEMALE:
                child.father = self.spouse
            else:
                child.mother = self.spouse

    def add_child(self, child: Person) -> None:
            if child not in self.children:
                self.children.append(child)
                if self.gender == Gender.FEMALE:
                    child.mother = self
                    child.father = self.spouse
                else:
                    child.father = self
                    child.mother = self.spouse

                if self.spouse and child not in self.spouse.children:
                    self.spouse.add_child(child)