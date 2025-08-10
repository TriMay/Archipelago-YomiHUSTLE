from BaseClasses import Region, Location, Entrance, Item, ItemClassification
from .Moveset import hustle_moveset



class YomiHustleLocation(Location):
    game = "YOMI Hustle"








hustle_locations = {}

for move in hustle_moveset:
    hustle_locations[move] = hustle_moveset[move].code + 200000