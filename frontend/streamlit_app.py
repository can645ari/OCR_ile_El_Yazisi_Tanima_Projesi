import streamlit as st
import requests

st.set_page_config(page_title="OCR Uygulaması", layout="centered")

st.title("El Yazısı OCR Uygulaması")
st.markdown("Bir görseli **sürükleyip bırakın** ya da tıklayıp seçin. Ardından tanımayı başlatın.")
st.markdown("Gülden buraya foto atacan!")

# 🚀 Sürükle-bırak alanı
uploaded_file = st.file_uploader(
    "📎 Görselinizi buraya bırakın veya tıklayarak seçin",
    type=["jpg", "jpeg", "png"]
)

# Görsel göster
if uploaded_file is not None:
    st.image(uploaded_file, caption="Yüklenen Görsel", use_column_width=True)

    if st.button("🧠 Metni Tanı"):
        with st.spinner("OCR çalışıyor..."):
            response = requests.post(
                "http://127.0.0.1:8000/ocr",
                files={"file": (uploaded_file.name, uploaded_file, "image/jpeg")}
            )
            if response.status_code == 200:
                data = response.json()
                st.success("✅ OCR Başarılı")
                st.markdown("### 🔍 Tanınan Metin:")
                for line in data["result"]:
                    st.markdown(f"- {line}")
            else:
                st.error("❌ OCR sırasında bir hata oluştu.")
