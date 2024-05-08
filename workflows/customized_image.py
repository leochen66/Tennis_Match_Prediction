from flytekit import ImageSpec


IMAGE_NAME = "tennis"
IMAGE_REGISTRY = "localhost:30000"

image_spec = ImageSpec(
    name=IMAGE_NAME,
    packages=["pandas", "numpy", "matplotlib", "scikit-learn", "opendatasets", "bentoml"],
    env={"Debug": "True"},
    registry=IMAGE_REGISTRY
)

