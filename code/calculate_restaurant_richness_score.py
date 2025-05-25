import pandas as pd
import io
import numpy as np # Import numpy for log transformation

# Cluster characteristics data provided by the user
data_string = """cluster,avg_SatisHacmi,avg_OrtalamaHarcamaTutari,avg_PopulationInverseScore,avg_QualityScore,total_visits,VenueType_D_rate,VenueType_H_rate,VenueType_R_rate,TimeSlot_Afternoon_rate,TimeSlot_Evening_rate,TimeSlot_Morning_rate,TimeSlot_Night_rate
0,0.917531,1.067311,2.212629,0.754090,3.592412,0.083840,0.115721,0.800439,0.040310,0.023842,0.905886,0.029962
1,0.440084,1.064155,2.442076,1.099881,4.957923,0.891258,0.011116,0.097627,0.059413,0.020937,0.890218,0.029431
2,0.517944,1.131224,2.462004,1.058422,5.143595,0.886523,0.010656,0.102820,0.895165,0.024765,0.056413,0.023657
3,0.932332,1.061462,2.116274,0.854113,3.701558,0.094038,0.077511,0.828451,0.878927,0.031341,0.058825,0.030907
4,0.720858,1.088097,2.399856,0.916308,5.639502,0.510663,0.045852,0.443485,0.049164,0.884865,0.037502,0.028468
5,0.750049,1.193147,2.688764,0.759222,152.231707,0.669254,0.012568,0.318178,0.303056,0.256243,0.239183,0.201517
6,0.775008,1.087794,2.326682,0.887586,4.811664,0.414806,0.059735,0.525459,0.040499,0.035589,0.044133,0.879779
"""

# Read the data into a pandas DataFrame
df = pd.read_csv(io.StringIO(data_string))
df = df.set_index('cluster')

if 'total_visits' in df.columns:
    df['total_visits_original'] = df['total_visits'] 
    df['total_visits'] = np.log1p(df['total_visits'])
    print("Applied log1p transformation to 'total_visits'. First 5 transformed values:")
    print(df['total_visits'].head())
    print("-" * 30)
else:
    print("Warning: 'total_visits' column not found for log transformation.")


weights = {
    'avg_SatisHacmi': 4,
    'avg_OrtalamaHarcamaTutari': 5,
    'avg_PopulationInverseScore': -3,  # Higher score indicates lower wealth
    'avg_QualityScore': 4,
    'total_visits': 3, # Weight remains the same, but applied to transformed values
    'VenueType_D_rate': 1,  # Lower tier venues
    'VenueType_H_rate': 3,  # Hotels
    'VenueType_R_rate': 5,  # Higher tier/bistro
    'TimeSlot_Afternoon_rate': 1,
    'TimeSlot_Evening_rate': 2,
    'TimeSlot_Morning_rate': 1,
    'TimeSlot_Night_rate': 2
}

df['RichnessScore'] = 0

for feature, weight in weights.items():
    if feature in df.columns:
        df['RichnessScore'] += df[feature] * weight
    else:
        print(f"Warning: Feature '{feature}' from weights not found in DataFrame columns.")

# Print the DataFrame with the new RichnessScore
print("\nCluster Characteristics with Richness Score (after log_transform on total_visits):")
# Display relevant columns including original and transformed total_visits if needed
display_cols = list(weights.keys()) + ['RichnessScore']
if 'total_visits_original' in df.columns:
    display_cols.insert(display_cols.index('total_visits')+1, 'total_visits_original')
print(df[display_cols].head(len(df)))

# Save the DataFrame to a CSV file
output_path = 'code/restaurant_richness_scores.csv'
try:
    df.to_csv(output_path)
    print(f"\nSuccessfully saved restaurant richness scores to {output_path}")
except Exception as e:
    print(f"\nError saving restaurant richness scores to CSV: {e}")
