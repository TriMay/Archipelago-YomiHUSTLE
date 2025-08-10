import typing
from BaseClasses import Item, ItemClassification
from .Moveset import hustle_moveset



class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classification: ItemClassification
    has_hit: typing.Optional[int]



class YomiHustleItem(Item):
    game = "YOMI Hustle"







hustle_items = {}

for move in hustle_moveset:
    hustle_items[move] = hustle_moveset[move].code + 100000