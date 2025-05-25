import streamlit as st
import pandas as pd
import os

# Set page config for wider layout
st.set_page_config(layout="wide")

st.title("Device Richness Score Viewer")

# --- Data Loading ---
@st.cache_data # Cache the data loading to improve performance
def load_data():
    file_path = 'data/overall_device_richness_scores.csv'
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            st.error(f"Error loading CSV file: {e}")
            return pd.DataFrame() # Return empty DataFrame on error
    else:
        st.error(f"Error: The file {file_path} was not found. Please ensure it exists.")
        st.info("You might need to run the `calculate_overall_richness.py` script first to generate this file.")
        return pd.DataFrame()

data_df = load_data()

if not data_df.empty:
    st.header("Overall Device Richness Scores Data")
    
    # --- Display Raw Data ---
    st.subheader("Raw Data Table")
    st.write(f"Displaying top 1000 rows out of {len(data_df)} total rows.")
    st.dataframe(data_df.head(1000), height=400) # Display a portion for performance

    # --- Summary Statistics ---
    st.subheader("Summary Statistics for 'OverallRichnessScore'")
    if 'OverallRichnessScore' in data_df.columns:
        st.write(data_df['OverallRichnessScore'].describe())
    else:
        st.warning("'OverallRichnessScore' column not found.")

    # --- Histogram ---
    st.subheader("Distribution of 'OverallRichnessScore'")
    if 'OverallRichnessScore' in data_df.columns:
        # Ensure the column is numeric and drop NaNs for plotting
        scores_for_hist = pd.to_numeric(data_df['OverallRichnessScore'], errors='coerce').dropna()
        if not scores_for_hist.empty:
            st.bar_chart(scores_for_hist.value_counts().sort_index()) # Using bar_chart for discrete-like scores or hist
            
            # For a more traditional histogram, you might use matplotlib or plotly
            # Example with st.pyplot and matplotlib:
            # import matplotlib.pyplot as plt
            # fig, ax = plt.subplots()
            # ax.hist(scores_for_hist, bins=50)
            # ax.set_xlabel('OverallRichnessScore')
            # ax.set_ylabel('Frequency')
            # st.pyplot(fig)
        else:
            st.warning("No valid numeric data in 'OverallRichnessScore' to plot histogram.")
            
    else:
        st.warning("'OverallRichnessScore' column not found for histogram.")
        
    # --- Filtering (Optional Example) ---
    st.sidebar.header("Filtering Options")
    if 'OverallRichnessScore' in data_df.columns:
        min_score_val = float(data_df['OverallRichnessScore'].min())
        max_score_val = float(data_df['OverallRichnessScore'].max())
        
        score_range = st.sidebar.slider(
            "Filter by OverallRichnessScore:",
            min_value=min_score_val,
            max_value=max_score_val,
            value=(min_score_val, max_score_val)
        )
        
        filtered_df = data_df[
            (data_df['OverallRichnessScore'] >= score_range[0]) &
            (data_df['OverallRichnessScore'] <= score_range[1])
        ]
        st.subheader(f"Filtered Data (Score between {score_range[0]:.2f} and {score_range[1]:.2f})")
        st.write(f"Displaying top 1000 rows out of {len(filtered_df)} filtered rows.")
        st.dataframe(filtered_df.head(1000), height=300)
else:
    st.warning("Data could not be loaded. Please check the file path and ensure the CSV exists.")

st.info("This is a simple Streamlit app to view the richness scores.")

# --- Persona Descriptions ---
# User should fill these in with actual descriptions
cafe_persona_descriptions = {
    0: "Cafe Persona - Cluster 0: Gün tercihi belirgin değil, zaman dilimi tercihi dengeli. Düşük bağlılık gösteren kullanıcılar, kafe ziyaretleri seyrek ve rastgele.",
    1: "Cafe Persona - Cluster 1: Gün tercihi Perşembe günü baskın. Zaman dilimi tercihi öğleden sonra baskın. Düşük genel bağlılık, tek bir güne odaklanma.",
    2: "Cafe Persona - Cluster 2: Gün tercihi Cuma günü baskın. Zaman dilimi tercihi sabah saatleri baskın. Kısa süreli ziyaretler, diğer tek gün odaklı kümelerden farklı.",
    3: "Cafe Persona - Cluster 3: Orta düzey bağlılık. Ziyaret edilen kafe sayısı ve toplam süre ortalamanın üzerinde. Hafta içi ve günün farklı zamanlarına eşit yayılmış ziyaretler. Fırsat odaklı bir segment.",
    4: "Cafe Persona - Cluster 4: Gün tercihi Pazar günü baskın. Zaman dilimi tercihi öğleden sonra baskın. Hafta sonu odaklı, özellikle Pazar günü kafe keyfi yapan kullanıcılar.",
    5: "Cafe Persona - Cluster 5: Gün tercihi Cumartesi günü baskın. Zaman dilimi tercihi öğleden sonra baskın. Hafta sonu başlangıcını kafede değerlendiren kullanıcılar.",
    6: "Cafe Persona - Cluster 6: Gün tercihi Çarşamba günü baskın. Zaman dilimi tercihi sabah saatleri baskın. Hafta ortasında kafe ziyaretini rutine dönüştüren kullanıcılar.",
    7: "Cafe Persona - Cluster 7: Aşırı yüksek bağlılık. Ziyaret edilen kafe sayısı, ziyaret sıklığı, toplam süre ve her ziyaret süresi çok yüksek. Gün ve zaman dilimi tercihleri dengeli, premium müşteriler.",
    8: "Cafe Persona - Cluster 8: Zaman dilimi tercihi gece saatleri baskın. Niş segment, genel bağlılık güçlü kullanıcılar kadar yüksek değil. Gece açık kafeler için kritik hedef kitle."
}
ping_persona_descriptions = {
    0: "Ping Persona - Cluster 0: [Bu persona, kısa süreli aktivite aralıklarına sahip, ancak bu süre zarfında çoğunlukla ilgi çekici noktalarda (POI'lerde) bulunan bir kullanıcıdır. Özellikle geceleri bu POI'lerde belirgin bir şekilde yoğunlaşır ve genellikle tek bir baskın gece konumuna sahiptir. Sabahları da POI'lerde aktif olma eğilimindedir. Otel ve lüks ev gibi konaklama/yerleşim merkezlerinde aktivitesi neredeyse hiç yoktur, bu da onların daha çok dış mekanlarda veya belirli ilgi alanlarına yönelik yerlerde bulunduğunu düşündürür.]",
    1: "Ping Persona - Cluster 1: [Bu persona, uzun süreler boyunca çok yüksek genel aktivite gösteren bir kullanıcıdır. Gündüz ve akşam saatlerinde yoğun ping aktivitesine sahiptir. Pinglerinin büyük çoğunluğunu POI'ler dışında atar ve belirli bir gece baskın konumları yoktur. Bu durum, onların sürekli hareket halinde olan, farklı yerleri ziyaret eden, ancak bu ziyaretlerin mutlaka tanımlanmış ilgi çekici noktalar kategorisine girmeyen, şehir içinde aktif bir yaşam süren kişiler olduğunu düşündürür.]",
    2: "Ping Persona - Cluster 2: [Bu persona, çok düşük genel aktivite gösteren, kısa sürelerle aktif olan ve genellikle POI'lerde bulunmayan bir kullanıcıdır. Büyük olasılıkla cihazlarını nadiren kullanan veya belirli, sınırlı bir coğrafi alanda kalan, çevresinde pek hareket etmeyen kişilerdir. Gece aktivite paternleri veya belirli bir baskın gece konumları belirgin değildir. Bu durum, günlük yaşamlarının büyük bir kısmını ev veya iş gibi sabit bir konumda geçirdiklerini düşündürür.']"
}

restaurant_persona_descriptions = {
    0: "Restaurant Persona - Cluster 0: [Bu persona, sabah saatlerinde aktif olan, genellikle kalabalık bölgelerde yer alan, yüksek cirolu geleneksel kebap mekanlarını ve dikkate değer oranda hostelleri ziyaret eden bir kullanıcı profilidir. Kendi harcamaları ortalama olup, ziyaret ettikleri yerlerin kalite skoru öncelikli tercih sebepleri arasında görünmemektedir. Düşük ziyaret sayıları, belirli rutinlere sahip olduklarını düşündürebilir.]",
    1: "Restaurant Persona - Cluster 1: [Bu persona, sabah saatlerinde aktif olan, yüksek kaliteli Modern Pub & Bistro mekanlarını tercih eden bir kullanıcıdır. Bu mekanlar genellikle daha düşük satış hacmine sahip olup, nispeten sakin bölgelerde yer alır. Kalite ve modernlik, bu kullanıcıların temel tercih kriterleridir.]",
    2: "Restaurant Persona - Cluster 2: [Bu persona, özellikle öğleden sonraları aktif olan, yüksek kaliteli Modern Pub & Bistromekanlarını tercih eden bir profildir. Bu mekanlar genellikle nispeten sakin bölgelerde bulunur. Kullanıcılar bu deneyimler için ortalamanın üzerinde harcama yapmaya isteklidirler]",
    3: "Restaurant Persona - Cluster 3: [Bu persona, öğleden sonraları aktif olan ve özellikle çok kalabalık merkezi bölgelerde yer alan, yüksek cirolu geleneksel kebap mekanlarını ziyaret eden bir kullanıcıyı temsil eder. Ziyaret sayıları düşük olsa da, belirli ve yoğun lokasyonlara odaklanmışlardır.]",
    4: "Restaurant Persona - Cluster 4: [Bu persona, akşam saatlerinde sosyalleşen, hem modern (özellikle Pub & Bistro) hem de geleneksel mekanları dengeli bir şekilde tercih eden bir kullanıcıdır. Kaliteli ve orta yoğunluktaki bölgelerde vakit geçirmeyi severler ve bu deneyimler için iyi harcama yaparlar.]",
    5: "Restaurant Persona - Cluster 5: [ Bu persona, son derece aktif, günün her saatinde farklı mekanlarda bulunabilen ve en yüksek harcamayı yapan kullanıcı tipidir. Özellikle sakin, niş ve az keşfedilmiş lokasyonlardaki modern mekanları (özellikle Fine Dining ve Modern Pub & Bistro) tercih ederler. Ziyaret ettikleri mekanların kalite skoru birincil öncelikleri olmasa da, yüksek aktivite hacimleri, harcamaları ve keşifçi ruhları ile öne çıkarlar.]",
    6: "Restaurant Persona - Cluster 6: [Bu persona, gece saatlerinde aktif olan, kaliteli ve orta yoğunluktaki bölgelerde vakit geçiren bir profildir. Ağırlıklı olarak Modern Pub & Bistro ve geleneksel mekanları tercih ederken, hostellere de bir miktar ilgi gösterirler. Bu durum, çeşitli deneyimlere açık bir gece kuşu olduklarını düşündürür.]"
}

st.sidebar.header("View User Persona")
if not data_df.empty and 'device_aid' in data_df.columns:
    # Ensure device_aid is string for selectbox consistency
    unique_device_aids = data_df['device_aid'].astype(str).unique()
    selected_device_aid = st.sidebar.selectbox(
        "Select Device AID to view Persona:",
        options=unique_device_aids,
        index=None, # No default selection
        placeholder="Choose a device_aid..."
    )

    if selected_device_aid:
        st.header(f"Persona for Device: {selected_device_aid}")
        user_data = data_df[data_df['device_aid'].astype(str) == selected_device_aid].iloc[0]
        
        # Cafe Persona
        if 'cafe_cluster' in user_data:
            cafe_cluster_id = user_data['cafe_cluster']
            st.subheader("Cafe Activity Persona:")
            st.write(cafe_persona_descriptions.get(cafe_cluster_id, "No persona description available for this cafe cluster."))
        else:
            st.warning("Cafe cluster information not available for this user.")

        # Ping Persona
        if 'ping_cluster' in user_data:
            ping_cluster_id = user_data['ping_cluster']
            st.subheader("Mobility (Ping) Persona:")
            st.write(ping_persona_descriptions.get(ping_cluster_id, "No persona description available for this ping cluster."))
        else:
            st.warning("Ping cluster information not available for this user.")

        # Restaurant Persona
        if 'restaurant_cluster' in user_data:
            restaurant_cluster_id = user_data['restaurant_cluster']
            st.subheader("Restaurant Activity Persona:")
            st.write(restaurant_persona_descriptions.get(restaurant_cluster_id, "No persona description available for this restaurant cluster."))
        else:
            st.warning("Restaurant cluster information not available for this user.")
else:
    st.sidebar.info("Load data to select a device AID.")
