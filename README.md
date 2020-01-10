# mgutil

Standalone utilities to deal with Madgraph.

## param_card

A `param_card.dat` parser. Example:

```python
from mgutil import param_card

pc = param_card()
pc.read_file('/path/to/param_card.dat')

for particle in pc.particles:
    print(particle.pdg, particle.mass, ...)

for parameter_name, parameter_value in pc.parameters.items():
    print(parameter_name, parameter_value)
```

An executable example can be found in the `example` folder.