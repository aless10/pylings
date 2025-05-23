# pylings

This 'project' is inspired by [rustlings](https://github.com/rust-lang/rustlings) and it aims to be the pythonic version of it.


## Getting Started

You will need to have python>=3.7 installed. You can get it by visiting [python website](https://www.python.org/downloads/).

## MacOS/Linux

### with poetry

If you have ``poetry`` installed (or you plan to install it), run

```bash
curl -L https://raw.githubusercontent.com/aless10/pylings/main/install.sh | bash
# Or if you want it to be installed to a different path:
curl -L https://raw.githubusercontent.com/aless10/pylings/main/install.sh | bash -s mypath/
```

This will install pylings and give you access to the `poetry run pylings` command. Run it to get started!

### with virtualenv

If you want to use ``virtualenv``, run

```bash
curl -L https://raw.githubusercontent.com/aless10/pylings/main/install.sh | bash virtualenv
# Or if you want it to be installed to a different path:
curl -L https://raw.githubusercontent.com/aless10/pylings/main/install.sh | bash virtualenv -s mypath/
```

This will:

- create a virtualenvironment called ``venv``
- activate it
- install pylings and give you access to the `pylings` command. Run it to get started!


## Manually

Basically: Clone the repository at the latest tag, run `poetry install`.

```bash
# find out the latest version at https://github.com/rust-lang/rustlings/releases/latest (on edit 5.3.0)
git clone -b 0.2.0 --depth 1 https://github.com/aless10/pylings
cd pylings
poetry install
```

Then, same as above, run `poetry run pylings` to get started.