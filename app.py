import streamlit as st
import pandas as pd

st.title("📊 استخراج الصفوف ذات القيم المكررة من عمود في ملف Excel")

uploaded_file = st.file_uploader("⬆️ رفع ملف Excel (.xlsx)", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    st.write("🧾 الأعمدة المتوفرة:")
    column = st.selectbox("اختر العمود لاستخراج الصفوف ذات القيم المكررة منه:", df.columns)
    
    if column:
        # حساب تكرار القيم
        value_counts = df[column].value_counts()
        
        # اختيار القيم التي تكررت أكثر من مرة فقط
        duplicated_values = value_counts[value_counts > 1].index
        
        # استخراج الصفوف التي تحتوي هذه القيم المكررة فقط
        duplicated_rows = df[df[column].isin(duplicated_values)]
        
        st.write(f"📊 عدد القيم المكررة في العمود '{column}': {len(duplicated_values)}")
        st.dataframe(duplicated_rows)
        
        @st.cache_data
        def to_excel(df):
            import io
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='DuplicatedRows')
            return output.getvalue()
        
        excel_data = to_excel(duplicated_rows)
        
        st.download_button(
            label="⬇️ تحميل ملف الصفوف المكررة فقط",
            data=excel_data,
            file_name=f"الصفوف_المكررة_{column}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
