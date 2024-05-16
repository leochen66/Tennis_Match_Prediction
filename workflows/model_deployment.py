import os
# import bentoml
import typing
import subprocess
from flytekit import task, workflow, conditional

from aws_logger import logger
from data_pull import data_pull
from data_preprocess import data_preprocessing, data_split
from model_train import train, evaluation
from customized_image import image_spec


@task(container_image=image_spec)
def deployment():
    logger.info(f"Model approved, start deployment")

    # deploy by seldon (This is only support on local excution)
    current_dir = os.path.dirname(__file__)
    script_path = os.path.join(current_dir, "..", "seldon_deployment.sh")
    subprocess.run(["sh", script_path])

    # todo: Troubleshooting with bentoML team, error occure when annotate model in bentofile.yaml file
    # bentoml.deployment.create(bento = "./", name = "tennis-prediction-flyte")
    

@task(container_image=image_spec)
def discard() -> int:
    logger.info(f"Model not approved, will not trigger deployment")
    return -1


@task(container_image=image_spec)
def deployment_check(accuracy:float) -> bool:
    if accuracy > 0.6:
        return True
    else:
        return False


# Only for debug purpose
# @task(container_image=image_spec)
# def debug_file2() -> str:
#     current_directory = os.getcwd()
#     files = os.listdir(current_directory)
#     file_names = [str(file) for file in files]
#     return ', '.join(file_names)

# @task(container_image=image_spec)
# def debug_file2(files: str) -> str:
#     return files


@workflow
def wf():
    data = data_pull()
    x_data, y_data = data_preprocessing(matches_df=data)
    x_train, x_test, y_train, y_test = data_split(x=x_data, y=y_data)
    model = train(x=x_train, y=y_train)
    accuracy = evaluation(model=model, x_test=x_test, y_test=y_test)
    is_deploy = deployment_check(accuracy=accuracy)
    conditional("deployment_check").if_(is_deploy.is_true()).then(deployment()).else_().then(discard())


if __name__=="__main__":
    wf()