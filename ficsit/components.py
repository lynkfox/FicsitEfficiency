class BaseComponents():
    LIMESTONE = "stone"
    IRON = "oreIron"
    COPPER = "oreCopper"
    QUARTZ = "rawQuartz"
    COAL = "coal"
    SULFUR = "sulfur"
    CATERIUM = "oreGold"
    BAUXITE = "oreBauxite"
    URANIUM = "oreUranium"

    WATER = "water"
    OIL = "liquidOil"
    NITROGEN = "nitrogenGas"

    BIOMASS = "genericBiomass"
    WOOD = "wood"


endpoints = [
    BaseComponents.LIMESTONE,
    BaseComponents.IRON,
    BaseComponents.COPPER,
    BaseComponents.QUARTZ,
    BaseComponents.COAL,
    BaseComponents.SULFUR,
    BaseComponents.CATERIUM,
    BaseComponents.BAUXITE,
    BaseComponents.URANIUM,
    BaseComponents.WATER,
    BaseComponents.OIL,
    BaseComponents.NITROGEN,
    BaseComponents.BIOMASS,
    BaseComponents.WOOD
]

class ManufacturedComponents():
    AI_LIMITER = "circuitBoardHighSpeed"
    ALCLAD_ALUMINUM_SHEET = "aluminumPlate"
    ALUMNIUM_CASING = "aluminumCasing"
    ALUMNIUM_INGOT = "aluminumIngot"
    ALUMNIUM_SCRAP = "aluminumScrap"
    ALUMINA_SOLUTION = "aluminaSolution"
    BATTERY = "battery"
    BLACK_POWDER = "gunpowder"
    CABLE = "cable"
    CIRCUIT_BOARD = "circuitBoard"
    COMPACTED_COAL = "compactedCoal"
    COMPUTER = "computer"
    CONCRETE = "cement"
    COOLING_SYSTEM = "coolingSystem"
    COPPER_POWDER = "copperDust"
    COPPER_INGOT = "copperIngot"
    COPPER_SHEET = "copperSheet"
    CRYSTAL_OSCILLATOR = "crystalOscillator"
    ELECTROMAGNETIC_CONTROL_ROD = "electromagneticControlRod"
    ENCASED_INDUTRIAL_BEAM = "steelPlateReinforced"
    ENCASED_PLUTONIUM_CELL = "plutoniumCell"
    ENCASED_URANIUM_CELL = "uraniumCell"
    EMPTY_CANISTER = "fluidCanister"
    FABRIC = "fabric"
    FUEL = "liquidFuel"
    FUSED_MODULAR_FRAME = "modularFrameFused"
    HEAT_SINK = "aluminumPlateReinforced"
    HEAVY_MODULAR_FRAME = "modularFrameHeavy"
    HEAVY_OIL_RESIDUE = "heavyOilResidue"
    HIGH_SPEED_CONNECTOR = "highSpeedConnector"
    IRON_PLATE = "ironPlate"
    IRON_ROD = "ironRod"
    MODULAR_FRAME = "modularFrame"
    MOTOR = "motor"
    NITRIC_ACID = "nitricAcid"
    NON_FISSIBLE_URANIUM = "nonFissibleUranium"
    NUCLEAR_WASTE = "nuclearWaste"
    PETROLEUM_COKE = "petroleumCoke"
    PLASTIC = "plastic"
    PLUTONIUM_FUEL_ROD = "plutoniumFuelRod"
    PLUTONIUM_PELLET = "plutoniumPellet"
    PRESSURE_CONVERSION_CUBE = "pressureConversionCube"
    POLYMER_RESIN = "polymerResin"
    QUICKWIRE = "highSpeedWire"
    RADIO_CONTROL_UNIT = "modularFrameLightweight"
    REINFORCED_IRON_PLATE = "ironPlateReinforced"
    ROTOR = "rotor"
    RUBBER = "rubber"
    SCREWS = "ironScrew"
    SILICA = "silica"
    STATOR = "stator"
    STEEL_BEAM = "steelPlate"
    STEEL_PIPE = "steelPipe"
    SULFURIC_ACID = "sulfuricAcid"
    SUPERCOMPUTER = "computerSuper"
    TURBOFUEL = "liquidTurboFuel"
    TURBO_MOTOR = "motorLightweight"
    URANIUM_FUEL_ROD = "nuclearFuelRod"
    WIRE = "wire"

class ProjectAssemblyPart():
    SMART_PLATING = "spaceElevatorPart1"
    VERSITLE_FRAMEWORK = "spaceElevatorPart2"
    AUTOMATED_WIRING = "spaceElevatorPart3"
    MODULAR_ENGINE = "spaceElevatorPart4"
    ADAPTIVE_CONTROL_UNIT = "spaceElevatorPart5"
    MAGNETIC_FIELD_GENERATOR = "spaceElevatorPart6"
    ASSEMBLY_DIRECTOR_SYSTEM = "spaceElevatorPart7"
    THERMAL_PROPULSION_ROCKET = "spaceElevatorPart8"
    NUCLEAR_PASTA = "spaceElevatorPart9"

class Equipment():
    BEACON = "beacon"
    RIFLE_CARTRIDGE = "cartridgeStandard"

class Ingots():
    IRON = "ironIngot"
    COPPER = "copperIngot"
    STEEL = "steelIngot"
    CATERIUM = "goldIngot"
    ALUMINUM = "aluminumIngot"


display_name_mapping = {
    BaseComponents.LIMESTONE: "Limestone",
    BaseComponents.IRON: "Iron Ore",
    BaseComponents.COPPER: "Copper Ore",
    BaseComponents.QUARTZ: "Raw Quartz",
    BaseComponents.COAL: "Raw Coal",
    BaseComponents.SULFUR: "Raw Sulfur",
    BaseComponents.CATERIUM: "Caterium Ore",
    BaseComponents.BAUXITE: "Bauxite Ore",
    BaseComponents.URANIUM: "Uranium Ore",
    BaseComponents.WATER: "Water",
    BaseComponents.OIL: "Oil",
    BaseComponents.NITROGEN: "Nitrogen Gas",
    ManufacturedComponents.AI_LIMITER: "AI Limiter",
    ManufacturedComponents.ALCLAD_ALUMINUM_SHEET: "Alclad Aluminum Sheet",
    ManufacturedComponents.ALUMNIUM_CASING: "Alumnium Casing",
    ManufacturedComponents.ALUMNIUM_INGOT: "Alumnium Ingot",
    ManufacturedComponents.ALUMNIUM_SCRAP: "Aluminum Scrap",
    ManufacturedComponents.ALUMINA_SOLUTION: "Alumina Solution",
    ManufacturedComponents.BATTERY: "Battery",
    ManufacturedComponents.BLACK_POWDER: "Black Powder",
    ManufacturedComponents.CABLE: "Cable",
    ManufacturedComponents.CIRCUIT_BOARD: "Circuit Board",
    ManufacturedComponents.COMPACTED_COAL: "Compacted Coal",
    ManufacturedComponents.COMPUTER: "Computer",
    ManufacturedComponents.CONCRETE: "Concrete",
    ManufacturedComponents.COOLING_SYSTEM: "Cooling System",
    ManufacturedComponents.COPPER_POWDER: "Copper Dust",
    ManufacturedComponents.COPPER_INGOT: "Copper Ingot",
    ManufacturedComponents.COPPER_SHEET: "Copper Sheet",
    ManufacturedComponents.CRYSTAL_OSCILLATOR: "Crystal Oscillator",
    ManufacturedComponents.ELECTROMAGNETIC_CONTROL_ROD: "Electromagnetic Control Rod",
    ManufacturedComponents.EMPTY_CANISTER: "Empty Canister",
    ManufacturedComponents.ENCASED_INDUTRIAL_BEAM: "Encased Industrial Beam",
    ManufacturedComponents.ENCASED_PLUTONIUM_CELL: "Encased Plutonium Cell",
    ManufacturedComponents.ENCASED_URANIUM_CELL: "Encased Uranium Cell",
    ManufacturedComponents.FABRIC: "Fabric",
    ManufacturedComponents.FUEL: "Fuel",
    ManufacturedComponents.FUSED_MODULAR_FRAME: "Fused Modular Frame",
    ManufacturedComponents.HEAT_SINK: "Heat Sink",
    ManufacturedComponents.HEAVY_MODULAR_FRAME: "Heavy Modular Frame",
    ManufacturedComponents.HEAVY_OIL_RESIDUE: "Heavy Oil Residue",
    ManufacturedComponents.HIGH_SPEED_CONNECTOR: "High-Speed Connector",
    ManufacturedComponents.IRON_PLATE: "Iron Plate",
    ManufacturedComponents.IRON_ROD: "Iron Rod",
    ManufacturedComponents.MODULAR_FRAME: "Modular Frame",
    ManufacturedComponents.MOTOR: "Motor",
    ManufacturedComponents.NITRIC_ACID: "Nitric Acid",
    ManufacturedComponents.NON_FISSIBLE_URANIUM: "Non-Fissible Uranium",
    ManufacturedComponents.NUCLEAR_WASTE: "Nuclear Waste",
    ManufacturedComponents.PETROLEUM_COKE: "Petroleum Coke",
    ManufacturedComponents.PLASTIC: "Plastic",
    ManufacturedComponents.PLUTONIUM_FUEL_ROD: "Plutonium Fuel Rod",
    ManufacturedComponents.PLUTONIUM_PELLET: "Plutonium Pellet",
    ManufacturedComponents.POLYMER_RESIN: "Polymer Resin",
    ManufacturedComponents.PRESSURE_CONVERSION_CUBE: "Pressure Conversion Cube",
    ManufacturedComponents.QUICKWIRE: "Quickwire",
    ManufacturedComponents.RADIO_CONTROL_UNIT: "Radio Control Unit",
    ManufacturedComponents.REINFORCED_IRON_PLATE: "Reinforced Iron plate",
    ManufacturedComponents.ROTOR: "Rotor",
    ManufacturedComponents.RUBBER: "Rubber",
    ManufacturedComponents.SCREWS: "Screws",
    ManufacturedComponents.SILICA: "Silica",
    ManufacturedComponents.STATOR: "Stator",
    ManufacturedComponents.STEEL_BEAM: "Steel Beam",
    ManufacturedComponents.STEEL_PIPE: "Steel Pipe",
    ManufacturedComponents.SULFURIC_ACID: "Sulfuric Acid",
    ManufacturedComponents.SUPERCOMPUTER: "Supercomputer",
    ManufacturedComponents.TURBOFUEL: "Turbofuel",
    ManufacturedComponents.TURBO_MOTOR: "Turbo Motor",
    ManufacturedComponents.URANIUM_FUEL_ROD: "Uranium Fuel Rod",
    ManufacturedComponents.WIRE: "Wire",
    ProjectAssemblyPart.SMART_PLATING: "Smart Plating",
    ProjectAssemblyPart.VERSITLE_FRAMEWORK: "Versitile Framework",
    ProjectAssemblyPart.AUTOMATED_WIRING: "Automated Wiring",
    ProjectAssemblyPart.MODULAR_ENGINE: "Modular Engine",
    ProjectAssemblyPart.ADAPTIVE_CONTROL_UNIT: "Adaptive Control Unit",
    ProjectAssemblyPart.MAGNETIC_FIELD_GENERATOR: "Magnetic Field Generator",
    ProjectAssemblyPart.ASSEMBLY_DIRECTOR_SYSTEM: "Assembly Director System",
    ProjectAssemblyPart.THERMAL_PROPULSION_ROCKET: "Thermal Propulsion Rocket",
    ProjectAssemblyPart.NUCLEAR_PASTA: "Nuclear Pasta",
    Ingots.IRON : "Iron Ingot",
    Ingots.COPPER: "Copper Ingot",
    Ingots.STEEL: "Steel Ingot",
    Ingots.CATERIUM: "Caterium Ingot",
    Ingots.ALUMINUM: "Aluminum Ingot",
    Equipment.BEACON: "Beacon",
    Equipment.RIFLE_CARTRIDGE: "Rifle Cartridge"
}