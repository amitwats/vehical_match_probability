import spacy

nlp = spacy.load("en_core_web_lg")

def method(description):
    doc = nlp(description)

    make = None
    model = None
    badge = None
    transmission_type = None
    fuel_type = None
    drive_type = None

    makes = ['Volkswagen', 'Toyota', 'VW']  # Add more makes as needed
    transmission_types = ['Automatic', 'Manual']
    fuel_types = ['Petrol', 'Diesel', 'Electric', 'Hybrid']
    drive_types = ['Front Wheel Drive', 'Rear Wheel Drive', 'All Wheel Drive', '4WD', '4x4']

    for token in doc:
        # Extract make
        if token.text in makes:
            make = token.text
        # Extract model and badge if make is found
        elif make and not model:
            model = token.text
        elif make and model and not badge:
            badge = token.text
        # Extract transmission type
        elif token.text in transmission_types:
            transmission_type = token.text
        # Extract fuel type
        elif token.text in fuel_types:
            fuel_type = token.text
        # Extract drive type
        elif " ".join([token.text for token in doc[token.i:token.i+3]]) in drive_types:
            drive_type = " ".join([token.text for token in doc[token.i:token.i+3]])
        elif " ".join([token.text for token in doc[token.i:token.i+2]]) in drive_types:
            drive_type = " ".join([token.text for token in doc[token.i:token.i+2]])

    return {
        'make': make,
        'model': model,
        'badge': badge,
        'transmission_type': transmission_type,
        'fuel_type': fuel_type,
        'drive_type': drive_type
    }



    # def calculate_all_make_scores(self, vehicle_description, params):
    #     # nlp = spacy.load("en_core_web_lg")
    #     doc = nlp(vehicle_description)
    #     scores = []
    #     for param in params:
    #         # scores[param]=[]
    #         param_doc = nlp(param)
    #         score=Score(vehicle_description, param)
    #         scores.append(score)
    #         for token in doc:
    #             similariity_score = param_doc.similarity(nlp(token.text))
    #             score.add_match_score(token.text,similariity_score, token.dep_)
    #     return scores

    # def get_possible_make_scores(self,vehicle_description):
    #     # scores=self.calculate_all_make_scores(input,md.makes)
    #     scores=self.calculate_all_make_scores(vehicle_description,md.makes)
    #     input_make_score={}
    #     for score in scores:
    #         higher_scores=score.get_match_score_filtered(.75,["pobj"])
    #         for ms in higher_scores:
    #             print(ms)
    #             input_make_score[ms.compare_str]=ms.similarity_score
        
    #     return input_make_score


    # def calculate_all_model_scores(self, vehicle_description, params):
    #     # nlp = spacy.load("en_core_web_lg")
    #     doc = nlp(vehicle_description)
    #     scores = []
    #     for param in params:
    #         # scores[param]=[]
    #         param_doc = nlp(param)
    #         score=Score(vehicle_description, param)
    #         scores.append(score)
    #         for token in doc:
    #             similariity_score = param_doc.similarity(nlp(token.text))
    #             score.add_match_score(token.text,similariity_score, token.dep_)
    #     return scores

    # def get_possible_model_scores(self,vehicle_description):
    #     # scores=self.calculate_all_make_scores(input,md.makes)
    #     scores=self.calculate_all_model_scores(vehicle_description,md.models)
    #     input_make_score={}
    #     for score in scores:
    #         higher_scores=score.get_match_score_filtered(.75,[])
    #         for ms in higher_scores:
    #             # print(ms)
    #             input_make_score[ms.compare_str]=ms.similarity_score
        
    #     return input_make_score


if __name__=="__main__":
    print(method("VW Golf R with engine swap from Toyota 86 GT"))