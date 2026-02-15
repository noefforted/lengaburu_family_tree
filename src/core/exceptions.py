class InvalidCommand:
    pass

class PersonNotFound(InvalidCommand):
    @classmethod
    def message(cls): return "PERSON_NOT_FOUND_IN_FAMILY_TREE"

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