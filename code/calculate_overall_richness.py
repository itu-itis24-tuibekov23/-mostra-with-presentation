import pandas as pd

def load_and_prepare_data():
    """Loads all necessary CSV files and prepares them for merging."""
    try:
        # Load richness score files
        cafe_scores = pd.read_csv('data/cafe_richness_scores.csv').rename(
            columns={'cluster': 'cafe_cluster', 'CafeRichnessScore': 'cafe_richness_score'}
        )[['cafe_cluster', 'cafe_richness_score']]
        
        ping_scores = pd.read_csv('data/ping_richness_scores.csv').rename(
            columns={'cluster': 'ping_cluster', 'PingRichnessScore': 'ping_richness_score'}
        )[['ping_cluster', 'ping_richness_score']]
        
        restaurant_scores = pd.read_csv('data/restaurant_richness_scores.csv').rename(
            columns={'cluster': 'restaurant_cluster', 'RichnessScore': 'restaurant_richness_score'}
        )[['restaurant_cluster', 'restaurant_richness_score']]

        # Load device cluster assignment files
        coffee_device_clusters = pd.read_csv('data/coffee_device_clusters.csv', sep=';')
        # Keep only device_aid and cluster, rename cluster
        coffee_device_clusters = coffee_device_clusters[['device_aid', 'cluster']].rename(
            columns={'cluster': 'cafe_cluster'}
        )

        polygons_device_clusters = pd.read_csv('data/polygons_clusters.csv', sep=',')
        # Assuming the first column is the device_aid and is unnamed
        if polygons_device_clusters.columns[0].startswith('Unnamed:'):
            polygons_device_clusters = polygons_device_clusters.rename(columns={polygons_device_clusters.columns[0]: 'device_aid'})
        else:
            # If it's already named (e.g. if index_col=0 was used during creation and then reset_index)
            # Or if it's the first named column that acts as device_id
            # This part might need adjustment if the first column isn't implicitly the device_id
            # For now, let's assume it's the first column.
            # If the file truly uses the CSV index as device_id, it's better to load with index_col=0
            # For simplicity in this script, we'll assume it's a column named or becomes 'device_aid'
            # This might be a point of failure if the assumption is wrong.
            # A safer way for polygons_clusters if device_id is index:
            # polygons_device_clusters = pd.read_csv('clusteredcsvs/polygons_clusters.csv', sep=',', index_col=0)
            # polygons_device_clusters.index.name = 'device_aid'
            # polygons_device_clusters = polygons_device_clusters.reset_index()
            # For now, using the provided structure:
            polygons_device_clusters = polygons_device_clusters.rename(columns={polygons_device_clusters.columns[0]: 'device_aid'})


        polygons_device_clusters = polygons_device_clusters[['device_aid', 'cluster']].rename(
            columns={'cluster': 'ping_cluster'}
        )
        # Ensure device_aid is of the same type for merging, typically string
        polygons_device_clusters['device_aid'] = polygons_device_clusters['device_aid'].astype(str)


        restaurant_device_clusters = pd.read_csv('data/restaurant_clusters.csv', sep=';')
        restaurant_device_clusters = restaurant_device_clusters[['device_aid', 'cluster']].rename(
            columns={'cluster': 'restaurant_cluster'}
        )
        
        # Ensure device_aid is string type for all for consistent merging
        coffee_device_clusters['device_aid'] = coffee_device_clusters['device_aid'].astype(str)
        restaurant_device_clusters['device_aid'] = restaurant_device_clusters['device_aid'].astype(str)

        print("Data loaded and prepared successfully.")
        return cafe_scores, ping_scores, restaurant_scores, coffee_device_clusters, polygons_device_clusters, restaurant_device_clusters

    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        return None
    except Exception as e:
        print(f"An error occurred during data loading: {e}")
        return None

def merge_data(coffee_devices, polygons_devices, restaurant_devices):
    """Merges the device cluster dataframes."""
    try:
        # Merge dataframes on 'device_aid'
        # Start with coffee, then merge polygons, then restaurants
        # Using inner merge to find common device_aids across all three datasets
        merged_df = pd.merge(coffee_devices, polygons_devices, on='device_aid', how='inner')
        merged_df = pd.merge(merged_df, restaurant_devices, on='device_aid', how='inner')
        
        print(f"Merged device data. Found {len(merged_df)} common device_aids.")
        if len(merged_df) == 0:
            print("Warning: No common device_aids found across the three datasets. Output will be empty.")
        return merged_df
    except Exception as e:
        print(f"An error occurred during data merging: {e}")
        return None

def map_scores(merged_df, cafe_scores, ping_scores, restaurant_scores):
    """Maps cluster labels to richness scores."""
    try:
        merged_df = pd.merge(merged_df, cafe_scores, on='cafe_cluster', how='left')
        merged_df = pd.merge(merged_df, ping_scores, on='ping_cluster', how='left')
        merged_df = pd.merge(merged_df, restaurant_scores, on='restaurant_cluster', how='left')
        
        # Check for NaNs after merge, which indicates missing scores for some clusters
        cols_to_check = ['cafe_richness_score', 'ping_richness_score', 'restaurant_richness_score']
        for col in cols_to_check:
            if merged_df[col].isnull().any():
                print(f"Warning: Column '{col}' contains NaN values after merging scores. "
                      "This might be due to cluster labels in device files not present in score files.")
        
        print("Scores mapped successfully.")
        return merged_df
    except Exception as e:
        print(f"An error occurred during score mapping: {e}")
        return None

def calculate_overall_score(df_with_scores):
    """Calculates the overall richness score using weighted average."""
    try:
        weights = {
            'cafe_richness_score': 2,
            'ping_richness_score': 1,
            'restaurant_richness_score': 3
        }
        
        total_weight = sum(weights.values())
        
        # Ensure scores are numeric, fill NaNs with 0 for calculation if any (though ideally handled earlier)
        df_with_scores['OverallRichnessScore'] = (
            (df_with_scores['cafe_richness_score'].fillna(0) * weights['cafe_richness_score']) +
            (df_with_scores['ping_richness_score'].fillna(0) * weights['ping_richness_score']) +
            (df_with_scores['restaurant_richness_score'].fillna(0) * weights['restaurant_richness_score'])
        ) / total_weight
        
        print("Overall richness score calculated.")
        return df_with_scores
    except Exception as e:
        print(f"An error occurred during overall score calculation: {e}")
        return None

def main():
    loaded_data = load_and_prepare_data()
    if loaded_data is None:
        return

    cafe_scores, ping_scores, restaurant_scores, coffee_devices, polygons_devices, restaurant_devices = loaded_data
    
    merged_devices = merge_data(coffee_devices, polygons_devices, restaurant_devices)
    if merged_devices is None or merged_devices.empty:
        print("Halting execution due to issues in merging device data or no common devices found.")
        return
        
    df_with_scores = map_scores(merged_devices, cafe_scores, ping_scores, restaurant_scores)
    if df_with_scores is None:
        print("Halting execution due to issues in mapping scores.")
        return
        
    final_df = calculate_overall_score(df_with_scores)
    if final_df is None:
        print("Halting execution due to issues in calculating final score.")
        return

    output_path = 'data/overall_device_richness_scores.csv'
    try:
        final_df.to_csv(output_path, index=False)
        print(f"Successfully saved overall device richness scores to {output_path}")
        print("\nFinal DataFrame sample:")
        print(final_df.head())
    except Exception as e:
        print(f"Error saving final results to CSV: {e}")

if __name__ == '__main__':
    main()
