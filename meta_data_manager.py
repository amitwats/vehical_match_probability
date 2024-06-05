from db_utils import execute_query
from nlp import nlp
from score import Score
from config import exclude_description_mapping, threshold_mapping

class MetaDataManager:

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
        doc = nlp(vehicle_description)
        scores = []
        for param in params:
            # scores[param]=[]
            param_doc = nlp(param)
            score=Score(vehicle_description, param)
            scores.append(score)
            for token in doc:
                similariity_score = param_doc.similarity(nlp(token.text))
                similariity_score = param_doc.similarity(nlp(token.text))
                score.add_match_score(token.text,similariity_score, token.dep_)
        return scores

    def get_possible_scores(self,vehicle_description,param_type):
        # scores=self.calculate_all_make_scores(input,md.makes)
        param_mapping={ "make": self.makes,
                        "model":self.models,
                       "badge":self.badges,
                       "transmission_type": self.transmission_types,
                       "fuel_type": self.fuel_types,
                       "drive_type": self.drive_types}

        scores:list[Score]=self.calculate_all_scores(vehicle_description,param_mapping[param_type])
        input_score={}
        for score in scores:
            higher_scores=score.get_match_score_filtered(threshold_mapping[param_type],exclude_description_mapping[param_type])
            for ms in higher_scores:
                # print(ms)
                input_score[ms.compare_str]=ms.similarity_score
        if len(input_score)==0:
            input_score={"-":0}

        return input_score
    
    def populate_values_from_db(self):
        self.makes=execute_query("select DISTINCT  make from autograb_schema.vehicle; ")
        self.models=execute_query("select DISTINCT  model from autograb_schema.vehicle; ")
        self.badges=execute_query("select DISTINCT  badge from autograb_schema.vehicle; ")
        self.transmission_types=execute_query("select DISTINCT  transmission_type from autograb_schema.vehicle; ")
        self.fuel_types=execute_query("select DISTINCT  fuel_type from autograb_schema.vehicle; ")
        self.drive_types=execute_query("select DISTINCT  drive_type  from autograb_schema.vehicle; ")
