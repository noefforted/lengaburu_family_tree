import unittest
from src.models.family_tree import FamilyTree
from src.core.seeder import seed_data

class TestFamilyTreeComprehensive(unittest.TestCase):
    def setUp(self):
        self.tree = FamilyTree()
        seed_data(self.tree)
        print(f"\n{'='*30} START TEST: {self._testMethodName} {'='*30}")

    def log_result(self, status, person, relation, expected, actual):
        icon = "✅ PASS" if status else "❌ FAIL"
        print(f"{icon} | [{person}] -> {relation}")
        print(f"      Expected: {expected}")
        print(f"      Actual:   {actual}")

    def assert_rel(self, person, relation, expected):
        actual = self.tree.get_relationship(person, relation)
        
        # Logika pembandingan: urutan nama tidak masalah, jadi kita gunakan set
        actual_set = set(actual.split()) if actual not in ["NONE", "PERSON_NOT_FOUND"] else actual
        expected_set = set(expected.split()) if expected not in ["NONE", "PERSON_NOT_FOUND"] else expected
        
        is_match = actual_set == expected_set
        self.log_result(is_match, person, relation, expected, actual)
        
        if not is_match:
            self.assertEqual(actual, expected, f"Failed at {person} for {relation}")

    # ---------------------------------------------------------
    # 1. TEST SEMUA STRATEGY (CORE LOGIC)
    # ---------------------------------------------------------
    def test_all_strategies_comprehensive(self):
        """Mengetes setiap strategi relasi dengan sampel data yang berbeda."""
        test_cases = [
            # Relasi Dasar
            ("Aster", "Father", "Malfoy"),
            ("Aster", "Mother", "Rose"),
            ("Bill", "Son", "Louis"),
            ("Flora", "Daughter", "Victoire Dominique"),
            ("Louis", "Siblings", "Victoire Dominique"),
            
            # Relasi Uncle & Aunt (Paternal/Maternal)
            ("Remus", "Maternal-Aunt", "Dominique"),
            ("Louis", "Paternal-Uncle", "Charlie Percy Ronald"),
            ("Louis", "Paternal-Aunt", "Ginerva"),
            ("Rose", "Maternal-Uncle", "NONE"),
            ("James", "Maternal-Uncle", "Bill Charlie Percy Ronald"),
            
            # Relasi In-Laws
            ("Ted", "Brother-In-Law", "Louis"), # Suami Victoire, saudaranya Louis
            ("Lily", "Sister-In-Law", "Darcy Alice"), # Istri dari James dan Albus
            ("Harry", "Brother-In-Law", "Bill Charlie Percy Ronald"),
            
            # Relasi Multi-Generasi (Kakek/Nenek/Cucu)
            ("Remus", "Grandmother", "Flora"),
            ("Remus", "Grandfather", "Bill"),
            ("Remus", "Grandparent", "Bill Flora"),
            ("Arthur", "Grandson", "Louis Hugo James Albus"),
            ("Arthur", "Granddaughter", "Victoire Dominique Molly Lucy Rose Lily"),
            ("Arthur", "Grandchild", "Louis Hugo James Albus Victoire Dominique Molly Lucy Rose Lily"),

            # Relasi Spouse
            ("Arthur", "Spouse", "Margret"),
            ("Flora", "Spouse", "Bill"),
            ("Ted", "Spouse", "Victoire"),
            ("Charlie", "Spouse", "NONE"), # Charlie tidak punya istri di seeder

            # Relasi Children (Gabungan gender)
            ("Arthur", "Children", "Bill Charlie Percy Ronald Ginerva"),
            ("Ronald", "Children", "Rose Hugo"),
            ("Ginerva", "Children", "James Albus Lily"),
            ("Rose", "Children", "Draco Aster"),
            ("Victoire", "Children", "Remus"),
        ]

        for person, rel, expected in test_cases:
            with self.subTest(person=person, rel=rel):
                self.assert_rel(person, rel, expected)

    # ---------------------------------------------------------
    # 2. TEST SEMUA ANGGOTA KELUARGA (TRAVERSAL CHECK)
    # ---------------------------------------------------------
    def test_every_family_member_existence(self):
        """Memastikan setiap anggota yang ada di seeder bisa ditemukan dan punya relasi minimal."""
        all_members = [
            "Arthur", "Margret", "Bill", "Flora", "Victoire", "Ted", "Remus", 
            "Percy", "Audrey", "Molly", "Lucy", "Ronald", "Helen", "Rose", 
            "Malfoy", "Draco", "Aster", "Ginerva", "Harry", "James", "Darcy", "William"
        ]
        
        print("\n--- Verifying All Members Registration ---")
        for member in all_members:
            exists = member in self.tree.members
            status = "✅" if exists else "❌"
            print(f"{status} Member: {member}")
            self.assertTrue(exists, f"{member} should be in the tree")

    # ---------------------------------------------------------
    # 3. TEST EDGE CASES & ERROR HANDLING
    # ---------------------------------------------------------
    def test_edge_cases_and_errors(self):
        """Mengetes skenario batas sesuai permintaan soal halaman 3 & 10."""
        print("\n--- Running Edge Case Scenarios ---")
        
        # Kasus: Orang tidak ditemukan
        self.assert_rel("Voldemort", "Siblings", "PERSON_NOT_FOUND")
        
        # Kasus: Relasi valid tapi hasil kosong (NONE)
        # Arthur adalah puncak, tidak punya ayah di data
        self.assert_rel("Arthur", "Fathers", "NONE")
        
        # Kasus: Tambah anak pada Laki-laki (Harus gagal)
        res_add = self.tree.add_child("Arthur", "NewKid", "Male")
        self.log_result(res_add == "CHILD_ADDITION_FAILED", "Arthur", "AddChild", "CHILD_ADDITION_FAILED", res_add)
        self.assertEqual(res_add, "CHILD_ADDITION_FAILED")

        # Kasus: Tambah anak pada Ibu yang tidak terdaftar
        res_add_nf = self.tree.add_child("UnknownMom", "Baby", "Female")
        self.log_result(res_add_nf == "PERSON_NOT_FOUND", "UnknownMom", "AddChild", "PERSON_NOT_FOUND", res_add_nf)
        self.assertEqual(res_add_nf, "PERSON_NOT_FOUND")

if __name__ == "__main__":
    unittest.main()