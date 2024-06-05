# Database connection parameters


db_host = "localhost"  # or the IP address of your PostgreSQL server
db_port = 5432  # Default port for PostgreSQL
db_name = "autograb_db"
db_user = "autograb_user"
db_password = "autograb_password"


# file paths
OUTPUT_PATH="output.txt"
INPUT_PATH="input.txt"


# 
vehicle_parameter_weightage={
    "make": 0.3,
    "model":0.4,
    "badge":0.05,
    "transmission_type": 0.1,
    "fuel_type": 0.1,
    "drive_type": 0.05
}


#spacy settings

exclude_description_mapping={ "make":["pobj"],
                "model":[],
                "badge":[],
                "transmission_type": [],
                "fuel_type": [],
                "drive_type": []}

threshold_mapping={ "make":0.75,
                "model":0.75,
                "badge":0.6,
                "transmission_type": 0.75,
                "fuel_type": 0.75,
                "drive_type": 0.75
                }


