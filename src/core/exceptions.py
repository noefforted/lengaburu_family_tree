class InvalidCommand:
    pass

class PersonNotFound(InvalidCommand):
    @classmethod
    def message(cls): return "PERSON_NOT_FOUND_IN_FAMILY_TREE"

class SelfMarriage(InvalidCommand):
    @classmethod
    def message(cls): print("Error while seeding: Attempting to self marry is not allowed")

class CannotPolyamory(InvalidCommand):
    @classmethod
    def message(cls): print("Error while seeding: Attempting to polyamory is not allowed")

class NotSameGenderMarriage(InvalidCommand):
    @classmethod
    def message(cls): print("Error while seeding: Attempting to marry same gender is not allowed")

class ChildAdditionFailed(InvalidCommand):
    @classmethod
    def message(cls): return "CHILD_ADDITION_FAILED (only mothers can add children)"

class PersonAlreadyExists(InvalidCommand):
    @classmethod
    def message(cls): return "PERSON_ALREADY_EXISTS"

class GotNoOne(InvalidCommand):
    @classmethod
    def message(cls): return "NONE"

class InvalidGender(InvalidCommand):
    @classmethod
    def message(cls): return "INVALID_GENDER"

class UndefinedRelationship(InvalidCommand):
    @classmethod
    def message(cls): return "UNDEFINED_RELATIONSHIP_TYPE"