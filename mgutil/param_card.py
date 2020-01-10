#!/usr/bin/env python

from collections import namedtuple, defaultdict
from enum import Enum
import re
import string
import sys
from dataclasses import dataclass, field


characters = string.ascii_letters + string.digits

@dataclass
class particle():
    pdg: float = 0
    width: dict = field(default_factory=dict)
    branching: dict = field(default_factory=dict)
    mass: float = -1

@dataclass
class param_card():
    text: str = ''
    particles: dict = field(default_factory=dict)
    parameters: dict = field(default_factory=dict)
    states = Enum("states",["no_block","in_decay_block","in_mass_block","in_parameter_block"])
    def read_file(self, path_to_card):
        """
        """
        self._clear()
        with open(path_to_card) as infile:
            self.text = infile.read()
        self._parse()

    def _clear(self):
        self.particles = {}
        self.parameters = {}
        self.text = ''

    def _parse(self):
        lines = self.text.splitlines()
        # Output is stored in a dictionary
        # that maps PDG ID -> particle structs
        particles = defaultdict(lambda : particle())
        parameters = {}

        # Iterate over lines
        state = self.states.no_block
        for line in lines:
            if state == self.states.no_block:
                # Default state for looping
                # Check if this line is the start
                # of a block we recognize and take
                # appropriate action
                if(line.startswith("DECAY")):
                    state = self.states.in_decay_block
                    parts = line.split()
                    current_pdg = int(parts[1])
                    total_width = float(parts[2])
                    current_particle = particles[current_pdg]
                    current_particle.pdg = current_pdg
                    current_particle.width["total"] = total_width
                    current_particle.branching["total"] = 1.
                    continue
                if(line.startswith("BLOCK MASS")):
                    state = self.states.in_mass_block
                    continue
                if(re.match('BLOCK (NP|SMINPUTS|YUKAWA|DM).*', line)):
                    state = self.states.in_parameter_block
                    continue
            elif state == self.states.in_mass_block:
                # Block with one particle mass per line
                # The mass is saved both as a particle
                # attribute as well as as a parameter
                if(line.startswith("#")):
                    state = self.states.no_block
                    continue
                pdg, mass, _, parname = line.split()[:4]
                pdg = int(pdg)
                particles[pdg].mass = float(mass)
                parameters[parname] = float(mass)
            elif state == self.states.in_parameter_block:
                # Block with one parameter per line
                # This state covers different block names
                # and we do not differentiate between them
                # since parameter names are always unique
                if(line.startswith("#")):
                    state = self.states.no_block
                    continue
                _, parval, _, parname = line.split()
                parameters[parname] = float(parval)
            elif state == self.states.in_decay_block:
                # Block with one decay channel per line
                if(line.startswith("#") and not any([x in line for x in characters])):
                    state = self.states.no_block
                    continue
                if(line.startswith("#  BR")):
                    continue
                final_state=[]
                parts = line.split()
                br = parts[0]
                nfinal = int(parts[1])
                assert(nfinal>0)
                for p in parts[2:2+nfinal]:
                    final_state.append(p)
                width = parts[-1]

                final_state_string = ",".join(sorted(final_state))
                current_particle.branching[final_state_string] = float(br)
                current_particle.width[final_state_string] = float(width)
                continue


            else:
                raise RuntimeError("Undefined state: " + state)

        self.particles = dict(particles)
        self.parameters = parameters
        return True