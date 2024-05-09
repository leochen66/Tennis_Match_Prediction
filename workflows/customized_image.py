from flytekit import ImageSpec
from aws_logger import logger


with open("hello.json", "r") as f:
    cert_data = json.load(f)

env = {
    "Debug": "True",
    "BENTO_CLOUD_API_KEY": cert_data["BENTO_CLOUD_API_KEY"],
    "BENTO_CLOUD_API_ENDPOINT": cert_data["BENTO_CLOUD_API_ENDPOINT"],
    "AWS_ACCESS_KEY_ID": cert_data["AWS_ACCESS_KEY_ID"],
    "AWS_SECRET_ACCESS_KEY": cert_data["AWS_SECRET_ACCESS_KEY"],
    "AWS_DEFAULT_REGION": cert_data["AWS_DEFAULT_REGION"]
}

image_spec = ImageSpec(
    name="tennis",
    packages=["pandas", "numpy", "matplotlib", "scikit-learn", "opendatasets", "bentoml", "boto3", "watchtower"],
    env=env,
    registry="localhost:30000"
)