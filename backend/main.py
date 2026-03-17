from fastapi import FastAPI, Body
import pandas as pd
import pickle


app = FastAPI()
model = pickle.load(open("model_detector_email.pkl", "rb"))

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
