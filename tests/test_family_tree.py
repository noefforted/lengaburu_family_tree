import unittest
from src.models.family_tree import FamilyTree
from src.core.seeder import seed_data

class TestFamilyTreeComprehensive(unittest.TestCase):
    def setUp(self) -> None:
        self.tree = FamilyTree()
        seed_data(self.tree)
        print(f"\n{'='*30} START TEST: {self._testMethodName} {'='*30}")

    def log_result(self, status, person, relation, expected, actual):
        flag = "[PASS]" if status else "[FAIL]"
        print(f"{flag} | {relation} of {person}")
        print(f"--->Expected:  {expected}")
        print(f"--->Actual:    {actual}")

    def assert_rel(self, person, relation, expected):
        actual = self.tree.get_relationship(person, relation)
        
        # Comparison logic
        actual_set = set(actual.split()) if actual not in ["NONE", "PERSON_NOT_FOUND"] else actual
        expected_set = set(expected.split()) if expected not in ["NONE", "PERSON_NOT_FOUND"] else expected
        
        is_match = actual_set == expected_set
        self.log_result(is_match, person, relation, expected, actual)
        
        if not is_match:
            self.assertEqual(actual, expected, f"Failed at {person} for {relation}")

    # 1. TEST ALL STRATEGY (CORE LOGIC)
    def test_all_strategies_comprehensive(self):
        test_cases = [
            # Base Relation
            ("Aster", "Father", "Malfoy"),
            ("Aster", "Mother", "Rose"),
            ("Bill", "Son", "Louis"),
            ("Flora", "Daughter", "Victoire Dominique"),
            ("Louis", "Siblings", "Victoire Dominique"),
            
            # Uncle & Aunt (Paternal/Maternal)
            ("Remus", "Maternal-Aunt", "Dominique"),
            ("Louis", "Paternal-Uncle", "Charlie Percy Ronald"),
            ("Louis", "Paternal-Aunt", "Ginerva"),
            ("Rose", "Maternal-Uncle", "NONE"),
            ("James", "Maternal-Uncle", "Bill Charlie Percy Ronald"),
            
            # In-Laws
            ("Ted", "Brother-In-Law", "Louis"), # Suami Victoire, saudaranya Louis
            ("Lily", "Sister-In-Law", "Darcy Alice"), # Istri dari James dan Albus
            ("Harry", "Brother-In-Law", "Bill Charlie Percy Ronald"),
            
            # Multi Generation (Kakek/Nenek/Cucu)
            ("Remus", "Grandmother", "Flora"),
            ("Remus", "Grandfather", "Bill"),
            ("Remus", "Grandparent", "Bill Flora"),
            ("King-Arthur", "Grandson", "Louis Hugo James Albus"),
            ("King-Arthur", "Granddaughter", "Victoire Dominique Molly Lucy Rose Lily"),
            ("King-Arthur", "Grandchild", "Louis Hugo James Albus Victoire Dominique Molly Lucy Rose Lily"),

            # Spouse
            ("King-Arthur", "Spouse", "Queen-Margret"),
            ("Flora", "Spouse", "Bill"),
            ("Ted", "Spouse", "Victoire"),
            ("Charlie", "Spouse", "NONE"), # Charlie tidak punya istri di seeder

            # Children (Son + Daughter)
            ("King-Arthur", "Children", "Bill Charlie Percy Ronald Ginerva"),
            ("Ronald", "Children", "Rose Hugo"),
            ("Ginerva", "Children", "James Albus Lily"),
            ("Rose", "Children", "Draco Aster"),
            ("Victoire", "Children", "Remus"),
        ]

        for person, rel, expected in test_cases:
            with self.subTest(person=person, rel=rel):
                self.assert_rel(person, rel, expected)

    # 2. TEST EDGE CASES & ERROR HANDLING
    def test_edge_cases_and_errors(self):
        print("\n--- Running Edge Case Scenarios ---")
        
        # Person not found
        self.assert_rel("Aufa", "Siblings", "PERSON_NOT_FOUND")
        
        # Valid relation but no person
        self.assert_rel("King-Arthur", "Father", "NONE")
        
        # Add child to a person who is not a mother
        res_add = self.tree.add_child("King-Arthur", "Aufa", "Male")
        self.log_result(res_add == "CHILD_ADDITION_FAILED", "King-Arthur", "ADD_CHILD", "CHILD_ADDITION_FAILED", res_add)
        self.assertEqual(res_add, "CHILD_ADDITION_FAILED")

        # Add child to a non-existent mother
        res_add_nf = self.tree.add_child("Rihana", "Baby", "Female")
        self.log_result(res_add_nf == "PERSON_NOT_FOUND", "Rihana", "ADD_CHILD", "PERSON_NOT_FOUND", res_add_nf)
        self.assertEqual(res_add_nf, "PERSON_NOT_FOUND")

    # 3. TEST ALL MEMBERS EXISTENCE
    def test_every_family_member_existence(self):
        all_members = [
            "King-Arthur", "Queen-Margret", "Bill", "Flora", "Charlie", "Percy", "Audrey", 
            "Ronald", "Helen", "Ginerva", "Harry", "Victoire", "Ted", "Dominique", 
            "Louis", "Molly", "Lucy", "Malfoy", "Rose", "Hugo", "Darcy", "James",
            "Alice", "Albus", "Lily", "Remus", "Draco", "Aster", "William", "Ron","Ginny"
        ]
        
        print("\n--- Verifying All Members Registration ---")
        for member in all_members:
            exists = member in self.tree.members
            status = "[OK]" if exists else "[MISSING]"
            print(f"{status} Member: {member}")
            self.assertTrue(exists, f"{member} should be in the tree")


if __name__ == "__main__":
    unittest.main()