import os
import bentoml
import typing
from flytekit import task, workflow

from data_pull import data_pull
from data_preprocess import data_preprocessing, data_split
from model_train import train, evaluation

from customized_image import image_spec


def deployment_check(accuracy):
    if accuracy > 0.7:
        return True
    else:
        return False


# @task(container_image=image_spec)
# def debug_file2() -> str:
#     current_directory = os.getcwd()
#     files = os.listdir(current_directory)
#     file_names = [str(file) for file in files]
#     return ', '.join(file_names)

# @task(container_image=image_spec)
# def debug_file2(files: str) -> str:
#     return files


# def deployment_bentoml():
#     bentoml.deployment.create(bento="tennis_prediction:latest", name="tennis-match")


@workflow
def wf():
    data = data_pull()
    x_data, y_data = data_preprocessing(matches_df=data)
    x_train, x_test, y_train, y_test = data_split(x=x_data, y=y_data)
    model = train(x=x_train, y=y_train)
    evaluation(model=model, x_test=x_test, y_test=y_test)


if __name__=="__main__":
    wf()
