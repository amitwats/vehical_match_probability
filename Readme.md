# Vehicle Name Matcher

The objective of this project is generate a score indicating the possibility of a casually written vehicle name when compared to a data in a database of cars with various attributes.

## Table of Contents

- [Vehicle Name Matcher](#vehicle-name-matcher)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Running in DB Docker](#running-in-db-docker)
    - [Build the container](#build-the-container)
    - [Run the image](#run-the-image)
    - [Windows](#windows)
    - [Linux and MacOS](#linux-and-macos)
  - [Running the application](#running-the-application)
  - [Fine tunning the model](#fine-tunning-the-model)

## Installation

The following are in prerequisites
* Python (v 11 and above) is installed
* PYTHONPATH is configured to point to current folder
* Docker should be installed

The master data of the vehicles and its listings is in a postgres db. In order to run this I am using a docker image.

## Running in DB Docker

### Build the container

```bash
docker build --no-cache -t autograb_postgres .
```
  
### Run the image

```bash
docker run -d --name autograb_db_container -p 5432:5432 autograb_postgres
```
This should have the DB up and running with the required data.

### Windows
1. Clone the repository:<br>
   Go to the base folder where you need to project installed
   ```bash
   git clone https://github.com/amitwats/vehical_match_probability.git
   ```
2. Switch to the project directory:
   ```bash
   cd vehical_match_probability
   ```
3. Create a virtual environment, activate it and install requirements into it:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   py -m pip install -r requirements.txt
   ```
4. You need to download a model to use SpaCy. To download the model
   ```bash
   py -m spacy download en_core_web_lg
   ```
   
### Linux and MacOS
1. Clone the repository:<br>
   Go to the base folder where you need to project installed
   ```bash
   git clone https://github.com/amitwats/fixed_width_to_csv.git
2. Switch to the project directory:
   ```bash
   cd fixed_width_to_csv
   ```
3. Create a virtual environment, activate it and install requirements into it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
4. You need to download a model to use SpaCy. To download the model
   ```bash
   python -m spacy download en_core_web_lg
   ```
   

## Running the application
To run the default parsing with the input and output. After the installation and activating the environment, run the following command.

**Windows**
```bash
   py main.py
```
**Linux/ Macos**
```bash
   python main.py
```


## Fine tunning the model
The model can be fine tuned by modifying the parameters in ***config.py ***

**vehicle_parameter_weightage** : Adjust the weights to be given to the parameters vehicle. This will fine tune as the dataset increases.

**exclude_description_mapping** : Need to add SpaCy valid dependency types that need to be excluded here.

**threshold_mapping** : The threshold mapping scores to be given here, so include or exclude more similarity scores.
