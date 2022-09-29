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
    # Outdated
    "Biomass (Alien Carapace)",
    "Biomass (Alien Organs)",
    "Beacon",
    "Alternate: Uranium Fuel Unit",
    # Creates infinite loops and doesn't really add anything to the calculations
    "Alternate: Diluted Packaged Fuel",
    "Packaged Fuel",
    "Packaged Liquid Biofuel",
    "Packaged Oil",
    "Packaged Heavy Oil Residue",
    "Packaged Sulfuric Acid",
    "Packaged Turbofuel",
    "Packaged Water",
    # Handled manually in alternate_recipes.json
    "Empty Canister",
    "Packaged Nitric Acid",
    # Not Needed
    "Power Shard (1)",
    "Power Shard (2)",
    "Power Shard (5)",
    # Weapons that are outdated
    "Alternate: Seismic Nobelisk",
    "Rifle Cartridge",
    "Nobelisk",
    "Spiked Rebar",
]

# As this app is about finding the differences between production chains, and these have no alternates, not very useful
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
    "FICSMAS Wonder Star",
]
