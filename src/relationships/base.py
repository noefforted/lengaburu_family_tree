from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..models.person import Person

class RelationshipStrategy(ABC):
    @abstractmethod
    def find(self, person: Person) -> List[Person]:
        pass