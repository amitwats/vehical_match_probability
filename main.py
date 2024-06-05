'''
python -m venv venv
venv\Scripts\activate
deactivate

venv\Scripts\python main.py
venv\Scripts\python -m pip install --upgrade pip
venv\Scripts\python -m pip install -r requirements.txt


'''

import psycopg2
from functools import wraps
from thefuzz import fuzz
from thefuzz import process
import spacy

import pandas as pd
import itertools

# Database connection parameters
db_host = "localhost"  # or the IP address of your PostgreSQL server
db_port = 5432  # Default port for PostgreSQL
db_name = "autograb_db"
db_user = "autograb_user"
db_password = "autograb_password"
nlp = spacy.load("en_core_web_lg")


class MatchScore:
    def __init__(self, main_str, compare_str, token_str, similarity_score, dependency_type) -> None:
        self.main_str=main_str
        self.compare_str=compare_str
        self.token_str=token_str
        self.similarity_score=similarity_score
        self.dependency_type=dependency_type

    def __repr__(self):
        return (f"MatchScore("
                f"main_str='{self.main_str}', "
                f"compare_str='{self.compare_str}', "
                f"token_str='{self.token_str}', "
                f"similarity_score={self.similarity_score}, "
                f"dependency_type='{self.dependency_type}')")
    
    def compare_similarity_score(self,num):
        if self.similarity_score==num:
            return 0
        elif self.similarity_score>num:
            return 1
        else:
            return -1

class Score:
    def __init__(self, main_str, word):
        self.main_str=main_str
        self.word=word
        self.match_scores=[]

    def add_match_score(self, token_str, similarity_score, dependency_type):
        ms=MatchScore(self.main_str,self.word,token_str=token_str,similarity_score=similarity_score, dependency_type=dependency_type)
        self.match_scores.append(ms)

    def get_match_score_filtered(self,threshold=.75, dependency_exclude=None):
        
        if dependency_exclude and threshold:
            filter_function=lambda x:x.compare_similarity_score(threshold)==1 and x.dependency_type not in dependency_exclude
        elif dependency_exclude and not threshold:
            filter_function=lambda x: x.dependency_type not in dependency_exclude
        elif not dependency_exclude and threshold:
            filter_function=lambda x:x.compare_similarity_score(threshold)==1
        else:
            filter_function=lambda x: True

        # return list(filter(lambda x:x.compare_similarity_score(threshold)==1 ,self.match_scores))
        return list(filter(filter_function ,self.match_scores))

    
    def __repr__(self):
        match_scores_string='\n'.join([str(ms) for ms in self.match_scores])
        return f"Score(main_str='{self.main_str}', word='{self.word}', match_scores=\n{match_scores_string})"



class MetaDataHolder:

    def __init__(self) -> None:
        self.makes=[]
        self.models=[]
        self.badges=[]
        self.transmission_types=[]
        self.fuel_types=[]
        self.drive_types=[]


    def __str__(self) -> str:
        return (
            f"MetaDataHolder(\n"
            f"  make={self.makes},\n"
            f"  model={self.models},\n"
            f"  badge={self.badges},\n"
            f"  transmission_type={self.transmission_types},\n"
            f"  fuel_type={self.fuel_types},\n"
            f"  drive_type={self.drive_types}\n"
            f")"
        )



    def calculate_all_scores(self, vehicle_description, params):
        # nlp = spacy.load("en_core_web_lg")
        doc = nlp(vehicle_description)
        scores = []
        for param in params:
            # scores[param]=[]
            param_doc = nlp(param)
            score=Score(vehicle_description, param)
            scores.append(score)
            for token in doc:
                similariity_score = param_doc.similarity(nlp(token.text))
                score.add_match_score(token.text,similariity_score, token.dep_)
        return scores

    def get_possible_scores(self,vehicle_description,param_type):
        # scores=self.calculate_all_make_scores(input,md.makes)
        param_mapping={ "make": md.makes,
                        "model":md.models, 
                       "badge":self.badges, 
                       "transmission_type": self.transmission_types, 
                       "fuel_type": self.fuel_types, 
                       "drive_type": self.drive_types}

        exclude_description_mapping={ "make":["pobj"], 
                        "model":[], 
                       "badge":[], 
                       "transmission_type": [], 
                       "fuel_type": [], 
                       "drive_type": []}

        threshold_mapping={ "make":0.75, 
                        "model":0.75, 
                       "badge":0.75, 
                       "transmission_type": 0.75, 
                       "fuel_type": 0.75, 
                       "drive_type": 0.75
                       }


        scores=self.calculate_all_scores(vehicle_description,param_mapping[param_type])
        input_score={}
        for score in scores:
            higher_scores=score.get_match_score_filtered(threshold_mapping[param_type],exclude_description_mapping[param_type])
            for ms in higher_scores:
                # print(ms)
                input_score[ms.compare_str]=ms.similarity_score
        if len(input_score)==0:
            input_score={"-":0}
        
        return input_score


def read_file_to_list(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    return lines

def db_connect(func):
    @wraps(func)
    def with_connection(*args, **kwargs):
        conn = None
        try:
            conn = psycopg2.connect(
                dbname=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port
            )
            result = func(conn, *args, **kwargs)
            return result
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()
    return with_connection

@db_connect
def execute_query(conn, query):
    with conn.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
        result = [row[0] for row in result]
        return result

def get_dataframe(data):
    # data = {
    #     "make": {"Volkswagen": 1.0},
    #     "model": {"Golf": 1.0},
    #     "badge": {
    #         "132TSI Comfortline Allspace": 0.8769095459110375,
    #         "110TSI Comfortline": 0.9999999713304009,
    #         "132TSI Comfortline": 0.9999999713304009,
    #         "110TSI Comfortline Allspace": 0.8769095459110375
    #     },
    #     "transmission_type": {"Automatic": 1.0},
    #     "fuel_type": {"Petrol": 1.0},
    #     "drive_type": {
    #         "Rear Wheel Drive": 0.8150659445886941,
    #         "Front Wheel Drive": 0.7666825475513469
    #     }
    # }

    # Generate all permutations of the data
    permutations = list(itertools.product(
        data["make"].items(),
        data["model"].items(),
        data["badge"].items(),
        data["transmission_type"].items(),
        data["fuel_type"].items(),
        data["drive_type"].items()
    ))

    # Prepare the DataFrame
    rows = []
    for perm in permutations:
        row = {
            "make": perm[0][0], "make_value": perm[0][1],
            "model": perm[1][0], "model_value": perm[1][1],
            "badge": perm[2][0], "badge_value": perm[2][1],
            "transmission_type": perm[3][0], "transmission_type_value": perm[3][1],
            "fuel_type": perm[4][0], "fuel_type_value": perm[4][1],
            "drive_type": perm[5][0], "drive_type_value": perm[5][1]
        }
        rows.append(row)

    # Create the DataFrame
    df = pd.DataFrame(rows)
    return df


if __name__ == '__main__':

    res=execute_query("select * from autograb_schema.vehicle limit 5")
    md=MetaDataHolder()
    
    md.makes=execute_query("select DISTINCT  make from autograb_schema.vehicle; ")
    md.models=execute_query("select DISTINCT  model from autograb_schema.vehicle; ")
    md.badges=execute_query("select DISTINCT  badge from autograb_schema.vehicle; ")
    md.transmission_types=execute_query("select DISTINCT  transmission_type from autograb_schema.vehicle; ")
    md.fuel_types=execute_query("select DISTINCT  fuel_type from autograb_schema.vehicle; ")
    md.drive_types=execute_query("select DISTINCT  drive_type  from autograb_schema.vehicle; ")

    inputs=read_file_to_list("input.txt")


    input_make_score={}
    # for input in inputs:
    #     input_make_score[input]={}
    #     input_make_score[input]["make"]=md.get_possible_scores(input, "make")
    #     input_make_score[input]["model"]=md.get_possible_scores(input, "model")
    #     input_make_score[input]["badge"]=md.get_possible_scores(input, "badge")
    #     input_make_score[input]["transmission_type"]=md.get_possible_scores(input, "transmission_type")
    #     input_make_score[input]["fuel_type"]=md.get_possible_scores(input, "fuel_type")
    #     input_make_score[input]["drive_type"]=md.get_possible_scores(input, "drive_type")
    #     break
        
    input_make_score={}
    input=inputs[0]
    input_make_score[input]={}
    input_make_score[input]["make"]=md.get_possible_scores(input, "make")
    input_make_score[input]["model"]=md.get_possible_scores(input, "model")
    input_make_score[input]["badge"]=md.get_possible_scores(input, "badge")
    input_make_score[input]["transmission_type"]=md.get_possible_scores(input, "transmission_type")
    input_make_score[input]["fuel_type"]=md.get_possible_scores(input, "fuel_type")
    input_make_score[input]["drive_type"]=md.get_possible_scores(input, "drive_type")
        # scores=md.calculate_all_make_scores(input,md.makes)
        # input_make_score[input]={}
        # # print(len(scores))
        # valid_scores=[]
        # for score in scores:
        #     higher_scores=score.get_match_score_filtered(.75,["pobj"])

        #     # if len(higher_scores)
        #     for ms in higher_scores:
        #         input_make_score[input][ms.token_str]=ms.similarity_score
        #     # if len(higher_scores)>0:
        #     #     input_make_score
        #     #     print(higher_scores)

    weitage={
        "make": 0.2,
        "model":0.4, 
        "badge":0.05, 
        "transmission_type": 0.2, 
        "fuel_type": 0.1, 
        "drive_type": 0.05
    }


    for key, value in input_make_score.items():
        print(key)
        print(value)
        df=get_dataframe(value)
        df['input']=key
        df['weighted_average'] = df.apply(lambda row: (
            row['make_value'] * weitage['make'] +
            row['model_value'] * weitage['model'] +
            row['badge_value'] * weitage['badge'] +
            row['transmission_type_value'] * weitage['transmission_type'] +
            row['fuel_type_value'] * weitage['fuel_type'] +
            row['drive_type_value'] * weitage['drive_type']
            ) , axis=1)
        df_grouped=df.groupby(["make", "model", "badge", "transmission_type", "fuel_type", "drive_type"], as_index=False)['weighted_average'].max()
        print(df)
        print(df_grouped)

        # for key_inner, value_inner in value.items():
        #     print(f"{key_inner}: {value_inner}")

    # print(input_make_score)

    # print(type(res))
    # print(md)

