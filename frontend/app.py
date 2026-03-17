import streamlit as st
import requests

# Cấu hình địa chỉ của FastAPI backend
# Mặc định uvicorn chạy ở port 8000
API_URL = "http://127.0.0.1:8000/predict"

# Cài đặt cấu hình trang web
st.set_page_config(page_title="Hệ thống Phát hiện Email Rác", page_icon="📧")

st.title("📧 Email Spam Detector")
st.markdown("Nhập nội dung email vào ô bên dưới để AI kiểm tra xem đây là thư rác (Spam) hay thư bình thường (Ham).")

# Khung nhập liệu cho người dùng
email_content = st.text_area("Nội dung Email:", height=200, placeholder="Dán nội dung email cần kiểm tra vào đây...")

# Nút bấm để gọi API
if st.button("Kiểm tra Email", type="primary"):
    if not email_content.strip():
        st.warning("⚠️ Vui lòng nhập nội dung email trước khi kiểm tra!")
    else:
        with st.spinner("Mô hình đang phân tích..."):
            try:
                # Gửi request dạng text/plain để khớp với cấu hình Body của FastAPI
                headers = {'Content-Type': 'text/plain'}

                # Encode text thành utf-8 để tránh lỗi font chữ tiếng Việt
                response = requests.post(API_URL, data=email_content.encode('utf-8'), headers=headers)

                if response.status_code == 200:
                    result = response.json()
                    prediction = result.get("prediction")

                    st.divider()
                    st.subheader("Kết quả phân tích:")

                    # Tuỳ thuộc vào label output của mô hình (ví dụ: 1 là Spam, 0 là Ham hoặc chuỗi 'spam'/'ham')
                    # Bạn có thể điều chỉnh lại điều kiện if này cho đúng với file .pkl của bạn
                    if str(prediction).lower() in ['1', 'spam']:
                        st.error("🚨 Cảnh báo: Đây rất có thể là thư rác (Spam)!")
                    else:
                        st.success("✅ An toàn: Đây là email bình thường (Ham).")
                else:
                    st.error(f"Lỗi từ Server: {response.status_code} - {response.text}")

            except requests.exceptions.ConnectionError:
                st.error("❌ Không thể kết nối đến Backend. Vui lòng kiểm tra xem FastAPI đã được bật chưa!")