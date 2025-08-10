import typing
from BaseClasses import ItemClassification



class MoveData(typing.NamedTuple):
    code: typing.Optional[int]
    has_hit: typing.Optional[bool]







hustle_moveset = {
    "Cowboy - 3 Combo":           MoveData(2001, True),
    "Cowboy - Lightning Slice":   MoveData(2002, True),
    "Cowboy - Lasso":             MoveData(2003, True),
    "Cowboy - Pull":              MoveData(2004, True),
    "Cowboy - Izuna Drop":        MoveData(2005, True),
    "Cowboy - Impale":            MoveData(2006, True),
    "Cowboy - Gun Throw":         MoveData(2007, True),
    "Cowboy - Gun Pull":          MoveData(2008, True),
    "Cowboy - Foresight":         MoveData(2009, False),
    "Cowboy - Quick Draw":        MoveData(2010, False),
    "Cowboy - Shoot":             MoveData(2011, True),
    "Cowboy - Shoot Dodge":       MoveData(2012, True),
    "Cowboy - Point Blank":       MoveData(2013, True),
    "Cowboy - Holster":           MoveData(2014, False),
    "Cowboy - Backslash":         MoveData(2015, True),
    "Cowboy - 3 Combo Down":      MoveData(2016, True),
}