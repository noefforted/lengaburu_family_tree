import unittest
from src.models.family_tree import FamilyTree
from src.core.seeder import seed_data
from src.core import exceptions

class TestFamilyTreeComprehensive(unittest.TestCase):
    # collection of standard error strings for normalization
    ERROR_MESSAGES = [
        exceptions.PersonNotFound.message(),
        exceptions.ChildAdditionFailed.message(),
        exceptions.PersonAlreadyExists.message(),
        exceptions.GotNoOne.message(),
        exceptions.InvalidGender.message(),
        exceptions.UndefinedRelationship.message()
    ]

    def setUp(self) -> None:
        # initialize tree and populate with initial data before each test
        self.tree = FamilyTree()
        seed_data(self.tree)
        print(f"\n{'='*30} START TEST: {self._testMethodName} {'='*30}")

    def _normalize(self, value: str):
        # convert string to set for comparison if it is a list of names and skips normalization if the value is a specific error message
        if value in self.ERROR_MESSAGES:
            return value
        return set(value.split())

    def log_result(self, status, person, relation, expected, actual):
        # helper to print formatted test results in the console
        flag = "[PASSED]" if status else "[FAILED]"
        print(f"{flag} | {relation} of {person}")
        print(f"--->Expected:  {expected}")
        print(f"--->Actual:    {actual}")
        
    def assert_add_child(self, mother, child, gender, expected):
        # execute add child action and check the return value
        actual = self.tree.add_child(mother, child, gender)
        is_match = actual == expected
        self.log_result(is_match, mother, f"ADD_CHILD {child}", expected, actual)
        # verify if the output matches requirement
        self.assertEqual(actual, expected, f"Failed at {mother} adding {child}")
        # check if the person object actually exists in memory after success
        if expected == "CHILD_ADDED":
            # verify the new member is registered in the dictionary
            self.assertIn(child, self.tree.members, f"{child} was not actually saved in tree!")
            # verify the child object has the correct link to the mother
            self.assertEqual(self.tree.get_relationship(child, "Mother"), mother)

    def assert_relationship(self, person, relation, expected):
        # query the relationship and handle multi-name results via normalization
        actual = self.tree.get_relationship(person, relation)
        actual_norm = self._normalize(actual)
        expected_norm = self._normalize(expected)
        is_match = actual_norm == expected_norm
        self.log_result(is_match, person, relation, expected, actual)
        if not is_match:
            self.assertEqual(actual, expected, f"Failed at {person} for {relation}")

    # 1. test all members existence
    def test_every_family_member_existence(self):
        # verify that all names from the seeder are correctly registered
        all_members = [
            "King-Arthur", "Queen-Margret", "Bill", "Flora", "Charlie", "Percy", "Audrey", 
            "Ronald", "Helen", "Ginerva", "Harry", "Victoire", "Ted", "Dominique", 
            "Louis", "Molly", "Lucy", "Malfoy", "Rose", "Hugo", "Darcy", "James",
            "Alice", "Albus", "Lily", "Remus", "Draco", "Aster", "William", "Ron","Ginny"
        ] 
        for member in all_members:
            exists = member in self.tree.members
            status = "[OK]" if exists else "[MISSING]"
            print(f"{status} Member: {member}")
            self.assertTrue(exists, f"{member} should be in the tree")

    # 2. test all add_child cases
    def test_add_child_cases(self):
        # covering success, missing parents, biological constraints, and duplicates
        test_cases = [
            # success scenarios
            ("Flora", "Aufa", "Female", "CHILD_ADDED"),
            ("Ginerva", "Aula", "Male", "CHILD_ADDED"),
            # mother not found
            ("Rihana", "Aufa", "Male", exceptions.PersonNotFound.message()),
            # check biological constraint where only mother can have children
            ("King-Arthur", "Aufa", "Male", exceptions.ChildAdditionFailed.message()),
            ("Bill", "Aula", "Female", exceptions.ChildAdditionFailed.message()),
            # duplicate name check
            ("Queen-Margret", "Bill", "Male", exceptions.PersonAlreadyExists.message()), 
            # data integrity check for gender input
            ("Queen-Margret", "Aufal", "NotGender", exceptions.InvalidGender.message()),
        ]
        print("\n--- Running Add Child Scenarios ---")
        for mother, child, gender, expected in test_cases:
            with self.subTest(mother=mother, child=child, gender=gender):
                self.assert_add_child(mother, child, gender, expected)

    # 3. test all get_relationship cases
    def test_get_relationship_cases(self):
        # comprehensive data driven tests for all relationship strategies
        test_cases = [
            # basic relations
            ("Aster", "Father", "Malfoy"),
            ("Aster", "Mother", "Rose"),
            ("Bill", "Son", "Louis"),
            ("Flora", "Daughter", "Victoire Dominique"),
            ("Louis", "Siblings", "Victoire Dominique"),
            # uncle and aunt
            ("Remus", "Maternal-Aunt", "Dominique"),
            ("Louis", "Paternal-Uncle", "Charlie Percy Ronald"),
            ("Louis", "Paternal-Aunt", "Ginerva"),
            ("Rose", "Maternal-Uncle", exceptions.GotNoOne.message()),
            ("James", "Maternal-Uncle", "Bill Charlie Percy Ronald"),
            # in-laws
            ("Ted", "Brother-In-Law", "Louis"), 
            ("Lily", "Sister-In-Law", "Darcy Alice"), 
            ("Harry", "Brother-In-Law", "Bill Charlie Percy Ronald"),
            # multi generation
            ("Remus", "Grandmother", "Flora"),
            ("Remus", "Grandfather", "Bill"),
            ("Remus", "Grandparent", "Bill Flora"),
            ("King-Arthur", "Grandson", "Louis Hugo James Albus"),
            ("King-Arthur", "Granddaughter", "Victoire Dominique Molly Lucy Rose Lily"),
            ("King-Arthur", "Grandchild", "Louis Hugo James Albus Victoire Dominique Molly Lucy Rose Lily"),
            # spouses
            ("King-Arthur", "Spouse", "Queen-Margret"),
            ("Flora", "Spouse", "Bill"),
            ("Ted", "Spouse", "Victoire"),
            ("Charlie", "Spouse", exceptions.GotNoOne.message()),
            # children
            ("King-Arthur", "Children", "Bill Charlie Percy Ronald Ginerva"),
            ("Ronald", "Children", "Rose Hugo"),
            ("Ginerva", "Children", "James Albus Lily"),
            ("Rose", "Children", "Draco Aster"),
            ("Victoire", "Children", "Remus"),
            # great-grandparents
            ("Remus", "Great-Grandfather", "King-Arthur"),
            ("Remus", "Great-Grandmother", "Queen-Margret"),
            ("Remus", "Great-Grandparent", "King-Arthur Queen-Margret"),
            # great-grandchildren
            ("King-Arthur", "Great-Grandson", "Remus Draco William Ron"),
            ("King-Arthur", "Great-Granddaughter", "Aster Ginny"),
            ("King-Arthur", "Great-Grandchild", "Remus Draco William Ron Aster Ginny"),
            # invalid queries
            ("Aufa", "Siblings", exceptions.PersonNotFound.message()),
            ("King-Arthur", "Father", exceptions.GotNoOne.message()),
        ]
        for person, rel, expected in test_cases:
            with self.subTest(person=person, rel=rel):
                self.assert_relationship(person, rel, expected)

if __name__ == "__main__":
    unittest.main()