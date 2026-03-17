import pandas as pd
import re
import nltk
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
from preprocess import preprocess_text





data = pd.read_csv("email.csv")

target = "Category"
X = data.drop(target, axis=1)
y = data[target]


X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=7
)


processing = ColumnTransformer(
    transformers=[
        (
            "tfidf_message",
            TfidfVectorizer(
                stop_words='english',
                preprocessor=preprocess_text,
                min_df=2,
                max_df=0.95,
                ngram_range=(1, 2)
            ),
            "Message"
        )
    ]
)

pipeline = Pipeline(
    steps=[
        ("processing", processing),
        ("classifier", LinearSVC(
            class_weight="balanced",
            random_state=7
        ))
    ]
)

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)
print(classification_report(y_test, y_pred))


pickle.dump(pipeline, open("model_detector_email.pkl", "wb"))
