from __future__ import annotations
from .enums import Gender

class Person:
    def __init__(self, name: str, gender: Gender) -> None:
        self.name = name
        self.gender = gender
        self.mother = None
        self.father = None
        self.spouse = None
        self.children = []

    def set_spouse(self, spouse: Person) -> None:
        """
        Expert Logic: Sinkronisasi otomatis saat terjadi pernikahan.
        """
        self.spouse = spouse
        # Jika saya punya anak sebelum menikah, 
        # segera berikan Ayah/Ibu kepada mereka sekarang.
        self._sync_children_with_spouse()

    def _sync_children_with_spouse(self) -> None:
        """Internal helper untuk menjaga integritas data."""
        if not self.spouse:
            return
            
        for child in self.children:
            if self.gender == Gender.FEMALE:
                child.father = self.spouse
            else:
                child.mother = self.spouse

    def add_child(self, child: Person) -> None:
            """
            Menambahkan anak ke diri sendiri dan secara otomatis ke pasangan (jika ada).
            """
            if child not in self.children:
                self.children.append(child)
                
                # Hubungkan anak ke orang tua secara biologis/legal
                if self.gender == Gender.FEMALE:
                    child.mother = self
                    child.father = self.spouse # Bisa None jika belum menikah
                else:
                    child.father = self
                    child.mother = self.spouse # Bisa None jika belum menikah

                # EXPERT MOVE: Jika saya punya pasangan, tambahkan anak ini ke list pasangan juga
                # Gunakan pengecekan agar tidak terjadi pengulangan tanpa akhir (infinite loop)
                if self.spouse and child not in self.spouse.children:
                    self.spouse.add_child(child)