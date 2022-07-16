# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 09:07:36 2021

@author: frank
"""

from pathlib import Path

import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

from PySpice.Doc.ExampleTools import find_libraries
from PySpice.Probe.Plot import plot
from PySpice.Spice.Library import SpiceLibrary
from PySpice.Spice.Netlist import SubCircuitFactory
from PySpice.Spice.Parser import SpiceParser
from PySpice.Unit import *

libraries_path = find_libraries()
print(libraries_path)
spice_library = SpiceLibrary(libraries_path)

class PowerIn(SubCircuitFactory):
    __name__ = 'PowerIn'
    __nodes__ = ('plus','minus')
    
    def __init__(self):
        super().__init__()
        self.V('positive', 'plus', 'minus', 6.0@u_V)
        

directory_path = Path(__file__).resolve().parent
kicad_netlist_path = directory_path.joinpath('osc.cir')
print(kicad_netlist_path)

parser = SpiceParser(path=str(kicad_netlist_path))

circuit = parser.build_circuit(ground='GNDREF')

circuit.include(spice_library['2N5134'])
circuit.include(spice_library['2N5139'])

for subcircuit in (PowerIn()):
    circuit.subcircuit(subcircuit)

print(str(circuit))

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.transient(step_time=100@u_us, end_time=3@u_ms)

figure, ax = plt.subplots(figsize=(20, 10))
#ax.plot(analysis['2']) # JackIn input
ax.plot(analysis['Net-_D1-Pad2_']) # Horiz output
ax.legend(('Vin [V]', 'Vout [V]'), loc=(.8,.8))
ax.grid()
ax.set_xlabel('t [s]')
ax.set_ylabel('[V]')

plt.tight_layout()
plt.show()
