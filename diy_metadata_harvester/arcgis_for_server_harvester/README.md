# ArcGIS for Server metadata harvester

## Introduction

Creates CKAN metadata from ArcGIS for Server REST services. 

## Usage

In a virtual environment:

```bash
pip install -r requirements
python .\src\main.py <arcgis-for-server-url> <ckan-url> <ckan-api-token> <ckan-organization-id>
```
## Documentation

The code is documented using docstrings. Use pdoc to read them in a web browser.

In a virtual environment (can be the virtual environment for this project):

```bash
pip install -r requirements
pdoc .\src\
```