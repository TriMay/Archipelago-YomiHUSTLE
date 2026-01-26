from __future__ import annotations
import json
import os
from random import Random
from typing import Final
from enum import Enum

from .Item import YomiHustleItem, AbstractItemData
from .Location import YomiHustleLocation, AbstractLocationData
from worlds.generic.Rules import CollectionRule
from BaseClasses import CollectionState, ItemClassification



# class MoveData(typing.NamedTuple):
#    code: typing.Optional[int]
#    has_hit: typing.Optional[bool]


class LocationType(Enum):
	NONE = 0
	HIT = 1
	PERFORM = 2
	BLOCK = 3



class YomiHustleMoveLocationRule:
    def __init__(self, move :MoveData, player :int) -> None:
        self.move :MoveData = move
        self.player :int = player
    
    def __call__(self, state :CollectionState) -> bool:
        return self.has_move_unlocked(state) and self.can_select_move(state)


    def has_move_unlocked(self, state :CollectionState) -> bool:
        move :MoveData = self.move
        # TODO check path to location is clear
        return (move.free_item or state.has(move.get_item_name(), self.player)) and state.has(move.character.get_item_name(), self.player)


    def can_select_move(self, state :CollectionState) -> bool:
        return True # TODO





class YomiHustleShopLocationRule:
    def __init__(self, shop_slot :int, player :int) -> None:
        self.shop_slot: int  = shop_slot
        self.player :int = player
    
    def __call__(self, state :CollectionState) -> bool:
        return state.has(self.get_shop_key_name(), self.player)
    
    def get_shop_key_name(self) -> str:
        return "Shop Key " + str(((self.shop_slot - 1) % 5)+ 1)
        # TODO replace "Shop Key #" with "Color Shop Key"





class YomiHustleTestLocationRule:
    def __init__(self, shop_slot :int, player :int) -> None:
        self.shop_slot: int  = shop_slot
        self.player :int = player
    
    def __call__(self, state :CollectionState) -> bool:
        return state.has_group_unique("Moves", self.player, self.shop_slot * 10)
        # TODO this is psuedo logic, this will be replaced when I figure it out





class YomiHustleCharHittableMovesLocationRule: # dear god I'm sorry for this one
    def __init__(self, player :int, char :CharData, num_moves :int) -> None:
        self.player :int = player
        self.char :CharData = char
        self.num_moves: int  = num_moves
    
    def __call__(self, state :CollectionState) -> bool:
        return (
            state.has(self.char.get_item_name(), self.player) and
            state.has_group_unique(self.char.char_name + " Hittable Move", self.player, self.num_moves)
        )





class MoveData(AbstractLocationData, AbstractItemData):

    def __init__(self, char :CharData, json_data) -> None:
        self.character :CharData = char
        self.move_id :int = json_data["id"]
        self.move_name :str = json_data["name"]
        self.starter :bool = json_data["starter"]
        self.type :str = json_data["type"]
        self.location_type :LocationType = LocationType(json_data["location"])
        self.free_item :bool = json_data["free_item"]
        self.states :list[int] = json_data["states"]
    
    
    def get_item_id(self) -> int:
        return self.character.get_item_id() + self.move_id * 2 + CharData.MOVE_ID_START
    
    
    def get_item_name(self) -> str:
        return self.character.char_name + "'s " + self.move_name


    def get_location_id(self) -> int:
        return self.character.get_item_id() + self.move_id * 2 + CharData.MOVE_ID_START


    def get_location_name(self) -> str:
        return self.character.char_name + " - " + self.move_name


    def get_location_rule(self, player :int) -> CollectionRule:
        return YomiHustleMoveLocationRule(self, player)





class ShopLocationData(AbstractLocationData):

    def __init__(self, shop_slot :int) -> None:
        self.shop_slot :int = shop_slot
        self.id :int = shop_slot
        self.name :str = "Shop " + str(shop_slot)
    

    def get_location_id(self) -> int:
        return self.id
    
    
    def get_location_name(self) -> str:
        return self.name


    def get_location_rule(self, player :int) -> CollectionRule:
        return YomiHustleShopLocationRule(self.shop_slot, player)





class CharLevelLocationData(AbstractLocationData):

    def __init__(self, char :CharData, level :int) -> None:
        self.character :CharData = char
        self.level :int = level
    

    def get_location_id(self) -> int:       
        return self.character.get_item_id() + CharData.LEVEL_ID_START + self.level
    
    
    def get_location_name(self) -> str:
        return self.character.char_name + " Level " + str(self.level)
    

    def get_location_rule(self, player :int) -> CollectionRule:
        return YomiHustleCharHittableMovesLocationRule(player, self.character, self.level * 3)





class CharWinLocationData(AbstractLocationData):

    def __init__(self, char :CharData, milestone :int) -> None:
        self.character :CharData = char
        self.milestone :int = milestone
    

    def get_location_id(self) -> int:       
        return self.character.get_item_id() + CharData.WIN_ID_START + self.milestone
    
    
    def get_location_name(self) -> str:
        return self.character.char_name + " Win Milestone " + str(self.milestone)
    

    def get_location_rule(self, player :int) -> CollectionRule:
        return YomiHustleCharHittableMovesLocationRule(player, self.character, self.milestone * 4 + 8)





class CharComboLocationData(AbstractLocationData):

    def __init__(self, char :CharData, milestone :int) -> None:
        self.character :CharData = char
        self.milestone :int = milestone
    

    def get_location_id(self) -> int:       
        return self.character.get_item_id() + CharData.COMBO_ID_START + self.milestone
    
    
    def get_location_name(self) -> str:
        return self.character.char_name + " Combo Milestone " + str(self.milestone)
    

    def get_location_rule(self, player :int) -> CollectionRule:
        return YomiHustleCharHittableMovesLocationRule(player, self.character, self.milestone * 5)





class ShopKeyItemData(AbstractItemData):
    
    def __init__(self, key_num :int) -> None:
        self.key_num :int = key_num
    

    def get_item_id(self) -> int:
        return self.key_num
        

    def get_item_name(self) -> str:
        return "Shop Key " + str(self.key_num)




class CharData(AbstractItemData):

    CHAR_ID_OFFSET :Final[int] = 0x1000
    LEVEL_ID_START : Final[int] = 0x0001
    WIN_ID_START : Final[int] = 0x0010
    COMBO_ID_START : Final[int] = 0x0018
    MOVE_ID_START : Final[int] = 0x0040
    MAX_LEVEL_IDS : Final[int] = 7
    MAX_WIN_IDS : Final[int] = 3
    MAX_COMBO_IDS : Final[int] = 3


    def __init__(self, json_data) -> None:
        self.char_id :int = json_data["id"]
        self.char_name :str = json_data["name"]
        self.moves :dict[str, MoveData] = {}
        self.level_locations : list[CharLevelLocationData] = []
        self.win_locations : list[CharWinLocationData] = []
        self.combo_locations : list[CharComboLocationData] = []

        for name in json_data["items"]:  # pyright: ignore[reportUnknownVariableType]
            self.moves[name] = MoveData(self, json_data["items"][name])  # pyright: ignore[reportUnknownArgumentType]
        
        for i in range(self.MAX_LEVEL_IDS):
            new_data = CharLevelLocationData(self, i+1)
            self.level_locations.append(new_data)
        for i in range(self.MAX_WIN_IDS):
            new_data = CharWinLocationData(self, i+1)
            self.win_locations.append(new_data)
        for i in range(self.MAX_COMBO_IDS):
            new_data = CharComboLocationData(self, i+1)
            self.combo_locations.append(new_data)
    


    def get_item_name(self) -> str:
        return self.char_name + " (Fighter)"
    


    def get_item_id(self) -> int:
        return self.char_id * self.CHAR_ID_OFFSET
    


    def get_item_classification(self) -> ItemClassification:
        return ItemClassification.progression | ItemClassification.useful



    def get_all_location_data(self) -> list[AbstractLocationData]:
        result :list[AbstractLocationData] = []
        for move_name in self.moves:
            if self.moves[move_name].location_type == LocationType.NONE:
                continue
            result.append(self.moves[move_name])
        for location in self.level_locations:
            result.append(location)
        for location in self.win_locations:
            result.append(location)
        for location in self.combo_locations:
            result.append(location)
        return result
    


    def get_location_name_to_id(self) -> dict[str, int]:
        result :dict[str, int] = {}
        for location_data in self.get_all_location_data():
            result[location_data.get_location_name()] = location_data.get_location_id()
        return result
    


    def get_all_item_data(self) -> list[AbstractItemData]:
        result :list[AbstractItemData] = []
        result.append(self)
        for move_name in self.moves:
            if self.moves[move_name].free_item:
                continue
            result.append(self.moves[move_name])
        return result
    


    def get_item_name_to_id(self) -> dict[str, int]:
        result :dict[str, int] = {}
        for location_data in self.get_all_item_data():
            result[location_data.get_item_name()] = location_data.get_item_id()
        return result

    







class YomiHustleLogicData:

    NUM_SHOP_KEYS :Final[int] = 5
    MAX_SHOP_SIZE :Final[int] = 18

    char_data :dict[str, CharData] = {}
    id_to_location_data :dict[int, AbstractLocationData] = {}
    id_to_item_data :dict[int, AbstractItemData] = {}
    



    @staticmethod
    def init_class() -> None:
        for i in range(YomiHustleLogicData.NUM_SHOP_KEYS):
            new_item = ShopKeyItemData(i+1)
            YomiHustleLogicData.id_to_item_data[new_item.get_item_id()] = new_item
        for i in range(YomiHustleLogicData.MAX_SHOP_SIZE):
            new_location = ShopLocationData(i+1)
            YomiHustleLogicData.id_to_location_data[new_location.get_location_id()] = new_location



    @staticmethod
    def load_moveset_data(file_name :str):
        full_path = os.path.join(os.path.dirname(__file__), file_name)
        
        try:
            with open(full_path, "r") as file:
                json_data = json.loads(file.read())  # pyright: ignore[reportAny]
            if not isinstance(json_data, dict):
                return

            data :CharData = CharData(json_data)  # pyright: ignore[reportUnknownArgumentType]
            YomiHustleLogicData.char_data[data.char_name] = data
            for location_data in data.get_all_location_data():
                YomiHustleLogicData.id_to_location_data[location_data.get_location_id()] = location_data
            for item_data in data.get_all_item_data():
                YomiHustleLogicData.id_to_item_data[item_data.get_item_id()] = item_data

        except FileNotFoundError:
            return
        except json.JSONDecodeError:
            return
    


    @staticmethod
    def get_item_name_to_id() -> dict[str, int]:
        result :dict[str, int] = {}
        for item_id in YomiHustleLogicData.id_to_item_data:
            item_name = YomiHustleLogicData.id_to_item_data[item_id].get_item_name()
            result[item_name] = item_id
        return result



    @staticmethod
    def get_location_name_to_id() -> dict[str, int]:
        result :dict[str, int] = {}
        for location_id in YomiHustleLogicData.id_to_location_data:
            location_name = YomiHustleLogicData.id_to_location_data[location_id].get_location_name()
            result[location_name] = location_id
        return result
    


    @staticmethod
    def get_item_groups() -> dict[str, set[str]]:
        result: dict[str, set[str]] = {
            "Moves": set[str](),
            "Fighters": set[str]()
        }
        for char_name in YomiHustleLogicData.char_data:
            result["Fighters"].add(YomiHustleLogicData.char_data[char_name].get_item_name())
            result[char_name + " Move"] = set[str]()
            result[char_name + " Hittable Move"] = set[str]()
            char_moveset = YomiHustleLogicData.char_data[char_name].moves
            for move_name in char_moveset:
                if char_moveset[move_name].free_item:
                    continue
                item_name = char_moveset[move_name].get_item_name()
                result["Moves"].add(item_name)
                result[char_name + " Move"].add(item_name)
                if char_moveset[move_name].location_type == LocationType.HIT:
                    result[char_name + " Hittable Move"].add(item_name)
        return result
    


    @staticmethod
    def get_location_groups() -> dict[str, set[str]]:
        result: dict[str, set[str]] = {
            "Moves": set[str](),
            "Shop": set[str]()
        }
        for char_name in YomiHustleLogicData.char_data:
            char_moveset = YomiHustleLogicData.char_data[char_name].moves
            for move_name in char_moveset:
                if char_moveset[move_name].location_type == LocationType.NONE:
                    continue
                result["Moves"].add(char_moveset[move_name].get_location_name())
        for i in range(YomiHustleLogicData.MAX_SHOP_SIZE):
            result["Shop"].add("Shop " + str(i+1))
        return result



    @staticmethod
    def get_location_rule(location_id :int, player :int) -> CollectionRule:
        location_data = YomiHustleLogicData.id_to_location_data[location_id]
        return location_data.get_location_rule(player)
        


    @staticmethod
    def randomize_start_moves(random :Random) -> list[str]:
        fighter: str = random.choice(list(YomiHustleLogicData.char_data))
        move_pool :list[str] = YomiHustleLogicData.list_possible_start_moves(fighter)
        starter_items: list[str] = random.sample(move_pool, 5)
        starter_items.insert(0, YomiHustleLogicData.char_data[fighter].get_item_name())
        return starter_items
    


    @staticmethod
    def list_possible_start_moves(fighter :str) -> list[str]:
        result :list[str] = []
        move_pool: dict[str, MoveData] = YomiHustleLogicData.char_data[fighter].moves
        for move_name in move_pool:
            if move_pool[move_name].starter:
                result.append(move_pool[move_name].get_item_name())
        return result
    


    @staticmethod
    def get_item_classification(id :int) -> ItemClassification:
        return YomiHustleLogicData.id_to_item_data[id].get_item_classification()





YomiHustleLogicData.init_class()
YomiHustleLogicData.load_moveset_data("logic_data/NinjaLogic.json")
YomiHustleLogicData.load_moveset_data("logic_data/CowboyLogic.json")
YomiHustleLogicData.load_moveset_data("logic_data/WizardLogic.json")
YomiHustleLogicData.load_moveset_data("logic_data/RobotLogic.json")
YomiHustleLogicData.load_moveset_data("logic_data/MutantLogic.json")