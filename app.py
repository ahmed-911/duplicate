import streamlit as st
import pandas as pd

st.title("📊 استخراج التكرار من عمود في ملف Excel")

uploaded_file = st.file_uploader("⬆️ رفع ملف Excel (.xlsx)", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    st.write("🧾 الأعمدة المتوفرة:")
    column = st.selectbox("اختر العمود لاستخراج التكرار منه:", df.columns)
    
    if column:
        value_counts = df[column].value_counts()
        df['تكرار القيمة'] = df[column].map(value_counts)
        
        st.write(f"📊 عدد التكرارات لكل قيمة في العمود '{column}':")
        st.dataframe(value_counts)
        
        st.write("🗂️ عرض البيانات مع عمود التكرار:")
        st.dataframe(df)
        
        # زر لتحميل النتائج كملف Excel
        @st.cache_data
        def to_excel(df):
            import io
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
                writer.save()
            processed_data = output.getvalue()
            return processed_data
        
        excel_data = to_excel(df)
        
        st.download_button(
            label="⬇️ تحميل الملف مع التكرار",
            data=excel_data,
            file_name=f"الصفوف_مع_التكرار_{column}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
