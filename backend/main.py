from fastapi import FastAPI, Body
import pandas as pd
import pickle
import sys

app = FastAPI()

# Thêm try-except để bắt lỗi khi load model
try:
    print("⏳ Đang tải mô hình AI...", flush=True)
    model = pickle.load(open("model_detector_email.pkl", "rb"))
    print("✅ Đã load model thành công!", flush=True)
except Exception as e:
    print(f"❌ LỖI KHI LOAD MODEL: {e}", flush=True)
    sys.exit(1)
@app.post("/predict")
def predict_spam(text: str = Body(..., media_type="text/plain")):
    clean_text = (
        text.replace("\r\n", " ")
            .replace("\n", " ")
            .replace("\t", " ")
            .strip()
    )

    input_df = pd.DataFrame({"Message": [clean_text]})
    prediction = model.predict(input_df)[0]

    return {"prediction": prediction}
