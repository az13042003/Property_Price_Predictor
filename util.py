import json
import pickle
import numpy as np
__location=None
__data_columns=None
__model=None

def get_estimated_price(location,total_sqft,bhk,bath):
    try:

        loc_index = __data_columns.index(location.lower())
    except:
        loc_index=-1
    x = np.zeros(len(__data_columns))
    x[0] = total_sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1
    return round(__model.predict([x])[0],2)

def get_location_names():
    return __location

def load_saved_artifacts():
    print('Loading saved artifacts..... start')
    global __data_columns
    global __location
    with open("./artifact/colummns.json",'r') as f:

        __data_columns=json.load(f)['data columns']
        __location=__data_columns[3:]
    global __model
    with open('./artifact/banglore_prpty_price_predct','rb') as f:
        __model=pickle.load(f)
        print("Loading asved arifacts... done")
if __name__ =='__main__':
    load_saved_artifacts()
    print(get_location_names())
