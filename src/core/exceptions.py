class FamilyTreeError(Exception):
    """Base class untuk semua error di aplikasi ini."""
    pass

class PersonNotFoundError(FamilyTreeError):
    def __str__(self): return "PERSON_NOT_FOUND"

class ChildAdditionFailedError(FamilyTreeError):
    def __str__(self): return "CHILD_ADDITION_FAILED"