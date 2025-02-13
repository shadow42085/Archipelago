"""Runnable module that exports data needed by the mod/client."""

if __name__ == "__main__":
    import json
    import math
    import sys
    import os

    # makes this module runnable from its world folder.
    sys.path.remove(os.path.dirname(__file__))
    new_home = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
    os.chdir(new_home)
    sys.path.append(new_home)

    from worlds.subnautica.Locations import Vector, location_table
    from worlds.subnautica.Items import item_table, group_items
    from NetUtils import encode

    payload = {location_id: location_data["position"] for location_id, location_data in location_table.items()}
    with open("locations.json", "w") as f:
        json.dump(payload, f)

    # copy-paste from Rules
    def is_radiated(x: float, y: float, z: float) -> bool:
        aurora_dist = math.sqrt((x - 1038.0) ** 2 + y ** 2 + (z - -163.1) ** 2)
        return aurora_dist < 950
    # end of copy-paste


    def radiated(pos: Vector):
        return is_radiated(pos["x"], pos["y"], pos["z"])


    def far_away(pos: Vector):
        return (pos["x"] ** 2 + pos["z"] ** 2) > (800 ** 2)


    payload = {
        # "LaserCutter" in Subnautica ID
        "761": [location_id for location_id, location_data
                in location_table.items() if location_data["need_laser_cutter"]],
        # PropulsionCannon in Subnautica ID
        "757": [location_id for location_id, location_data
                in location_table.items() if location_data.get("need_propulsion_cannon", False)],
        # Radiation Suit in Subnautica ID
        "519": [location_id for location_id, location_data
                in location_table.items() if radiated(location_data["position"])],
        # SeaGlide in Subnautica ID
        "751": [location_id for location_id, location_data
                in location_table.items() if far_away(location_data["position"])],
    }
    with open("logic.json", "w") as f:
        json.dump(payload, f)

    itemcount = sum(item_data["count"] for item_data in item_table.values())
    assert itemcount == len(location_table), f"{itemcount} != {len(location_table)}"
    payload = {item_id: item_data["tech_type"] for item_id, item_data in item_table.items()}
    import json

    with open("items.json", "w") as f:
        json.dump(payload, f)
    with open("group_items.json", "w") as f:
        f.write(encode(group_items))

    print(f"Subnautica exports dumped to {new_home}")
