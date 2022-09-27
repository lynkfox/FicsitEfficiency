from ficsit2.com.names import ComponentName

# List of endpoints that signify no further recipes will be found
ENDPOINTS = [
    ComponentName.IRON_ORE,
    ComponentName.COPPER_ORE,
    ComponentName.BAUXITE_ORE,
    ComponentName.URANIUM_ORE,
    ComponentName.CATERIUM_ORE,
    ComponentName.COAL,
    ComponentName.SULFUR,
    ComponentName.NITROGEN,
    ComponentName.LIMESTONE,
    ComponentName.WATER,
    ComponentName.OIL,
]

# List of Components that count as a fluid - mostly for display purposes out of Component
FLUIDS = [
    ComponentName.WATER,
    ComponentName.OIL,
    ComponentName.HEAVY_OIL_RESIDUE,
    ComponentName.FUEL,
    ComponentName.TURBO_FUEL,
    ComponentName.NITROGEN,
    ComponentName.SULFURIC_ACID,
    ComponentName.NITRIC_ACID,
    ComponentName.ALUMINA_SOLUTION,
]


# List of ignored recipes in Build Recipe
IGNORED_RECIPES = [
    "Alternate: Coated Iron Canister",
    "Alternate: Diluted Packaged Fuel",
    "Alternate: Steel Canister",
    "Beacon",
    "Solid Biofuel",
    "Color Cartridge",
    "Gas Filter",
    "Iodine Infused Filter",
    "Empty Canister",
    "Packaged Fuel",
    "Liquid Biofuel",
    "Packaged Liquid Biofuel",
    "Packaged Oil",
    "Packaged Nitric Acid",
    "Packaged Heavy Oil Residue",
    "Packaged Sulfuric Acid",
    "Packaged Turbofuel",
    "Packaged Water",
    "Power Shard (1)",
    "Power Shard (2)",
    "Power Shard (5)",
    "Alternate: Seismic Nobelisk",
    "Rifle Cartridge",
    "Nobelisk",
    "Spiked Rebar"
]

WEAPON_RECIPES = [
    "Nobelisk",
    "Alternate: Seismic Nobelisk",
    "Spiked Rebar",
    "Rifle Cartridge"
]

FICSMAS_RECIPES = [
    "Candy Cane",
    "Sweet Fireworks",
    "Fancy Fireworks",
    "Sparkly Fireworks",
    "Actual Snow",
    "Snowball",
    "Red FICSMAS Ornament",
    "Blue FICSMAS Ornament",
    "Copper FICSMAS Ornament",
    "Iron FICSMAS Ornament",
    "FICSMAS Ornament Bundle",
    "FICSMAS Bow",
    "FICSMAS Tree Branch",
    "FICSMAS Decoration",
    "FICSMAS Wonder Star"
]