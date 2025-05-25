# Project Description

## 👥 Team Members

- Sanzhar Tuibekov
- Seyit Mustafa Demir
- Kerem Adin
- Buğra Şahin

This project analyzes mobility data to classify user behavior and assign a “richness score” based on activity around coffee shops, restaurants, and urban polygons. Users are clustered and visualized using interactive tools for insight into urban dynamics.

## Data Processing and Analysis Steps:

1.  **Data Integration:**

    - Scripts such as `mobil_coffee.ipynb`, `mobil_polygons.ipynb`, and `mobil_restaurant.ipynb` were utilized to merge and consolidate data from `mobil_coffee`, `mobil_polygons`, and `mobil_restaurant` datasets.

2.  **Feature Enhancement:**

    - The `feature_enhancement.ipynb` notebook was employed to enrich the existing datasets with additional relevant features, improving the quality and depth of the data for analysis.

3.  **Score Calculation per Cluster:**

    - Scripts like `calculate_cafe_richness_score.py`, `calculate_ping_richness_score.py`, and `calculate_restaurant_richness_score.py` were used to compute cafe, ping, and restaurant scores for each identified cluster. This step helps in understanding the characteristics and significance of different clusters.

4.  **Data Visualization:**
    - The `view_richness_app.py` script provides an application to visualize the calculated richness scores. This allows for an interactive exploration of the data and the identified patterns.

## Running the Visualization App

### Requirements

Before running the app, ensure you have the necessary Python libraries installed. You can typically install them using pip:

```bash
pip install streamlit pandas
```

### Execution

To run the visualization app, execute the following command from the project's root directory in your terminal:

```bash
streamlit run code/view_richness_app.py
```

This will start the application, and you can typically access it via a local URL provided in the terminal output (e.g., http://localhost:8501/).
