import numpy as np
import pandas as pd
from encoder_helpers import make_decade,make_movement,make_wealth,make_life_stage

# Converting (list of string) values to (list of integers and string) in nan_vals column.
def text_to_int(value):
    try:
        int(value)
        return True
    except ValueError:    
        return False
    
def get_missing_columns():
    data_types = pd.read_csv('data_types.csv')
    data_types.set_index('attribute', inplace=True)
    data_types['nan_vals'] = data_types['missing_or_unknown'].str.replace('[','').str.replace(']','').str.split(',').values
    data_types['nan_vals'] = data_types.apply(lambda x: [int(i) if text_to_int(i) else i for i in x['nan_vals']], axis=1)
    return data_types

def strat_rand_sampling(df, frac):
    '''
    :params
        df(DataFrame)- from which sample has to be dervied\
        frac(float)- proportion of number of observations in df to be dervied in sample
        
    :return(dataframe)- dataframe sampled from df
        
    '''
    sample_df = df.sample(frac=frac, random_state=42) 
    return sample_df

def find_missing_data(df):
    '''
    INPUT:
        df - (dataframe), dataframe to check for missing values in its columns
    OUTPUT:
        df_null: (dataframe), with count & percentage of missing values in input dataframe columns
    '''
    null_data = df.isnull().sum()[df.isnull().sum() > 0]
    
    data_dict = {'count': null_data.values, 'pct': np.round(null_data.values *100/df.shape[0],2)}
    
    df_null = pd.DataFrame(data=data_dict, index=null_data.index)
    df_null.sort_values(by='count', ascending=False, inplace=True)
    return df_null


def clean_data(df):
    
    """
    Perform feature trimming, re-encoding, and engineering for demographics
    data
    :params
        df(DataFrame)- Demographics DataFrame
    
    :returns(DataFrame)- Trimmed and cleaned demographics DataFrame
    """
    data_types = get_missing_columns()
    
    for idx in data_types.index:
        column = idx
        if column in df.columns:
            df[column] = df[column].replace(data_types.loc[column]['nan_vals'], np.nan)

      
    # remove selected columns
    df.drop(['AGER_TYP', 'ALTER_HH', 'ALTER_KIND1', 'ALTER_KIND2', 'ALTER_KIND3', 'ALTER_KIND4', 'ALTERSKATEGORIE_FEIN',\
             'D19_BANKEN_ONLINE_QUOTE_12', 'D19_GESAMT_ONLINE_QUOTE_12', 'D19_KONSUMTYP', 'D19_LETZTER_KAUF_BRANCHE',\
             'D19_LOTTO', 'D19_SOZIALES', 'D19_TELKO_ONLINE_QUOTE_12', 'D19_VERSAND_ONLINE_QUOTE_12',\
             'D19_VERSI_ONLINE_QUOTE_12', 'EXTSEL992','GEBURTSJAHR', 'KBA05_BAUMAX', 'KK_KUNDENTYP', 'TITEL_KZ', 'LNR'],
            axis=1, inplace=True)
    
    print("Removal of Columns with over 20% null values complete...")
    
    # remove selected rows
    df = df[df.isnull().sum(axis=1) < 9].reset_index(drop=True)
    
    # remove selected columns again
    features_not_in_feat_info_42 = ['AKT_DAT_KL', 'ANZ_KINDER', 'ANZ_STATISTISCHE_HAUSHALTE', 'CJT_KATALOGNUTZER','CJT_TYP_1',\
                                    'CJT_TYP_2', 'CJT_TYP_3', 'CJT_TYP_4', 'CJT_TYP_5', 'CJT_TYP_6', 'DSL_FLAG',\
                                    'EINGEZOGENAM_HH_JAHR','FIRMENDICHTE', 'GEMEINDETYP', 'HH_DELTA_FLAG', 'KBA13_ANTG1',\
                                    'KBA13_ANTG2', 'KBA13_ANTG3','KBA13_ANTG4', 'KBA13_BAUMAX', 'KBA13_CCM_1401_2500',\
                                    'KBA13_GBZ', 'KBA13_HHZ', 'KBA13_KMH_210','KONSUMZELLE', 'MOBI_RASTER', 'RT_KEIN_ANREIZ',\
                                    'RT_SCHNAEPPCHEN', 'RT_UEBERGROESSE', 'STRUKTURTYP','UMFELD_ALT', 'UMFELD_JUNG',\
                                    'UNGLEICHENN_FLAG', 'VERDICHTUNGSRAUM', 'VHA', 'VHN', 'VK_DHT4A','VK_DISTANZ',\
                                    'VK_ZG11','D19_KONSUMTYP_MAX', 'KOMBIALTER','EINGEFUEGT_AM']
    
    df.drop(features_not_in_feat_info_42,axis=1, inplace=True)
    
    print("Removal of undocumented columns complete...")
    
    
    # select, re-encode, and engineer column values.
    # # feature engineering of categorical features

    df['OST_WEST_KZ'].replace(['W','O'], [1, 0], inplace=True)
    
    multi = ['CAMEO_DEU_2015', 'CAMEO_DEUG_2015', 'CJT_GESAMTTYP', 'D19_BANKEN_ANZ_12', 'D19_BANKEN_ANZ_24',\
             'D19_BANKEN_DATUM','D19_BANKEN_OFFLINE_DATUM', 'D19_BANKEN_ONLINE_DATUM', 'D19_GESAMT_ANZ_12',\
             'D19_GESAMT_ANZ_24', 'D19_GESAMT_DATUM','D19_GESAMT_OFFLINE_DATUM', 'D19_GESAMT_ONLINE_DATUM',\
             'D19_TELKO_DATUM', 'D19_TELKO_OFFLINE_DATUM', 'D19_TELKO_ONLINE_DATUM','D19_VERSAND_DATUM',\
             'D19_VERSAND_OFFLINE_DATUM', 'D19_VERSAND_ONLINE_DATUM', 'D19_VERSI_DATUM', 'D19_VERSI_OFFLINE_DATUM',\
             'D19_VERSI_ONLINE_DATUM', 'FINANZTYP', 'GEBAEUDETYP', 'GFK_URLAUBERTYP','LP_FAMILIE_FEIN','LP_FAMILIE_GROB',\
             'LP_STATUS_FEIN', 'LP_STATUS_GROB', 'NATIONALITAET_KZ', 'SHOPPER_TYP', 'ZABEOTYP']
        
    df = pd.get_dummies(df, columns=multi, prefix=multi)
    
    
     # feature engineering of mixed features
    df['PRAEGENDE_JUGENDJAHRE_decade'] = df['PRAEGENDE_JUGENDJAHRE'].apply(make_decade)
    df['PRAEGENDE_JUGENDJAHRE_movement'] = df['PRAEGENDE_JUGENDJAHRE'].apply(make_movement)
    df.drop('PRAEGENDE_JUGENDJAHRE', axis=1, inplace=True)
    
    print("Feature Engineering PRAEGENDE_JUGENDJAHRE complete...")
    
    
    df['CAMEO_INTL_2015_wealth'] = df['CAMEO_INTL_2015'].apply(make_wealth) 
    df['CAMEO_INTL_2015_life_stage'] = df['CAMEO_INTL_2015'].apply(make_life_stage)
    df.drop('CAMEO_INTL_2015', axis=1, inplace=True)
    
    print("Feature Engineering CAMEO_INTL_2015 complete...")
    
    df['WOHNLAGE_rural'] = df['WOHNLAGE'].map({0:0,1:0,2:0,3:0,4:0,5:0,7:1,8:1})
    df['WOHNLAGE_rating_class'] = df['WOHNLAGE'].map({0:0,1:1,2:2,3:3,4:4,5:5,7:0,8:0})
    
    print("Feature Engineering WOHNLAGE complete...")
    
    df = df.drop(['LP_LEBENSPHASE_FEIN','LP_LEBENSPHASE_GROB','WOHNLAGE','PLZ8_BAUMAX'], axis=1)
    
    print("Finished!")
    
    # Return the cleaned dataframe.
    return df
