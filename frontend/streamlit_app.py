import streamlit as st
import requests

st.set_page_config(page_title="📄 El Yazısı OCR", layout="centered")

# Başlık ve açıklama
st.markdown("<h1 style='text-align: center; color: #f39c12;'>📝 El Yazısı OCR Uygulaması</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 16px;'>"
    "Bir görseli <b>sürükleyip bırakın</b> veya seçin, ardından <b>OCR</b> ile tanıyalım 👇"
    "</p>",
    unsafe_allow_html=True
)

# Dosya yükleme alanı
uploaded_files = st.file_uploader(
    "📎 Görsellerinizi buraya bırakın veya tıklayarak seçin (En fazla 3 adet!)",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# Görseller varsa işleme başla
if uploaded_files:
    if len(uploaded_files) > 3:
        st.error("⚠️ En fazla 3 dosya yükleyebilirsiniz.")
    else:
        # Görselleri yan yana göster
        cols = st.columns(len(uploaded_files))
        for i, uploaded_file in enumerate(uploaded_files):
            with cols[i]:
                st.image(uploaded_file, caption=f"📷 Görsel {i+1}", use_container_width=True)

        # Dinamik buton metni
        button_label = "🔍 OCR ile Tara" if len(uploaded_files) == 1 else "🔍 Hepsini Tara"

        # Tara butonu
        if st.button(button_label):
            with st.spinner("🧠 OCR çalışıyor..."):
                for i, uploaded_file in enumerate(uploaded_files, start=1):
                    response = requests.post(
                        "http://127.0.0.1:8000/ocr",
                        files={"file": (uploaded_file.name, uploaded_file, "image/jpeg")}
                    )
                    if response.status_code == 200:
                        data = response.json()

                        with st.expander(f"📄 Görsel {i} OCR Sonucu"):
                            if not data.get("result"):
                                st.info("⚠️ Bu görselde tanınabilir bir yazı bulunamadı.")
                            else:
                                # OCR çıktısını topla (indirilebilir hale getirmek için)
                                ocr_lines = [text for text, _ in data["result"]]
                                ocr_text = "\n".join(ocr_lines)

                                # Tanınan metinleri göster
                                for text, score in data["result"]:
                                    st.markdown(
                                        f"<div style='font-size:18px;'>• <b>{text}</b> "
                                        f"<span style='color:#aaa;'>(🧠 Güven: {float(score):.2f})</span></div>",
                                        unsafe_allow_html=True
                                    )
                                st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
                                # 📥 TXT olarak indirilebilir buton
                                st.download_button(
                                    label="📥 OCR sonucunu TXT olarak indir",
                                    data=ocr_text,
                                    file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}_ocr.txt",
                                    mime="text/plain"
                                )
                    else:
                        st.error(f"❌ Hata oluştu: {uploaded_file.name}")

# Footer – Katkıda Bulunanlar
st.markdown("---")
st.markdown(
    "<p style='text-align: left; font-size: 14px; color: gray;'>"
    "👥 <b>Katkıda Bulunanlar:</b> Yusuf Ataş, Gülden Akarsu, Can Arı"
    "</p>",
    unsafe_allow_html=True
)
