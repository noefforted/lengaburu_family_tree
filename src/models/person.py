from .enums import Gender

class Person:
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
        self.mother = None
        self.father = None
        self.spouse = None
        self.children = []

    def set_spouse(self, spouse):
        self.spouse = spouse

    def add_child(self, child):
        self.children.append(child)
        if self.gender == Gender.FEMALE:
            child.mother = self
            child.father = self.spouse
        else:
            child.father = self
            child.mother = self.spouse
