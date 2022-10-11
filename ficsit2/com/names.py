from enum import Enum


class Buildable(Enum):
    MINER = "Miner"
    SMELTER = "Smelter"
    FOUNDRY = "Foundry"
    CONSTRUCTOR = "Constructor"
    ASSEMBLER = "Assembler"
    MANUFACTURER = "Manufacturer"
    REFINERY = "Refinery"
    BLENDER = "Blender"
    PACKAGER = "Packager"
    PARTICLE_ACCELERATOR = "Particle Accelerator"
    NUCLEAR_POWER_PLANT = "Nuclear Power Plant"


class ComponentName(Enum):
    PORTABLE_MINER = "Portable Miner"
    LIMESTONE = "Limestone"
    IRON_ORE = "Iron Ore"
    COPPER_ORE = "Copper Ore"
    RAW_QUARTZ = "Raw Quartz"
    COAL = "Coal"
    SULFUR = "Sulfur"
    CATERIUM_ORE = "Caterium Ore"
    BAUXITE_ORE = "Bauxite Ore"
    URANIUM_ORE = "Uranium Ore"
    WATER = "Water"
    OIL = "Oil"
    NITROGEN = "Nitrogen Gas"
    BIOMASS = "Biomass"
    WOOD = "Wood"
    QUARTZ_CRYSTAL = "Quartz Crystal"
    IRON_INGOT = "Iron Ingot"
    COPPER_INGOT = "Copper Ingot"
    STEEL_INGOT = "Steel Ingot"
    CATERIUM_INGOT = "Caterium Ingot"
    ALUMINUM_INGOT = "Aluminum Ingot"
    AI_LIMITER = "AI Limiter"
    ALCLAD_ALUMINUM_SHEET = "Alclad Sheet"
    ALUMINUM_CASING = "Aluminum Casing"
    ALUMINUM_SCRAP = "Aluminum Scrap"
    ALUMINA_SOLUTION = "Alumina Solution"
    BATTERY = "Battery"
    BLACK_POWDER = "Black Powder"
    CABLE = "Cable"
    CIRCUIT_BOARD = "Circuit Board"
    COMPACTED_COAL = "Compacted Coal"
    COMPUTER = "Computer"
    CONCRETE = "Concrete"
    COOLING_SYSTEM = "Cooling System"
    COPPER_POWDER = "Copper Dust"
    COPPER_SHEET = "Copper Sheet"
    CRYSTAL_OSCILLATOR = "Crystal Oscillator"
    ELECTROMAGNETIC_CONTROL_ROD = "Electromagnetic Control Rod"
    ENCASED_INDUSTRIAL_BEAM = "Encased Industrial Beam"
    ENCASED_PLUTONIUM_CELL = "Encased Plutonium Cell"
    ENCASED_URANIUM_CELL = "Encased Uranium Cell"
    EMPTY_TANK = "Empty Fluid Tank"
    EMPTY_CANISTER = "Empty Canister"
    FABRIC = "Fabric"
    FUEL = "Fuel"
    FUSED_MODULAR_FRAME = "Fused Modular Frame"
    HEAT_SINK = "Heat Sink"
    HEAVY_MODULAR_FRAME = "Heavy Modular Frame"
    HEAVY_OIL_RESIDUE = "Heavy Oil Residue"
    HIGH_SPEED_CONNECTOR = "High Speed Connector"
    IRON_PLATE = "Iron Plate"
    IRON_ROD = "Iron Rod"
    MODULAR_FRAME = "Modular Frame"
    MOTOR = "Motor"
    NITRIC_ACID = "Nitric Acid"
    NON_FISSILE_URANIUM = "Non Fissile Uranium"
    PETROLEUM_COKE = "Petroleum Coke"
    PLASTIC = "Plastic"
    PLUTONIUM_FUEL_ROD = "Plutonium Fuel Rod"
    PLUTONIUM_PELLET = "Plutonium Pellet"
    PRESSURE_CONVERSION_CUBE = "Pressure Conversion Cube"
    POLYMER_RESIN = "Polymer Resin"
    QUICKWIRE = "Quickwire"
    RADIO_CONTROL_UNIT = "Radio Control Unit"
    REINFORCED_IRON_PLATE = "Reinforced Iron Plate"
    ROTOR = "Rotor"
    RUBBER = "Rubber"
    SCREWS = "Screws"
    SILICA = "Silica"
    STATOR = "Stator"
    STEEL_BEAM = "Steel Beam"
    STEEL_PIPE = "Steel Pipe"
    SULFURIC_ACID = "Sulfuric Acid"
    SUPERCOMPUTER = "Super Computer"
    TURBO_FUEL = "Turbo Fuel"
    TURBO_MOTOR = "Turbo Motor"
    URANIUM_FUEL_ROD = "Uranium Fuel Rod"
    URANIUM_WASTE = "Uranium Waste"
    PLUTONIUM_WASTE = "Plutonium Waste"
    WIRE = "Wire"
    SMART_PLATING = "Project Part: Smart Plating"
    VERSATILE_FRAMEWORK = "Project Part: Versatile Framework"
    AUTOMATED_WIRING = "Project Part: Automated Wiring"
    MODULAR_ENGINE = "Project Part: Modular Engine"
    ADAPTIVE_CONTROL_UNIT = "Project Part: Adaptive Control Unit"
    MAGNETIC_FIELD_GENERATOR = "Project Part: Magnetic Field Generator"
    ASSEMBLY_DIRECTOR_SYSTEM = "Project Part: Assembly Director System"
    THERMAL_PROPULSION_ROCKET = "Project Part: Thermal Propulsion Rocket"
    NUCLEAR_PASTA = "Project Part: Nuclear Pasta"
    ALIEN_PROTEIN = "Alien Protein"
    HOG_REMAINS = "Hog Remains"
    SPITTER_REMAINS = "Spitter Remains"
    HATCHER_REMAINS = "Hatcher Remains"
    STINGER_REMAINS = "Stinger Remains"
    MYCELIA = "Mycelia"
    LEAVES = "Leaves"
    FLOWER_PETALS = "Flower Petals"
    COLOR_CARTRIDGE = "Color Cartridge"
    PACKAGED_NITROGEN_GAS = "Packaged Nitrogen Gas"
    PACKAGED_TURBO_FUEL = "Packaged Turbo Fuel"
    SMOKELESS_POWDER = "Smokeless Powder"
    CLUSTER_NOBELISK = "Cluster Nobelisk"
    GAS_NOBELISK = "Gas Nobelisk"
    NUKE_NOBELISK = "Nuke Nobelisk"
    PULSE_NOBELISK = "Pulse Nobelisk"
    NOBELISK = "Nobelisk"
    HOMING_RIFLE_AMMO = "Homing Rifle Ammo"
    TURBO_RIFLE_AMMO = "Turbo Rifle Ammo"
    RIFLE_AMMO = "Rifle Ammo"
    EXPLOSIVE_REBAR = "Explosive Rebar"
    SHATTER_REBAR = "Shatter Rebar"
    STUN_REBAR = "Stun Rebar"
    IRON_REBAR = "Iron Rebar"
    GAS_FILTER = "Gas Filter"
    IODINE_INFUSED_FILTER = "Iodine Infused Filter"
    LIQUID_BIOFUEL = "Liquid BioFuel"
    SOLID_BIOFUEL = "Solid BioFuel"
    ORGANIC_DATA_CAPSULE = "Organic Data Capsule"
    MEDICINAL_INHALER = "Medicinal Inhaler"
    PARACHUTE = "Parachute"
    XENO_ZAPPER = "Xeno-Zapper"
    BACON_AGARIC = "Bacon Agaric"
    SAM_ORE = "SAM Ore"
    OBJECT_SCANNER = "Object Scanner"
