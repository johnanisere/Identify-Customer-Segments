import numpy as np
import pandas as pd

# Creating decade_dict and decade_list to be used in make_decade function.
decade_dict = {1: [1, 2], 2: [3, 4], 3: [5, 6, 7], 4: [8, 9], 5: [10, 11, 12, 13], 6:[14, 15]}

decade_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        
# Investigate "PRAEGENDE_JUGENDJAHRE" and engineer two new variables.
def make_decade(x):
    if pd.isnull(x):
        return np.nan
    else:
        for key, array in decade_dict.items():
            if x in array:
                return key
            elif x not in decade_list:
                print(x,decade_list,'There is some error while mapping decade. Please check.')

    
def make_movement(x):
    if pd.isnull(x):
        return np.nan
    elif x in (2,4,6,7,9,11,13,15):
        return 0        
    elif x in (1,3,5,8,10,12,14):
        return 1
    else:
        print('make_movement-There is some error while mapping movement. Please check.')


# Investigate "CAMEO_INTL_2015" and engineer two new variables.
def make_wealth(x):
    if pd.isnull(x):
        return np.nan 
    elif int(x) // 10 == 1:
        return 1
    elif int(x) // 10 == 2:
        return 2
    elif int(x) // 10 == 3:
        return 3
    elif int(x) // 10 == 4:
        return 4
    elif int(x) // 10 == 5:
        return 5
    else:
        print('make_wealth-There is some error while mapping movement. Please check.')
    
def make_life_stage(x):
    if pd.isnull(x):
        return np.nan 
    elif int(x) % 10 == 1:
        return 1
    elif int(x) % 10 == 2:
        return 2
    elif int(x) % 10 == 3:
        return 3
    elif int(x) % 10 == 4:
        return 4
    elif int(x) % 10 == 5:
        return 5
    else:
        print('make_life_stage-There is some error while mapping movement. Please check.')