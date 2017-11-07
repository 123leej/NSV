# NSV
this is SDN project Network simulate visualizer for Biomimicry Adhoc nodes

## Getting Started

It will update soon...

## Setting Virtual Environment

### Setting virtual environment for Development
virtual environment activation (you must make your own virtual environments not mine)
Linux:
```sh
. venv/bin/activate
```
Windows:
```sh
cd ~/NSV/venv/Scripts
activate
```

(venv) has appear in front of command line and install require packages.
```sh
(venv)username@desktop$ pip install -r requirements.txt
```
NOTE : Do not push your virtual environment folder !! (if it comes up to changed file set as ignore folder)

### Developing with IDE
set this python file to interpreter
```sh
venvv/bin/python
```
### Install packages in virtual environment
if you installed new package in virtual environment you have to update requirements.txt

1. activate your virtual environment

2. record your all installed package in requirements.txt
```sh
(venv)username@desktop$ pip freeze > requirements.txt
```

3. push on github your updated requirements.txt 

## Built With
* [Python3](https://www.python.org/) - NSV development language
* [Qt designer](https://www.qt.io/) - Make Gui for Python
