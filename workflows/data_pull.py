import os
import pandas as pd
import opendatasets as od
from flytekit import task, workflow

from customized_image import image_spec


DATASET_NAME = "atp-tennis-2000-2023daily-pull"
DATASET_LINK = f"https://www.kaggle.com/datasets/dissfya/{DATASET_NAME}"
DATASET_FILE = "atp_tennis.csv"
DATASET_SAVE = "data"


@task(container_image=image_spec)
def data_pull() -> pd.DataFrame:
    # Pull data from Kaggle
    od.download(DATASET_LINK)

    # change file path
    filepath = os.path.join(DATASET_NAME, DATASET_FILE)
    if os.path.exists(filepath):
        data = pd.read_csv(filepath)
        return data
    else:
        print(f"Error: File download failed")
        return None
