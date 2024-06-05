from thefuzz import fuzz

import pandas as pd
import itertools
import warnings

from db_utils import get_df_from_db
from meta_data_manager import MetaDataManager
from config import INPUT_PATH, OUTPUT_PATH, vehicle_parameter_weightage

# Ignore all warnings
warnings.filterwarnings("ignore")


def read_file_to_list(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    return lines

def get_all_combination_dataframe(data):
    # Generate all permutations of the data
    # for all the makes, models, etc listed 
    permutations = list(itertools.product(
        data["make"].items(),
        data["model"].items(),
        data["badge"].items(),
        data["transmission_type"].items(),
        data["fuel_type"].items(),
        data["drive_type"].items()
    ))

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

def get_max_listing_df(merged_df,listings_df):
    combined_df = pd.merge(merged_df, listings_df, left_on='id', right_on='vehicle_id')
    count_series = combined_df.groupby('id_x').size()
    max_id = count_series.idxmax()
    result_row = merged_df[merged_df['id'] == max_id]

    return result_row

def get_non_hyphen_values(row):
    ret_text_list=[]
    for col_name in ['make', 'model', 'badge', 'transmission_type', 'fuel_type', 'drive_type']:
        if row[col_name]!="-":
            ret_text_list.append(row[col_name])
    
    return " ".join(ret_text_list)

def write_output(df):
    with open(OUTPUT_PATH, 'w') as file:

        for _, row in df.iterrows():
            file.write(f"Input: {row['input']}\n")
            file.write(f"Vehicle ID: {row['id']}\n")
            file.write(f"Confidence: {round( row['match_score']*10,1)}\n\n")




def get_heighest_probable_df(md, input):
    input_make_score={}
    input_make_score["make"]=md.get_possible_scores(input, "make")
    input_make_score["model"]=md.get_possible_scores(input, "model")
    input_make_score["badge"]=md.get_possible_scores(input, "badge")
    input_make_score["transmission_type"]=md.get_possible_scores(input, "transmission_type")
    input_make_score["fuel_type"]=md.get_possible_scores(input, "fuel_type")
    input_make_score["drive_type"]=md.get_possible_scores(input, "drive_type")
    possible_combinations_df=get_all_combination_dataframe(input_make_score)
    possible_combinations_df['input']=input
    possible_combinations_df['match_score'] = possible_combinations_df.apply(lambda row: (
            row['make_value'] * vehicle_parameter_weightage['make'] +
            row['model_value'] * vehicle_parameter_weightage['model'] +
            row['badge_value'] * vehicle_parameter_weightage['badge'] +
            row['transmission_type_value'] * vehicle_parameter_weightage['transmission_type'] +
            row['fuel_type_value'] * vehicle_parameter_weightage['fuel_type'] +
            row['drive_type_value'] * vehicle_parameter_weightage['drive_type']
            ) , axis=1)
    possible_combinations_grouped_df=possible_combinations_df.groupby(["make", "model", "badge", "transmission_type", "fuel_type", "drive_type"], as_index=False)['match_score'].max()
    possible_combinations_grouped_df['input']=input
    return possible_combinations_grouped_df


def generate_input_scores(inputs:list[str]):
    md=MetaDataManager()
    md.populate_values_from_db()

    result_df=None

    vehicle_df=    get_df_from_db("SELECT id, make, model, badge, transmission_type, fuel_type, drive_type FROM autograb_schema.vehicle")
    listings_df = get_df_from_db(" select id,vehicle_id,url,price,kms from autograb_schema.listing")

    vehicle_df["all_params"]=vehicle_df['make'] + ' ' + \
        vehicle_df['model'] + ' ' + \
        vehicle_df['badge'] + ' ' + \
        vehicle_df['transmission_type'] + ' ' + \
        vehicle_df['fuel_type'] + ' ' + \
        vehicle_df['drive_type']

    for input in inputs:


        probable_df = get_heighest_probable_df(md, input)

        merged_df = pd.merge(
            vehicle_df,
            probable_df,
            on=['make', 'model', 'badge', 'transmission_type', 'fuel_type', 'drive_type']
        )

        if merged_df.shape[0]==0: # no exact matches
            #look for aproximate matches
            v_df=vehicle_df.copy()
            v_df["match_score"]=0
            probable_df['all_params']= probable_df.apply(lambda row: get_non_hyphen_values(row), axis=1)

            for index, row_possible_combinations_grouped_df in probable_df.iterrows():
                v_df["match_score"]=\
                    v_df.apply(lambda row: fuzz.ratio(row['all_params'], row_possible_combinations_grouped_df['all_params']), axis=1)/100
                
                top_result=v_df.sort_values(by="match_score", ascending=False).iloc[[0]]
                top_result['input']=input
                if index==0:
                    merged_df=top_result
                else:
                    merged_df= pd.concat([merged_df,top_result], ignore_index=True)
            
            merged_df=merged_df.sort_values(by="match_score", ascending=False).iloc[[0]]
        
        if merged_df.shape[0]>1: # more than one row did match
            merged_df=get_max_listing_df(merged_df,listings_df)
        
        
        if result_df is None: # first time populating
            result_df=merged_df
        else:
            result_df=pd.concat([result_df,merged_df], ignore_index=True)
    return result_df


if __name__ == '__main__':
    inputs=read_file_to_list(INPUT_PATH)
    data=generate_input_scores(inputs)
    print(data)
    write_output(data)


