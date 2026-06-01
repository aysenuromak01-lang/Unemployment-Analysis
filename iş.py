import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.title("📊 Covid-19 Dönemi İşsizlik Oranı Veri Görselleştirme")
st.write("Hindistan işsizlik verilerini dinamik grafikler ve tablolar ile analiz edin.")

# 1. Veriyi Yükle ve Temizle
@st.cache_data
def load_data():
    df = "unemployment.csv"
    data = pd.read_csv(df)
    data.columns = ["States", "Date", "Frequency", "Estimated Unemployment Rate", 
                    "Estimated Employed", "Estimated Labour Participation Rate", 
                    "Region", "longitude", "latitude"]
    return data

df = load_data()

# Sekmeli Arayüz Tasarımı
tab1, tab2, tab3 = st.tabs(["📉 Korelasyon & Sayısal Grafikler", "🗺️ Bölgesel Dağılım (Sunburst)", "📋 Ham Veri"])

with tab1:
    st.subheader("Özellikler Arasındaki Korelasyon Matrisi")
    # Sadece sayısal sütunları seçip korelasyon matrisi çizdirme
    numeric_df = df[["Estimated Unemployment Rate", "Estimated Employed", "Estimated Labour Participation Rate", "longitude", "latitude"]]
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig)
    
    st.subheader("Bölgelere Göre Tahmini Çalışan Sayısı Dağılımı")
    # Orijinal makaledeki tahmini çalışan sayısı grafiği
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.histplot(x="Estimated Employed", hue="Region", data=df, multiple="stack", ax=ax2)
    st.pyplot(fig2)

with tab2:
    st.subheader("Bölge ve Eyaletlere Göre İşsizlik Oranı Dashboard'u")
    # Orijinal makalede dashboard için kullanılan etkileşimli Sunburst grafiği
    fig_sunburst = px.sunburst(df, path=["Region", "States"], 
                               values="Estimated Unemployment Rate",
                               title="Bölgeler ve Eyaletlere Göre İşsizlik Oranları Payı",
                               color_continuous_scale="RdYlGn")
    st.plotly_chart(fig_sunburst, use_container_width=True)

with tab3:
    st.subheader("Filtrelenebilir Veri Seti")
    # Kullanıcının seçtiği bölgeye göre tabloyu filtreleme özelliği
    regions = ["Hepsi"] + list(df["Region"].unique())
    selected_region = st.selectbox("Analiz etmek istediğiniz bölgeyi seçin:", regions)
    
    if selected_region == "Hepsi":
        st.dataframe(df, use_container_width=True)
    else:
        filtered_df = df[df["Region"] == selected_region]
        st.dataframe(filtered_df, use_container_width=True)