import settings
import typing
from .Options import YomiHustleOptions  # the options we defined earlier
from .Items import YomiHustleItem, hustle_items  # data used below to add items to the World
from .Locations import YomiHustleLocation, hustle_locations  # same as above
from worlds.AutoWorld import World
from BaseClasses import Region, Location, Entrance, Item, ItemClassification
from worlds.generic.Rules import add_rule, set_rule, forbid_item, add_item_rule


class YomiHustleSettings(settings.Group):
    pass



class YomiHustleWorld(World):
    """Insert description of the world/game here."""
    game = "YOMI Hustle"  # name of the game/world
    options_dataclass = YomiHustleOptions  # options the player can set
    options: YomiHustleOptions  # typing hints for option results
    settings: typing.ClassVar[YomiHustleSettings]  # will be automatically assigned from type hint
    topology_present = True  # show path to required location checks in spoiler

    # ID of first item and location, could be hard-coded but code may be easier
    # to read with this as a property.
    #base_id = 1234
    # instead of dynamic numbering, IDs could be part of data

    # The following two dicts are required for the generation to know which
    # items exist. They could be generated from json or something else. They can
    # include events, but don't have to since events will be placed manually.
    item_name_to_id = hustle_items
    location_name_to_id = hustle_locations

    # Items can be grouped using their names to allow easy checking if any item
    # from that group has been collected. Group names can also be used for !hint
    #item_name_groups = {
    #    "weapons": {"sword", "lance"},
    #}
    
    
    
    def generate_early(self) -> None:
        self.random_start_moves = [ "Cowboy - 3 Combo", "Cowboy - Lightning Slice", "Cowboy - Lasso" ]
        for move in self.random_start_moves:
            self.multiworld.push_precollected(self.create_item(move))
        #self.multiworld.push_precollected(self.create_item("Cowboy - 3 Combo Down"))
        #print(self.options.starting_inventory.value)
        #self.options.starting_inventory.value += ["Cowboy - 3 Combo", "Cowboy - Lightning Slice", "Cowboy - Lasso"]
        #self.final_boss_hp = self.options.final_boss_hp.value
    
    
    
    
    def create_regions(self) -> None:
        # Add regions to the multiworld. One of them must use the origin_region_name as its name ("Menu" by default).
        # Arguments to Region() are name, player, multiworld, and optionally hint_text
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)  # or use += [menu_region...]

        main_region = Region("Main Area", self.player, self.multiworld)
        # add main area's locations to main area (all but final boss)
        # main_region.add_locations(main_region_locations, MyGameLocation)
        for location_name in hustle_locations:
            location_id = self.location_name_to_id[location_name]
            location_entry = YomiHustleLocation(self.player, location_name, location_id, main_region)
            main_region.locations.append(location_entry)
        
        menu_region.connect(main_region)
        
        self.multiworld.regions.append(main_region)
        
        goal_region = Region("Goal", self.player, self.multiworld)
        # add event to Boss Room
        goal_region.locations.append(YomiHustleLocation(self.player, "Goal", None, goal_region))
        
        
        main_region.connect(goal_region)
        
        
        
    
    
    
    def create_item(self, item: str) -> YomiHustleItem:
        if item == "Nothing":
            return YomiHustleItem(item, ItemClassification.filler, 1, self.player)
        classification = ItemClassification.progression
        return YomiHustleItem(item, classification, self.item_name_to_id[item], self.player)
    
    
    
    
    def create_event(self, event: str) -> YomiHustleItem:
        return YomiHustleItem(event, ItemClassification.progression, None, self.player)
    
    
    
    
    def create_items(self) -> None:
        # Add items to the Multiworld.
        # If there are two of the same item, the item has to be twice in the pool.
        # Which items are added to the pool may depend on player options, e.g. custom win condition like triforce hunt.
        # Having an item in the start inventory won't remove it from the pool.
        # If an item can't have duplicates it has to be excluded manually.

        # List of items to exclude, as a copy since it will be destroyed below
        
        
        exclude = self.random_start_moves
        
        basic_item_pool = self.item_name_to_id.keys()
        
        junk = 0
        
        for item in basic_item_pool:
            if item in exclude:
                self.multiworld.itempool.append(self.create_item("Nothing"))
                exclude.remove(item)
                junk += 1
            else:
                self.multiworld.itempool.append(self.create_item(item))

        # itempool and number of locations should match up.
        # If this is not the case we want to fill the itempool with junk.
        #self.multiworld.itempool += [self.create_item("Nothing") for _ in range(junk)]
    
    
    
    
    def set_rules(self) -> None:
        for location_name in hustle_locations:
            #forbid_item(self.multiworld.get_location(location_name, self.player), location_name, self.player)
            set_rule(self.multiworld.get_location(location_name, self.player),
                lambda state, l=location_name: state.has(l, self.player))
        
        self.multiworld.get_location("Goal", self.player).place_locked_item(self.create_event("Victory"))
    
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
        
        