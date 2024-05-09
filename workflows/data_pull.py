import os
import pandas as pd
import opendatasets as od
from flytekit import task, workflow

from aws_logger import logger
from customized_image import image_spec
from config import DATASET_FILE


DATASET_NAME = "atp-tennis-2000-2023daily-pull"
DATASET_LINK = f"https://www.kaggle.com/datasets/dissfya/{DATASET_NAME}"


@task(container_image=image_spec)
def data_pull() -> pd.DataFrame:
    # Pull data from Kaggle
    od.download(DATASET_LINK)
    logger.info("[data_pull]File download successfully")

    # Read file
    filepath = os.path.join(DATASET_NAME, DATASET_FILE)
    if os.path.exists(filepath):
        data = pd.read_csv(filepath)
        return data
    else:
        logger.error("[data_pull]Error: File download failed")
        return None
