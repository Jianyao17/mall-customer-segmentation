import streamlit as st
import pandas as pd
import altair as alt

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

# ==========================================================
# CONFIG
# ==========================================================

st.set_page_config(
    page_title="Mall Customer Segmentation",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# LOAD DATA & TRAIN MODEL
# ==========================================================

@st.cache_resource
def load_model():
    url = "https://raw.githubusercontent.com/kennedykwangari/Mall-Customer-Segmentation-Data/master/Mall_Customers.csv"
    df = pd.read_csv(url)
    X = df[['Annual Income (k$)', 'Spending Score (1-100)']]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = KMeans(
        n_clusters=5,
        init="k-means++",
        random_state=42
    )

    df["Cluster"] = model.fit_predict(X_scaled)
    df["Cluster_Name"] = df["Cluster"].astype(str)

    silhouette = silhouette_score(X_scaled, df["Cluster"])

    summary = df.groupby("Cluster")[
        ["Age", "Annual Income (k$)", "Spending Score (1-100)"]
    ].mean().round(1)

    return df, scaler, model, silhouette, summary

df, scaler, model, silhouette, summary = load_model()

# ==========================================================
# KARAKTERISTIK CLUSTER
# ==========================================================

cluster_info = {
    0: {"name": "Kelas Menengah (Average)", "desc": "Pendapatan dan tingkat pengeluaran yang seimbang (menengah/sedang).", "icon": "🔹"},
    1: {"name": "Target Utama (Target)", "desc": "Pendapatan tinggi dan tingkat pengeluaran yang sangat tinggi. Sangat konsumtif, royal, dan merupakan target promosi yang paling potensial.", "icon": "💎"},
    2: {"name": "Suka Jajan (Careless)", "desc": "Pendapatan rendah namun memiliki tingkat pengeluaran yang sangat tinggi (cenderung boros).", "icon": "🔥"},
    3: {"name": "Super Hemat (Careful)", "desc": "Pendapatan tinggi namun tingkat pengeluarannya sangat rendah. Cenderung berhati-hati dalam membelanjakan uang dan rajin menabung.", "icon": "🛡️"},
    4: {"name": "Konservatif (Sensible)", "desc": "Pendapatan rendah dan tingkat pengeluaran yang juga rendah. Lebih fokus berbelanja untuk kebutuhan pokok.", "icon": "📉"}
}

# Apply mapped names to dataframe for better tooltip in Altair
df["Segment"] = df["Cluster"].map(lambda c: f"{cluster_info[c]['icon']} {cluster_info[c]['name']}")

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:
    st.title("🛍️ Customer Segments")
    st.write("Aplikasi ini mengelompokkan pelanggan menggunakan model **K-Means Clustering**.")
    
    st.divider()
    
    st.header("⚙️ Informasi Model")
    col1, col2 = st.columns(2)
    col1.metric("Algoritma", "K-Means")
    col2.metric("Klaster", "5")
    
    col3, col4 = st.columns(2)
    col3.metric("Data", f"{len(df)} baris")
    col4.metric("Silhouette", f"{silhouette:.2f}")
    
    st.divider()
    st.info("💡 **Tips**: Gunakan Tab Prediksi untuk melihat segmen dari pelanggan baru.")

# ==========================================================
# MAIN LAYOUT
# ==========================================================

st.title("📊 Mall Customer Segmentation Dashboard")
st.markdown("Analisis dan prediksi profil pengeluaran pelanggan mal untuk strategi pemasaran yang lebih tepat sasaran.")

tab_predict, tab_dashboard = st.tabs(["🎯 Prediksi Pelanggan", "📈 Dashboard Analisis"])

# ----------------------------------------------------------
# TAB 1: PREDIKSI
# ----------------------------------------------------------
with tab_predict:
    st.header("Prediksi Segmen Pelanggan Baru")
    st.write("Silakan geser *slider* di bawah ini untuk melihat ke dalam klaster mana pelanggan tersebut masuk.")
    
    # Input Area
    input_col1, input_col2 = st.columns(2)
    with input_col1:
        income = st.slider("Annual Income (k$)", min_value=0, max_value=150, value=60, help="Pendapatan tahunan dalam ribuan dollar")
    with input_col2:
        spending = st.slider("Spending Score (1-100)", min_value=1, max_value=100, value=50, help="Skor pengeluaran berdasarkan riwayat belanja")

    # Predict Action
    if st.button("🔍 Prediksi Segmen Pelanggan", type="primary", width="stretch"):
        # Create a DataFrame with the exact same column names used during training to avoid warnings
        sample_df = pd.DataFrame([[income, spending]], columns=['Annual Income (k$)', 'Spending Score (1-100)'])
        sample = scaler.transform(sample_df)
        cluster = model.predict(sample)[0]
        c_info = cluster_info[cluster]
        
        st.divider()
        
        # Result Area Split: Info (Left) & Chart (Right)
        main_col_left, main_col_right = st.columns([1, 1.2])
        
        with main_col_left:
            st.success("Hasil Prediksi")
            st.metric(label="Cluster ID", value=f"Cluster {cluster}")
            st.subheader(f"{c_info['icon']} {c_info['name']}")
            
            st.info("Karakteristik Segmen")
            st.write(c_info["desc"])
            
            st.write("**Rata-rata Segmen Ini:**")
            m_col1, m_col2, m_col3 = st.columns(3)
            m_col1.metric("Umur", f"{summary.loc[cluster,'Age']:.1f} thn")
            m_col2.metric("Pendapatan", f"${summary.loc[cluster,'Annual Income (k$)']:.1f}k")
            m_col3.metric("Pengeluaran", f"{summary.loc[cluster,'Spending Score (1-100)']:.1f}")
        
        with main_col_right:
            st.subheader("Titik Posisi Pelanggan")
            
            # Base chart for all points
            base_chart = alt.Chart(df).mark_circle(size=60).encode(
                x=alt.X('Annual Income (k$)', scale=alt.Scale(domain=[0, 150])),
                y=alt.Y('Spending Score (1-100)', scale=alt.Scale(domain=[0, 100])),
                color=alt.Color('Segment', legend=alt.Legend(title="Segmen", orient="bottom")),
                tooltip=['Age', 'Annual Income (k$)', 'Spending Score (1-100)', 'Segment']
            ).interactive()

            # Input point chart
            input_df = pd.DataFrame({'Annual Income (k$)': [income], 'Spending Score (1-100)': [spending]})
            input_chart = alt.Chart(input_df).mark_point(
                size=300, shape="cross", color="black", strokeWidth=3
            ).encode(
                x='Annual Income (k$)',
                y='Spending Score (1-100)',
                tooltip=[alt.Tooltip('Annual Income (k$)', title='Your Income'), 
                         alt.Tooltip('Spending Score (1-100)', title='Your Spending')]
            )

            st.altair_chart((base_chart + input_chart).properties(height=450), width="stretch")

# ----------------------------------------------------------
# TAB 2: DASHBOARD
# ----------------------------------------------------------
with tab_dashboard:
    st.header("Ringkasan Seluruh Data")
    
    # K-Means Visual
    st.subheader("Visualisasi Keseluruhan Klaster")
    dash_chart = alt.Chart(df).mark_circle(size=80).encode(
        x='Annual Income (k$)',
        y='Spending Score (1-100)',
        color=alt.Color('Segment', legend=alt.Legend(title="Segmen", orient="bottom")),
        tooltip=['Age', 'Annual Income (k$)', 'Spending Score (1-100)', 'Segment']
    ).properties(height=500).interactive()
    
    st.altair_chart(dash_chart, width="stretch")
    
    st.divider()
    
    col_data1, col_data2 = st.columns(2)
    
    with col_data1:
        st.subheader("Dataset (Berdasarkan Segmen)")
        cols = ['Segment', 'Age', 'Annual Income (k$)', 'Spending Score (1-100)']
        st.dataframe(df[cols], width="stretch", height=250)
        
    with col_data2:
        st.subheader("Rata-rata Tiap Klaster")
        display_summary = summary.copy()
        display_summary["Segment"] = display_summary.index.map(lambda c: cluster_info[c]["name"])
        display_summary = display_summary.set_index("Segment")
        st.dataframe(display_summary, width="stretch", height=250)