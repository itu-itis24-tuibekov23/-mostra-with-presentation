import pandas as pd
import io
import numpy as np

# New cluster characteristics data provided by the user
data_string = """cluster,num_unique_cafes_visited,avg_visits_per_week,TimeSlot_Afternoon_rate,TimeSlot_Evening_rate,TimeSlot_Morning_rate,TimeSlot_Night_rate,DayOfWeek_Friday_rate,DayOfWeek_Monday_rate,DayOfWeek_Saturday_rate,DayOfWeek_Sunday_rate,DayOfWeek_Thursday_rate,DayOfWeek_Tuesday_rate,DayOfWeek_Wednesday_rate,avg_visit_duration_minutes,total_time_spent_hours
0,1.863670,9.522846,0.431337,0.074554,0.481527,0.012583,0.026297,0.033559,0.014607,0.006964,0.029617,0.868105,0.020851,1.189899,0.054112
1,1.762386,10.515043,0.466602,0.094343,0.426750,0.012306,0.020508,0.006748,0.005360,0.003367,0.942278,0.006623,0.015116,1.214090,0.057964
2,1.814654,10.401403,0.436020,0.063205,0.488828,0.011946,0.934363,0.008400,0.011147,0.004400,0.027029,0.007242,0.007419,0.783230,0.039246
3,6.379594,7.838877,0.377289,0.118829,0.411364,0.092518,0.184881,0.144854,0.120670,0.101271,0.183006,0.135321,0.129998,2.540515,1.064228
4,1.891847,10.232391,0.489341,0.115454,0.381706,0.013499,0.022430,0.023908,0.033117,0.865834,0.021201,0.015379,0.018131,1.626054,0.074163
5,1.835467,10.309680,0.461656,0.112435,0.413619,0.012289,0.022243,0.011875,0.913817,0.009947,0.026714,0.007980,0.007424,1.095794,0.053774
6,1.817197,9.318538,0.393898,0.067472,0.525998,0.012632,0.028189,0.017951,0.012385,0.006135,0.037168,0.013288,0.884883,1.093464,0.047170
7,10.500000,77.677356,0.213760,0.237899,0.251783,0.296558,0.130075,0.146091,0.147268,0.168377,0.143962,0.139950,0.124277,19.203231,90.586778
8,1.742545,8.451405,0.063378,0.036040,0.065262,0.835321,0.173178,0.176719,0.076191,0.066468,0.160983,0.136301,0.210160,1.693918,0.127524
9,1.870493,9.625080,0.437527,0.070889,0.479388,0.012196,0.029079,0.895795,0.011133,0.009328,0.030357,0.012033,0.012276,1.140250,0.051116
"""

# Read the data into a pandas DataFrame
df = pd.read_csv(io.StringIO(data_string))
df = df.set_index('cluster')

# Columns to apply log transformation
cols_to_transform = [
    'num_unique_cafes_visited',
    'avg_visits_per_week',
    'avg_visit_duration_minutes',
    'total_time_spent_hours'
]

print("Applying log1p transformation to specified columns...")
for col in cols_to_transform:
    if col in df.columns:
        # df[col + '_original'] = df[col] # Optionally keep original values
        df[col] = np.log1p(df[col])
        print(f"Transformed '{col}'. First 5 values:\n{df[col].head()}")
    else:
        print(f"Warning: Column '{col}' not found for log transformation.")
print("-" * 30)

# Define the weights for each feature
weights = {
    'num_unique_cafes_visited': 3,
    'avg_visits_per_week': 4,
    'TimeSlot_Afternoon_rate': 2,
    'TimeSlot_Evening_rate': 3,
    'TimeSlot_Morning_rate': 1,
    'TimeSlot_Night_rate': 3,
    'DayOfWeek_Friday_rate': 2,
    'DayOfWeek_Monday_rate': 1,
    'DayOfWeek_Saturday_rate': 3,
    'DayOfWeek_Sunday_rate': 3,
    'DayOfWeek_Thursday_rate': 1,
    'DayOfWeek_Tuesday_rate': 1,
    'DayOfWeek_Wednesday_rate': 1,
    'avg_visit_duration_minutes': 3,
    'total_time_spent_hours': 4
}

# Calculate the richness score for each cluster
df['CafeRichnessScore'] = 0

for feature, weight in weights.items():
    if feature in df.columns:
        df['CafeRichnessScore'] += df[feature] * weight
    else:
        print(f"Warning: Feature '{feature}' from weights not found in DataFrame columns.")

# Print the DataFrame with the new RichnessScore
print("\nCafe Cluster Characteristics with Richness Score:")
# Display relevant columns
display_cols = list(weights.keys()) + ['CafeRichnessScore']
# To see original values of transformed columns, you would add them to display_cols
# e.g., if you kept 'num_unique_cafes_visited_original'
print(df[display_cols].head(len(df)))

# Save the DataFrame to a CSV file
output_path = 'code/cafe_richness_scores.csv'
try:
    df.to_csv(output_path)
    print(f"\nSuccessfully saved cafe richness scores to {output_path}")
except Exception as e:
    print(f"\nError saving cafe richness scores to CSV: {e}")
