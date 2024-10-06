# Binary Demo

An example project built with [pybind11](https://github.com/pybind/pybind11) and
scikit-build-core. Python 3.8+ (see older commits for older versions of Python).


## Installation

- clone this repository
- `pip install ./binary_demo`

## CI Examples

There are examples for CI in `.github/workflows`. A simple way to produces
binary "wheels" for all platforms is illustrated in the "wheels.yml" file, using
[`cibuildwheel`][].

## Test call

```python
import binary_demo

binary_demo.add(1, 2)
```

[`cibuildwheel`]: https://cibuildwheel.readthedocs.io
