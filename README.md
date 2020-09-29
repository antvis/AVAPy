# AVAPy

> This Project is Work-In-Progress

Python implementation of AVA.

## Development

### Set your local virtual environment

Requirements should be installed in a [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

Make one under the root of this repo, for example:

```bash
> python3 -m venv venv
> source venv/bin/activate
```

### Install Requirements

```bash
> pip install wheel
> pip install setuptools
> pip install twine
> pip install pytest==4.4.1
> pip install pytest-runner==4.4
> pip install altair
```

### Tests

Write your test cases in modules under `test/`.

Run:

```bash
> python setup.py pytest
```

Daily Testing:

```bash
> pytest
> pytest -s
```

### Build

```bash
> python setup.py bdist_wheel
```

### Local Install for Demos

```bash
> pip install /path/to/dist/wheelfile.whl
```
