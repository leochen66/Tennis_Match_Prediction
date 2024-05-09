import bentoml
import numpy as np
import pandas as pd

from aws_logger import logger


@bentoml.service(
    resources={"cpu": "2"},
    traffic={"timeout": 10},
)
class TennisPrediction:
    def __init__(self) -> None:
        self.model = bentoml.sklearn.load_model('tennis-predictor:latest')

    @bentoml.api
    def tennis_match_prediction(self, odd1: float, odd2: float) -> int:
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
            'Odd_1': [odd1],
            'Odd_2': [odd2],
        }
        pre_data = pd.DataFrame(pre_data)

        predict = self.model.predict(pre_data)[0]
        return predict