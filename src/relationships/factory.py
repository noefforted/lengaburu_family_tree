# src/relationships/factory.py
from . import strategies
from .base import RelationshipStrategy

class RelationFactory:
    _strategies = None

    @classmethod
    def get_all_strategies(cls):
        if cls._strategies is None:
            # Otomatis mendaftar semua class yang punya COMMAND_NAME
            cls._strategies = {
                sub.COMMAND_NAME: sub() 
                for sub in RelationshipStrategy.__subclasses__()
                if hasattr(sub, 'COMMAND_NAME')
            }
        return cls._strategies