import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
import re

def parse_sales_volume(value):
    if isinstance(value, str) and value and value[0].isalpha() and value[1:].isdigit():
        return int(value[1:])
    return np.nan

def parse_range_to_midpoint(value_str):
    if pd.isna(value_str) or value_str == '':
        return np.nan
    value_str = str(value_str).replace('.', '').replace(' TL', '').replace('+', '')
    if '-' in value_str:
        parts = value_str.split('-')
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            low, high = map(int, parts)
            return (low + high) / 2
    elif value_str.isdigit():
        return int(value_str)
    return np.nan

def parse_yatak_sayisi(value_str):
    if pd.isna(value_str) or value_str == '':
        return np.nan
    value_str = str(value_str).replace('.', '').replace('K', '000')
    if '-' in value_str:
        parts = value_str.split('-')
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            low, high = int(parts[0]), int(parts[1])
            return (low + high) / 2
    elif value_str.isdigit():
        return int(value_str)
    elif ' / ' in value_str: # Handles '5 / 5+'
         return 5
    elif value_str in ['Lüks Butik Otel', 'Butik Otel', 'Business', 'Diğer (Apart, Pansiyon)']:
        return np.nan
    return np.nan

def parse_mapin_segment(segment_str):
    if pd.isna(segment_str):
        return np.nan, np.nan, np.nan
    
    match = re.match(r'([A-Z]+)([0-5])(?:-([A-E]))?', str(segment_str))
    if match:
        type_val = match.group(1)
        pop_score_raw = int(match.group(2))
        pop_val_transformed = 6 - pop_score_raw

        luxury_val_raw = match.group(3)
        luxury_mapping = {'A': 5, 'B': 4, 'C': 3, 'D': 2, 'E': 1, np.nan: np.nan}
        luxury_val_numeric = luxury_mapping.get(luxury_val_raw, np.nan) 

        return type_val, pop_val_transformed, luxury_val_numeric
    return np.nan, np.nan, np.nan


def preprocess_data(input_filepath='filtered_data.csv', output_filepath='processed_filtered_data.csv'):
    try:
        df = pd.read_csv(input_filepath, delimiter=';', decimal=',')
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None

    df.replace('', np.nan, inplace=True)

    # 1. Numerical Conversions and Initial Cleaning
    sales_cols = ['SatisHacmi', 'DiageoSatisHacmi']
    for col in sales_cols:
        df[col + '_num'] = df[col].apply(parse_sales_volume)

    range_cols_map = {
        'OrtalamaHarcamaTutari': 'OrtalamaHarcamaTutari_num',
        'KuverSayisi': 'KuverSayisi_num',
        'YatakSayisi': 'YatakSayisi_num',
        'YillikMisafir': 'YillikMisafir_num'
    }
    for col, new_col in range_cols_map.items():
        if col == 'YatakSayisi':
            df[new_col] = df[col].apply(parse_yatak_sayisi)
        else:
            df[new_col] = df[col].apply(parse_range_to_midpoint)

    binary_map_cols = {
        'BiletEtkinlik': {'Etkinlik Yok': 0, 'Etkinlik Var': 1},
        'HerseyDahil': {'Hayır': 0, 'Evet': 1},
        'KisMevsimi': {'Hayır': 0, 'Evet': 1}
    }
    for col, mapping in binary_map_cols.items():
        df[col + '_encoded'] = df[col].map(mapping)

    numeric_direct_cols = ['lat', 'lng', 'MapProfileScore', 'MapPopulationScore']
    for col in numeric_direct_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    parsed_mapin_segment = df['Mapin Segment'].apply(lambda x: pd.Series(parse_mapin_segment(x)))
    df[['MapinSegment_Type', 'MapinSegment_Population_Num', 'MapinSegment_Luxury_Num']] = parsed_mapin_segment
    
    numerical_features = [col + '_num' for col in sales_cols] + \
                         list(range_cols_map.values()) + \
                         [col + '_encoded' for col in binary_map_cols.keys()] + \
                         numeric_direct_cols + \
                         ['MapinSegment_Population_Num', 'MapinSegment_Luxury_Num']
    
    numerical_features = [f for f in numerical_features if f in df.columns]

    categorical_features = ['SatisKanali', 'MusteriProfili', 'MusteriBolge4', 'OtelTipi', 'MapinSegment_Type']
    categorical_features = [f for f in categorical_features if f in df.columns]


    original_cols_to_drop = sales_cols + list(range_cols_map.keys()) + \
                              list(binary_map_cols.keys()) + ['Mapin Segment']
    
    original_cols_to_drop = [col for col in original_cols_to_drop if col in df.columns]
    
    processed_frames = [df.drop(columns=categorical_features + original_cols_to_drop, errors='ignore')]
    
    if categorical_features:
        encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False, drop='first') # drop='first' to avoid multicollinearity
        encoded_data = encoder.fit_transform(df[categorical_features])
        encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(categorical_features), index=df.index)
        processed_frames.append(encoded_df)

    df_processed = pd.concat(processed_frames, axis=1)
    
    current_numerical_cols_to_scale = [f for f in numerical_features if f in df_processed.columns]

    if current_numerical_cols_to_scale:
        scaler = MinMaxScaler()
        df_processed[current_numerical_cols_to_scale] = scaler.fit_transform(df_processed[current_numerical_cols_to_scale])

    try:
        df_processed.to_csv(output_filepath, index=False, sep=';', decimal=',')
        print(f"Processed data saved to {output_filepath}")
    except Exception as e:
        print(f"Error saving processed CSV: {e}")
    
    return df_processed

if __name__ == '__main__':
    processed_df = preprocess_data()
    if processed_df is not None:
        print(f"\nSample of processed data:")
        print(processed_df.head())
        print(f"\nInfo of processed data:")
        processed_df.info()
        print(f"\nColumns in processed data: {processed_df.columns.tolist()}")
