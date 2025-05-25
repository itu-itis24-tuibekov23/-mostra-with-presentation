import pandas as pd
import io
import numpy as np

# Load the data from the CSV file
file_path = 'code/cluster_profiles_numerical_median.csv'
try:
    df = pd.read_csv(file_path, index_col=0)
    df = df.T
    df.index = df.index.astype(int)
    df.index.name = 'cluster' # Set the index name to 'cluster'
    print(f"Successfully loaded and transposed data from {file_path}")
    print("First 5 rows of the loaded data:")
    print(df.head())
    print("-" * 30)

except FileNotFoundError:
    print(f"Error: The file {file_path} was not found.")
    exit()
except Exception as e:
    print(f"Error reading or processing the CSV file: {e}")
    exit()

# Define the weights for each feature (based on median values)
weights = {
    'total_pings': 2,
    'unique_days_active': 2,
    'activity_span_days': 1,
    'ratio_in_luxury_houses': 5,
    'ratio_in_hotels': 2,
    'ratio_in_turkey_sites': 5, # Ultra luxury accommodation
    'ratio_in_poi': 0.5,
    'ratio_in_p_schools': 0,    # Primary schools, neutral effect
    'ratio_gece_pings': 2,      # Renamed from ratio_gece_pings (script) to match CSV
    'ratio_aksam_pings': 2,     # Renamed from ratio_aksam_pings (script) to match CSV
    'ratio_sabah_pings': 1,     # Renamed from ratio_sabah_pings (script) to match CSV
    'ratio_ogle_pings': 1,      # Renamed from ratio_ogle_pings (script) to match CSV
    'num_distinct_polygon_types_visited': 1,
    'num_distinct_poi': 1,
    'dominant_gece_location_ping_count': 1,
    'ratio_dominant_gece_loc_pings_to_total_gece': 1
}

# Calculate the richness score for each cluster
df['PingRichnessScore'] = 0.0 # Initialize with float

print("\nCalculating Ping Richness Score using Median Values from CSV...")
for feature, weight in weights.items():
    if feature in df.columns:
        # Ensure the column is numeric before multiplication
        df[feature] = pd.to_numeric(df[feature], errors='coerce')
        df['PingRichnessScore'] += df[feature] * weight
    else:
        print(f"Warning: Feature '{feature}' from weights not found in DataFrame columns. Skipping.")
print("-" * 30)

# Print the DataFrame with the new RichnessScore
print("\nPing Data Cluster Characteristics with Richness Score (Median Values from CSV):")
# Ensure all keys in weights are actually columns in df before trying to display
display_cols_present = [col for col in weights.keys() if col in df.columns]
display_cols_present.append('PingRichnessScore')

print(df[display_cols_present].head(len(df)))

# Save the DataFrame to a CSV file
output_path = 'code/ping_richness_scores.csv'
try:
    df.to_csv(output_path)
    print(f"\nSuccessfully saved ping richness scores to {output_path}")
except Exception as e:
    print(f"\nError saving ping richness scores to CSV: {e}")
