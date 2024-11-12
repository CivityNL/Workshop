# DataTrial

## Introduction

What could possibly go wrong? Well, quite a lot actually when working with heterogeneous datasets. This program provides examples on what does work and what does not work when uploading resources (CSV, shape file, GeoPackage) to Dataplatform/Datacatalog. In addition, this program can be used to quickly test a Datacatalog/Dataplatform instance. 

## Adding the test-datasets to CKAN

To run the program:
1. Create a virtual environment;
2. Activate the virtual environment;
3. Install dependencies from requirements.txt

```pip install -r requirements.txt```

The program requires two arguments: 
1. the URL of the CKAN instance in which the resources must be created. This CKAN should contain a package with the "data-trial" package ID. If not present, this package should be created manually. If this package is not present, the program will raise an exception;
2. an API token for the user who has permissions to create resources in this package. Log in to CKAN, click the user name in the upper right corner of the screen and go to the "API tokens" tab to generate an API token. 