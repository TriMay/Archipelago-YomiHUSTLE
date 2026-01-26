from abc import ABC, abstractmethod

from worlds.generic.Rules import CollectionRule
from BaseClasses import Region, Location, Entrance



class YomiHustleLocation(Location):
    game = "YOMI Hustle"





class AbstractLocationData(ABC):

    @abstractmethod
    def get_location_id(self) -> int:
        pass
    
    @abstractmethod
    def get_location_name(self) -> str:
        pass

    @abstractmethod
    def get_location_rule(self, player :int) -> CollectionRule:
        pass