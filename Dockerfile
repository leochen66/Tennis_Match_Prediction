ARG PYTHON_VERSION
FROM python:3.8-slim-bookworm

MAINTAINER Flyte Team <users@flyte.org>
LABEL org.opencontainers.image.source=https://github.com/flyteorg/flytekit

WORKDIR /root
ENV PYTHONPATH /root
ENV FLYTE_SDK_RICH_TRACEBACKS 0

ARG VERSION
ARG DOCKER_IMAGE

# Copy the atp_tennis.csv file into the image
COPY data/atp_tennis.csv /root/atp_tennis.csv

# Run a series of commands to set up the environment:
# 1. Update and install dependencies.
# 2. Install Flytekit and its plugins.
# 3. Install additional Python packages.
# 4. Clean up the apt cache to reduce image size.
# 5. Create a non-root user 'flytekit' and set appropriate permissions for directories.
RUN apt-get update && apt-get install build-essential -y \
    && pip install --no-cache-dir -U flytekit==1.12.0 \
        flytekitplugins-pod==1.12.0 \
        flytekitplugins-deck-standard==1.12.0 \
        pandas \
        numpy \
        matplotlib \
        scikit-learn \
        opendatasets \
        bentoml \
    && apt-get clean autoclean \
    && apt-get autoremove --yes \
    && rm -rf /var/lib/{apt,dpkg,cache,log}/ \
    && useradd -u 1000 flytekit \
    && chown flytekit: /root \
    && chown flytekit: /home \
    && :

USER flytekit

ENV FLYTE_INTERNAL_IMAGE "$DOCKER_IMAGE"
