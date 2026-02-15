class FamilyTreeError:
    pass

class PersonNotFound(FamilyTreeError):
    @classmethod
    def message(cls): return "PERSON_NOT_FOUND"

class ChildAdditionFailed(FamilyTreeError):
    @classmethod
    def message(cls): return "CHILD_ADDITION_FAILED"

class GotNoOne(FamilyTreeError):
    @classmethod
    def message(cls): return "NONE"

class InvalidGender(FamilyTreeError):
    @classmethod
    def message(cls): return "INVALID GENDER"