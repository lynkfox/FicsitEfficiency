from ficsit.components import ManufacturedComponents, LogisticalInput


class iMachine:
    powerUse: float  # in MW
    footprint: float  # in m^2
    width: float  # in meters
    length: float
    height: float
    tierRequired: str  # in Tier.Upgrade
    inputs: dict  # of type:number
    outputs: dict  # of type: number
    cost: dict  # of component:number


class Smelter(iMachine):
    tierRequired = 0.2
    powerUse = 4
    width = 6
    length = 9
    height = 9
    footprint = 54
    inputs = {LogisticalInput.CONVEYOR: 1}
    outputs = {LogisticalInput.CONVEYOR: 1}
    cost = {ManufacturedComponents.IRON_ROD: 5, ManufacturedComponents.WIRE: 8}


class Foundry(iMachine):
    tierRequired = 3.3
    powerUse = 16
    width = 10
    length = 9
    height = 9
    footprint = 90
    inputs = {LogisticalInput.CONVEYOR: 2}
    outputs = {LogisticalInput.CONVEYOR: 1}
    cost = {
        ManufacturedComponents.MODULAR_FRAME: 10,
        ManufacturedComponents.ROTOR: 10,
        ManufacturedComponents.CONCRETE: 20,
    }


class Constructor(iMachine):
    powerUse = 4
    footprint = 80
    tierRequired = 0.3
    width = 8
    length = 10
    height = 8
    inputs = {LogisticalInput.CONVEYOR: 1}
    outputs = {LogisticalInput.CONVEYOR: 1}
    cost = {
        ManufacturedComponents.REINFORCED_IRON_PLATE: 2,
        ManufacturedComponents.CABLE: 8,
    }


class Assembler(iMachine):
    tierRequired = 2.1
    powerUse = 15
    width = 10
    length = 15
    height = 11
    footprint = 150
    inputs = {LogisticalInput.CONVEYOR: 2}
    outputs = {LogisticalInput.CONVEYOR: 1}
    cost = {
        ManufacturedComponents.REINFORCED_IRON_PLATE: 9,
        ManufacturedComponents.ROTOR: 4,
        ManufacturedComponents.CABLE: 10,
    }


class Manufacturer(iMachine):
    tierRequired = 5.2
    powerUse = 55
    width = 18
    length = 19
    height = 12
    footprint = 342
    inputs = {LogisticalInput.CONVEYOR: 4}
    outputs = {LogisticalInput.CONVEYOR: 1}
    cost = {
        ManufacturedComponents.MOTOR: 5,
        ManufacturedComponents.HEAVY_MODULAR_FRAME: 10,
        ManufacturedComponents.CABLE: 50,
        ManufacturedComponents.PLASTIC: 50,
    }


class Refinery(iMachine):
    tierRequired = 5.1
    powerUse = 30
    width = 10
    length = 20
    height = 31
    footprint = 200
    inputs = {LogisticalInput.CONVEYOR: 1, LogisticalInput.PIPE: 1}
    outputs = {LogisticalInput.CONVEYOR: 1, LogisticalInput.PIPE: 1}
    cost = {
        ManufacturedComponents.MOTOR: 10,
        ManufacturedComponents.ENCASED_INDUTRIAL_BEAM: 10,
        ManufacturedComponents.STEEL_PIPE: 30,
        ManufacturedComponents.COPPER_SHEET: 20,
    }


class Packager(iMachine):
    tierRequired = 5.3
    powerUse = 10
    width = 8
    length = 8
    height = 12
    footprint = 64
    inputs = {LogisticalInput.CONVEYOR: 1, LogisticalInput.PIPE: 1}
    outputs = {LogisticalInput.CONVEYOR: 1, LogisticalInput.PIPE: 1}
    cost = {
        ManufacturedComponents.STEEL_BEAM: 20,
        ManufacturedComponents.RUBBER: 10,
        ManufacturedComponents.PLASTIC: 10,
    }


class Blender(iMachine):
    tierRequired = 7.1
    powerUse = 75
    width = 18
    length = 19
    height = 12
    footprint = 342
    inputs = {LogisticalInput.CONVEYOR: 2, LogisticalInput.PIPE: 2}
    outputs = {LogisticalInput.CONVEYOR: 1, LogisticalInput.PIPE: 1}
    cost = {
        ManufacturedComponents.MOTOR: 20,
        ManufacturedComponents.HEAVY_MODULAR_FRAME: 10,
        ManufacturedComponents.ALUMNIUM_CASING: 50,
        ManufacturedComponents.RADIO_CONTROL_UNIT: 5,
    }


class ParticalAccelerator(iMachine):
    tierRequired = 8.4
    powerUse = 1500
    width = 24
    length = 38
    height = 32
    footprint = 912
    inputs = {LogisticalInput.CONVEYOR: 2, LogisticalInput.PIPE: 1}
    outputs = {LogisticalInput.CONVEYOR: 1}
    cost = {
        ManufacturedComponents.RADIO_CONTROL_UNIT: 20,
        ManufacturedComponents.ELECTROMAGNETIC_CONTROL_ROD: 100,
        ManufacturedComponents.SUPERCOMPUTER: 10,
        ManufacturedComponents.COOLING_SYSTEM: 50,
        ManufacturedComponents.FUSED_MODULAR_FRAME: 20,
        ManufacturedComponents.TURBO_MOTOR: 10,
    }
