from __future__ import annotations
from typing import Dict
from .base import RelationshipStrategy
from .strategies import (
    ChildrenStrategy, SiblingStrategy, SonStrategy, DaughterStrategy,
    PaternalUncleStrategy, MaternalUncleStrategy,
    PaternalAuntStrategy, MaternalAuntStrategy,
    SisterInLawStrategy, BrotherInLawStrategy, 
    FatherStrategy,MotherStrategy, GrandparentStrategy, GrandfatherStrategy, GrandmotherStrategy,
    GrandchildStrategy, GrandsonStrategy, GranddaughterStrategy, SpouseStrategy
)

class RelationFactory:
    @staticmethod
    def get_all_strategies() -> Dict[str, RelationshipStrategy]:
        return {
            "Siblings": SiblingStrategy(),
            "Son": SonStrategy(),
            "Daughter": DaughterStrategy(),
            "Paternal-Uncle": PaternalUncleStrategy(),
            "Maternal-Uncle": MaternalUncleStrategy(),
            "Paternal-Aunt": PaternalAuntStrategy(),
            "Maternal-Aunt": MaternalAuntStrategy(),
            "Sister-In-Law": SisterInLawStrategy(),
            "Brother-In-Law": BrotherInLawStrategy(),
            "Father": FatherStrategy(),
            "Mother": MotherStrategy(),
            "Grandparent": GrandparentStrategy(),
            "Grandfather": GrandfatherStrategy(),
            "Grandmother": GrandmotherStrategy(),
            "Grandchild": GrandchildStrategy(),
            "Grandson": GrandsonStrategy(),
            "Granddaughter": GranddaughterStrategy(),
            "Spouse": SpouseStrategy(),
            "Children": ChildrenStrategy(),
        }