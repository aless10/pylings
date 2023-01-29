# pylings

This 'project' is inspired by [rustlings](https://github.com/rust-lang/rustlings) and it aims to be the pythonic version of it.


## Getting Started

You will need to have python>=3.7 installed. You can get it by visiting [](https://www.python.org/downloads/).

## MacOS/Linux

Just run:

```bash
curl -L https://raw.githubusercontent.com/aless10/pylings/main/install.sh | bash
# Or if you want it to be installed to a different path:
curl -L https://raw.githubusercontent.com/aless10/pylings/main/install.sh | bash -s mypath/
```

This will install pylings and give you access to the `pylings` command. Run it to get started!


## Manually

Basically: Clone the repository at the latest tag, run `cargo install --path .`.

```bash
# find out the latest version at https://github.com/rust-lang/rustlings/releases/latest (on edit 5.3.0)
git clone -b 0.1.0 --depth 1 https://github.com/aless10/pylings
cd pylings
poetry install
```

Then, same as above, run `poetry run pylings` to get started.