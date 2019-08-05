# Greedy_method

- [Install](#install) 
- [Structure](#structure)
- [Run](#run)

## Install

This will install all the dependencies in the Pipefile by ***Pipenv***

```console
$ pipenv install
```

## Structure

    greedy_method/
        ├── edge/                   # Class of "Edge" 
        ├── fog_set/                # Class of "Fog_set", "Fog", "Vehicle"      
        ├── constant/               # Class of "Constant"
        ├── m_m_c/                  # Simulation for M/M/c
        ├── vehicle_set/            # Class of "Vehicle_set"
        ├── script/                 # Execution file in different scenarios
        ├── testcase/               # Input test file
        ├── graph/                  # Output graph 
        └── main.py                 # Original version

## Run

```console
$ pipenv run python {name.py}
```