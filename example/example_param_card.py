from mgutil import param_card
from pprint import pprint

pc = param_card()
pc.read_file('param_card.dat')

print ('--- Parameters')
for parname, parval in pc.parameters.items():
    print(f'   {parname}, {parval}')


print()
print('--- Particles')
for pdg, particle in pc.particles.items():
    # The PDG ID is the dictionary key,
    # but is also saved in the particle object
    assert(pdg, particle.pdg)

    # Access trivial information
    print(f'PDG ID = {particle.pdg}, mass = {particle.mass}')

    # We can also access width information,
    # as long as it is present in the param_card
    # Note that individual channels will only be present
    # if the width of the given particle was recalculated
    # by madgraph, i.e. it was set to "AUTO"
    for key, val in particle.width.items():
        if val == 0:
            continue
        print(f'   width for decay "{key}" = {val:.2e} GeV = {100*particle.branching[key]:.1f} %')
