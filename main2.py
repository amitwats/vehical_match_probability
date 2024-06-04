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



if __name__=="__main__":
    print(method("VW Golf R with engine swap from Toyota 86 GT"))