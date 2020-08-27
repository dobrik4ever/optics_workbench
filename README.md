# Optics workbench

## Usage

import a ```Bench``` and ```Components``` from ```Optics.py``` file and intialize your bench

```python
from Optics_workbench.Optics import Components, Bench
lens = Components.lens
space = Components.space

bench = Bench()
bench.add(space(10))
bench.add(lens(10))
bench.add(space(15))

bench.render(
    height = 10,
    angle = 1/3,
    rays_number = 10,
    point_source = True,
    color = 'r'
)


bench.render(
    height = 0,
    angle = 1/3,
    rays_number = 10,
    point_source = True,
    color = 'g'
)

print(bench)
bench.show()
```
