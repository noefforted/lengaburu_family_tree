from abc import ABC, abstractmethod

class RelationshipStrategy(ABC):
    @abstractmethod
    def find(self, person):
        pass
