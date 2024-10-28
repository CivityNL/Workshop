# DataTrial

## Introduction

What could possibly go wrong? Well, quite a lot actually when working with heterogeneous datasets. This program provides examples on what does work and what does not work when uploading resources (CSV, shape file, GeoPackage) to Dataplatform/Datacatalog.

## Adding the test-datasets to CKAN

To run the program:
1. Create a virtual environment
2. Install dependencies from requirements.txt

The program takes two arguments: 
1. the URL of the CKAN instance in which the resources must be created. This CKAN should contain a package with the "data-trial" package ID;
2. an API token for the user who has permissions to create resources in this package. 