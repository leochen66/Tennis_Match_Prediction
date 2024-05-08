import os
import pandas as pd
import matplotlib.pyplot as plt
import bentoml
from flytekit import task, workflow

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from customized_image import image_spec


ARTIFACTS_FOLDER = os.path.join("artifacts")
MODEL_FILE = os.path.join(ARTIFACTS_FOLDER, "model.pkl")
REPORT_FILE = os.path.join(ARTIFACTS_FOLDER, "report.txt")
IMPORTANCE_PLOT_FILE = os.path.join(ARTIFACTS_FOLDER, "feature_importance_plot.png")


def load_model() -> RandomForestClassifier:
    model = bentoml.sklearn.load_model('tennis-predictor:latest')
    return model


@task(container_image=image_spec)
def train(x: pd.DataFrame, y: pd.Series) -> RandomForestClassifier:
    rf_classifier = RandomForestClassifier(n_estimators=1500, random_state=100, max_depth=6)
    rf_classifier.fit(x, y)

    # model_saved = bentoml.sklearn.save_model("tennis-predictor", rf_classifier)
    # print(f"Model saved:{model_saved}")
    # bentoml.models.push("tennis-predictor:latest")

    # with bentoml.models.create(
    #     name='tennis-predictor', # Name of the model in the Model Store
    # ) as model_ref:
    #     pipeline.save_pretrained(model_ref.path)
    #     print(f"Model saved: {model_ref}")

    return rf_classifier


# todo: not save the model to local
@task(container_image=image_spec)
def evaluation(model: RandomForestClassifier, x_test: pd.DataFrame, y_test: pd.Series):

    # model = load_model()

    # Test on testing data and generate report
    y_pred = model.predict(x_test)
    report = classification_report(y_test, y_pred)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy: ", accuracy)
    print("Classification Report:")
    print(report)

    # Save report
    with open(REPORT_FILE, 'w') as f:
        f.write("Accuracy: " + str(accuracy) + "\n\n")
        f.write("Classification Report:\n")
        f.write(report)

    # Save feature importance plot
    feature_importances = model.feature_importances_
    features = ['Series', 'Court', 'Surface', 'Player_1', 'Player_2', 'Rank_1', 'Rank_2', 'Pts_1', 'Pts_2', 'Odd_1', 'Odd_2']
    importance_df = pd.DataFrame({'Feature': features, 'Importance': feature_importances})
    importance_df = importance_df.sort_values(by='Importance', ascending=False)
    plt.figure(figsize=(6, 4))
    plt.barh(importance_df['Feature'], importance_df['Importance'])
    plt.xlabel('Importance')
    plt.ylabel('Feature')
    plt.title('Feature Importance')
    plt.savefig(IMPORTANCE_PLOT_FILE)
    plt.close()


def predict():
    pre_data = {
        'Series': [0],
        'Court': [1],
        'Surface': [3],
        'Player_1': [506],
        'Player_2': [428],
        'Rank_1': [65],
        'Rank_2': [71],
        'Pts_1': [802],
        'Pts_2': [744],
        'Odd_1': [1.5],
        'Odd_2': [2.63],
    }
    pre_data = pd.DataFrame(pre_data)

    model = load_model()
    predict = model.predict(pre_data)[0]
    print(predict)
