import unittest
from src.models.family_tree import FamilyTree
from src.core.seeder import seed_data
from src.core import exceptions

class TestFamilyTreeComprehensive(unittest.TestCase):
    ERROR_MESSAGES = [
        exceptions.PersonNotFound.message(),
        exceptions.ChildAdditionFailed.message(),
        exceptions.PersonAlreadyExists.message(),
        exceptions.GotNoOne.message(),
        exceptions.InvalidGender.message(),
        exceptions.UndefinedRelationship.message()
    ]

    def setUp(self) -> None:
        self.tree = FamilyTree()
        seed_data(self.tree)
        print(f"\n{'='*30} START TEST: {self._testMethodName} {'='*30}")

    def _normalize(self, value: str):
        """
        Mengubah output menjadi set jika itu daftar nama, 
        tapi membiarkannya tetap string jika itu pesan error/NONE.
        """
        if value in self.ERROR_MESSAGES:
            return value
        return set(value.split())

    def log_result(self, status, person, relation, expected, actual):
        flag = "[PASSED]" if status else "[FAILED]"
        print(f"{flag} | {relation} of {person}")
        print(f"--->Expected:  {expected}")
        print(f"--->Actual:    {actual}")
        
    def assert_add_child(self, mother, child, gender, expected):
        actual = self.tree.add_child(mother, child, gender)
        
        is_match = actual == expected
        self.log_result(is_match, mother, f"ADD_CHILD {child}", expected, actual)
        
        # 1. Cek apakah output string sesuai
        self.assertEqual(actual, expected, f"Failed at {mother} adding {child}")
        
        # 2. THE "WAH" FACTOR: Pengecekan Efek Samping (Side Effect Validation)
        if expected == "CHILD_ADDED":
            # Pastikan anak benar-benar terdaftar di dictionary members
            self.assertIn(child, self.tree.members, f"{child} was not actually saved in tree!")
            # Pastikan objek anak memiliki ibu yang benar
            self.assertEqual(self.tree.get_relationship(child, "Mother"), mother)

    def assert_relationship(self, person, relation, expected):
        actual = self.tree.get_relationship(person, relation)
        
        # Logika perbandingan jadi sangat simpel dan readable
        actual_norm = self._normalize(actual)
        expected_norm = self._normalize(expected)
        
        is_match = actual_norm == expected_norm
        self.log_result(is_match, person, relation, expected, actual)
        
        if not is_match:
            self.assertEqual(actual, expected, f"Failed at {person} for {relation}")
    
    # 1. TEST ALL MEMBERS EXISTENCE
    def test_every_family_member_existence(self):
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

    # 2. TEST ALL ADD_CHILD CASES
    def test_add_child_cases(self):
        # Asumsi: Anda memiliki Exception PersonAlreadyExists. 
        # Jika belum diimport, sesuaikan dengan string yang Anda return.
        
        test_cases = [
            # --- SUCCESS CASES ---
            # Format: (Mother, Child, Gender, Expected Result)
            ("Flora", "Aufa", "Female", "CHILD_ADDED"),
            ("Ginerva", "Aula", "Male", "CHILD_ADDED"),
            
            # --- ERROR CASES (EDGE CASES) ---
            # Ibu tidak ditemukan
            ("Rihana", "Aufa", "Male", exceptions.PersonNotFound.message()),
            
            # Ayah mencoba menambah anak (Harus gagal sesuai aturan biologis)
            ("King-Arthur", "Aufa", "Male", exceptions.ChildAdditionFailed.message()),
            ("Bill", "Aula", "Female", exceptions.ChildAdditionFailed.message()),
            
            # Duplikasi Nama (Nama "Bill" sudah ada di seeder)
            # Sesuaikan string expected ini dengan logic di person_already_exists Anda
            ("Queen-Margret", "Bill", "Male", exceptions.PersonAlreadyExists.message()), 
            
            # Gender Invalid
            ("Queen-Margret", "Aufa", "NotGender", exceptions.InvalidGender.message()),
        ]

        print("\n--- Running Add Child Scenarios ---")
        for mother, child, gender, expected in test_cases:
            with self.subTest(mother=mother, child=child, gender=gender):
                self.assert_add_child(mother, child, gender, expected)

    # 3. TEST ALL GET_RELATIONSHIP CASES
    def test_get_relationship_cases(self):
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
            ("Rose", "Maternal-Uncle", exceptions.GotNoOne.message()),
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
            ("Charlie", "Spouse", exceptions.GotNoOne.message()), # Charlie tidak punya istri di seeder

            # Children (Son + Daughter)
            ("King-Arthur", "Children", "Bill Charlie Percy Ronald Ginerva"),
            ("Ronald", "Children", "Rose Hugo"),
            ("Ginerva", "Children", "James Albus Lily"),
            ("Rose", "Children", "Draco Aster"),
            ("Victoire", "Children", "Remus"),

            # Great-Grandparents
            ("Remus", "Great-Grandfather", "King-Arthur"),
            ("Remus", "Great-Grandmother", "Queen-Margret"),
            ("Remus", "Great-Grandparent", "King-Arthur Queen-Margret"),

            # Great-Grandchildren
            ("King-Arthur", "Great-Grandson", "Remus Draco William Ron"),
            ("King-Arthur", "Great-Granddaughter", "Aster Ginny"),
            ("King-Arthur", "Great-Grandchild", "Remus Draco William Ron Aster Ginny"),

            # Edge Cases: Person not found in family tree
            ("Aufa", "Siblings", exceptions.PersonNotFound.message()),

            # Edge Cases: Valid relation but no person
            ("King-Arthur", "Father", exceptions.GotNoOne.message()),
        ]

        for person, rel, expected in test_cases:
            with self.subTest(person=person, rel=rel):
                self.assert_relationship(person, rel, expected)


if __name__ == "__main__":
    unittest.main()