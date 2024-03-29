import json
from typing import Dict, List

def _load_xp_mult(filepath: str = "data/locations.json") -> Dict[str, float]:
        """
        Loads the known xp multipliers into a dict for dynamic creation
        Locations as needed
        
        Arguments:
            filepath {[str]} -- The filpath of the .json file  

        Returns:
            Dict[str, Location] -- A dict of [lowercase location name, xp multiplier]
        """
        with open(filepath) as file:
            content = json.load(file)

        result = {}
        locations = content["locations"]

        for location in locations:
            name = location['name'].lower()
            xp_mult = location['xp_multiplier']
            result[name] = xp_mult

        return result

class Location:
    _location_xp_mults = _load_xp_mult()
    _known_locations = {}

    def __init__(self, name: str, xp_mult: float = 1.0):
        self.name = name
        self.xp_mult = xp_mult

    @staticmethod
    def add_new_location(name: str, xp_mult: float) -> 'Location':
        name = name.lower()
        location = Location(name, xp_mult)
        Location._known_locations[name] = location
        return location

    @staticmethod
    def get_from_name(name: str) -> 'Location':
        name = name.lower()

        if name not in Location._known_locations:
            xp_mult = Location._location_xp_mults[name]
            Location._known_locations[name] = Location(name, xp_mult)
        
        return Location._known_locations[name]

    @staticmethod
    def save(filepath: str = 'data/locations.json') -> None:
        serialized = {"locations":[]}

        for name in Location._known_locations:
            entry = {}
            location = Location._known_locations[name]
            entry['name'] = location.name
            entry['xp_multiplier'] = location.xp_mult
            serialized["locations"].append(entry)

        with open(filepath, 'w') as f:
            json.dump(serialized, f)