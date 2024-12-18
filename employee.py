import streamlit as st
import pandas as pd

# Judul Dashboard
st.title("Dashboard Analisis Faktor yang Mempengaruhi Attrition Rate")

# Tombol interaktif
action = st.radio(
    "Pilih tindakan:",
    ["Tampilkan Data", "Analisis Korelasi", "Tampilkan Grafik"]
)

# Memuat dataset
data = pd.read_csv('data_cleaned.csv')

default_columns = ["Attrition", "Age", "JobLevel", "MonthlyIncome"]
selected_columns = st.sidebar.multiselect(
    "Pilih Kolom untuk Menampilkan Deskripsi Data", 
    options=data.columns, 
    default=default_columns  # Kolom default yang dipilih
)
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

match action:

    case "Tampilkan Data":
        # Menampilkan data di kolom pertama
        st.header("Data Awal")
        st.dataframe(data.head())

        # Menampilkan deskripsi data di kolom kedua
        st.header("Deskripsi Statistik Data")
        st.write(data[selected_columns].describe())

    case "Analisis Korelasi":
        # Analisis korelasi di kolom pertama
        st.header("Korelasi Numerik terhadap Attrition")
        if "Attrition" in data.columns:
            numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
            correlation = data[numeric_columns].corr()["Attrition"].sort_values(ascending=False)
            
            # Visualisasi korelasi menggunakan bar_chart di kolom pertama
            st.bar_chart(correlation)

    case "Tampilkan Grafik":
        # Pembagian grafik berdasarkan kategori
        col1.header("Demografi Karyawan")
        selected_category = col1.selectbox("Pilih Kolom Kategori (Demografi):", options=data.select_dtypes(include=['object']).columns)

        if selected_category:
            # Menghitung jumlah tiap kategori berdasarkan Attrition
            category_counts = data.groupby([selected_category, 'Attrition']).size().unstack(fill_value=0)
            
            # Visualisasi distribusi kategori dengan Streamlit bar_chart di kolom pertama
            col1.bar_chart(category_counts)

        # Kepuasan Kerja
        col2.header("Kepuasan Kerja")
        selected_satisfaction = col2.selectbox("Pilih Kolom Kepuasan Kerja:", options=["JobSatisfaction", "EnvironmentSatisfaction", "RelationshipSatisfaction", "WorkLifeBalance"])

        if selected_satisfaction:
            satisfaction_counts = data.groupby([selected_satisfaction, 'Attrition']).size().unstack(fill_value=0)
            col2.bar_chart(satisfaction_counts)

        # Gaji dan Penghasilan
        col3.header("Rata-rata Gaji dan Penghasilan")
        selected_numeric = col3.selectbox("Pilih Kolom Gaji/Penghasilan:", options=["MonthlyIncome", "HourlyRate", "DailyRate"])

        if selected_numeric:
            # Distribusi gaji berdasarkan attrition
            income_stats = data.groupby('Attrition')[selected_numeric].mean()
 
            col3.bar_chart(income_stats)

        # Kolom 4: Kolom lain untuk faktor terkait
        col4.header("Faktor Lainnya")
        selected_other = col4.selectbox("Pilih Kolom Lainnya:", options=["Age", "JobLevel", "NumCompaniesWorked", "YearsAtCompany"])

        if selected_other:
            other_counts = data.groupby('Attrition')[selected_other].mean()
            col4.bar_chart(other_counts)


        st.header("Kesimpulan Analisis")

        st.markdown("""
            Berdasarkan analisis dan visualisasi data tentang faktor-faktor yang mempengaruhi **attrition rate** (tingkat pengunduran diri) karyawan, berikut adalah beberapa kesimpulan yang dapat diambil:
                    
            - Faktor-faktor seperti **usia (age)**, **jumlah perusahaan yang pernah bekerja (NumCompaniesWorked)**, **gaji bulanan (MonthlyIncome)**, **kepuasan pekerjaan (JobSatisfaction)**, dan **work-life balance** menunjukkan pengaruh signifikan terhadap tingkat pengunduran diri. Karyawan dengan usia lebih muda, gaji lebih rendah, serta kepuasan kerja yang rendah atau work-life balance yang buruk cenderung memiliki tingkat attrition yang lebih tinggi.

            - Karyawan yang lebih muda atau dengan gaji yang lebih rendah lebih cenderung untuk mengundurkan diri. Hal ini menunjukkan bahwa faktor keuangan dan tahap karir yang lebih awal (misalnya, karyawan yang baru memulai karir) mungkin lebih rentan terhadap keputusan untuk berhenti kerja.

            - Karyawan yang memiliki pekerjaan sampingan atau mereka yang telah bekerja di beberapa perusahaan cenderung memiliki tingkat attrition yang lebih tinggi. Ini mungkin menunjukkan bahwa karyawan yang lebih berpengalaman atau yang mencari peluang lain memiliki kecenderungan untuk keluar lebih cepat.

            - Kolom seperti **status pernikahan (MaritalStatus)** dan **perjalanan bisnis (BusinessTravel)** juga dapat digunakan untuk memprediksi kelompok karyawan dengan risiko attrition yang tinggi. Karyawan yang mungkin sering melakukan perjalanan bisnis atau yang memiliki status pernikahan tertentu (misalnya, yang tidak menikah) mungkin lebih rentan terhadap pengunduran diri.
            """)
