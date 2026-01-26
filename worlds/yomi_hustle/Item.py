from abc import ABC, abstractmethod

from BaseClasses import Item, ItemClassification



class YomiHustleItem(Item):
    game :str = "YOMI Hustle"




class AbstractItemData(ABC):

    @abstractmethod
    def get_item_id(self) -> int:
        pass
    
    @abstractmethod
    def get_item_name(self) -> str:
        pass
    
    def get_item_classification(self) -> ItemClassification:
        return ItemClassification.progression
