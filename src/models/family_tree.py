from __future__ import annotations
from .person import Person, Gender
from ..relationships.factory import RelationFactory
from ..core import exceptions

class FamilyTree:
    def __init__(self) -> None:
        self.members = {}
        self.registry = RelationFactory.get_all_strategies()

    def add_person(self, name: str, gender_str: str) -> Person:
        # validate gender input before creating person object
        gender = Gender.from_str(gender_str)
        if not gender: return exceptions.InvalidGender.message()
        # create and register person in the main dictionary
        person = Person(name, gender)
        self.members[name] = person
        return person

    def marry(self, name1: str, name2: str) -> str:
        # fetch both person objects from registry
        p1, p2 = self.members.get(name1), self.members.get(name2)
        # ensure both people exist in the tree
        if not p1 or not p2: return exceptions.PersonNotFound.message()
        # logic check to prevent marrying oneself
        if p1 == p2: return exceptions.SelfMarriage.message()
        # check if either person is already married
        if p1.spouse or p2.spouse: return exceptions.CannotPolyamory.message()
        # validation for gender compatibility in marriage
        if p1.gender == p2.gender: return exceptions.NotSameGenderMarriage.message()

        # marry if all checks passed
        p1.set_spouse(p2)
        p2.set_spouse(p1)
        return "MARRIAGE_SUCCESSFUL"

    def add_child(self, mother_name: str, child_name: str, gender_str: str) -> str:
        # mother must exist in the system to add a child
        mother = self.members.get(mother_name)
        if not mother: return exceptions.PersonNotFound.message()
        # only female members can have children in this model
        if mother.gender != Gender.FEMALE: return exceptions.ChildAdditionFailed.message()
        # prevent duplicate names in the family tree
        if child_name in self.members: return exceptions.PersonAlreadyExists.message()
        # validate gender for the new child
        gender = Gender.from_str(gender_str)
        if not gender: return exceptions.InvalidGender.message()
        # create child and link to the mother
        child = Person(child_name, gender)
        mother.add_child(child)
        # save the new child to the global members list
        self.members[child_name] = child
        return "CHILD_ADDED"

    def get_relationship(self, name: str, relationship_type: str) -> str:
        # verify if the target person exists
        person = self.members.get(name)
        if not person:
            return exceptions.PersonNotFound.message()
        # retrieve specific search strategy from factory
        strategies = RelationFactory.get_all_strategies()
        strategy = strategies.get(relationship_type)
        # return error if the relationship type is not recognized
        if not strategy:
            return exceptions.UndefinedRelationship.message()
        # perform the search based on strategy logic
        results = strategy.find(person)
        # return none if no relatives were found
        if not results:
            return exceptions.GotNoOne.message()
        # join all found names into a single space-separated string
        return " ".join([p.name for p in results])