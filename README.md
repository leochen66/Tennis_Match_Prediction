# Tennis Match Prediction
## Overview
This is an end-to-end Flyte project, encompassing data fetching, data preprocessing, model training, and model deployment. The entire pipeline is executed on a Flyte cluster.
![](/images/cluster.png)

## Dataset
The dataset is pulled from Kaggle: https://www.kaggle.com/datasets/dissfya/atp-tennis-2000-2023daily-pull

## Run workflow in Flyte cluster

1. Start Flyte cluster in local machine
```
export FLYTECTL_CONFIG=~/.flyte/config-sandbox.yaml
flytectl demo start
```

2. Create project on Flyte cluster
```
flytectl create project \
      --id "tennis-match-prediction" \
      --labels "my-label=tennis-match-prediction" \
      --description "A Flyte project for tennis match prediction" \
      --name "Tennis"
```

3. Run workflow
```
pyflyte run --remote -p tennis-match-prediction -d development --copy-all workflows/model_deployment.py wf
```

If a customized docker image is needed, build image by the following command. In this project, Flyte ImageSpec is applied to build customized docker, so no manually build required.
```
docker build -t localhost:30000/tennis-predictor:v1.0.0 .
docker tag localhost:30000/tennis-predictor:v1.0.0 localhost:30000/tennis-predictor:v1.0.0
docker push localhost:30000/tennis-predictor:v1.0.0
```


## Workflows Descriprion
![](/images/Workflows.png)

1. Data Pull: Fetch data from **Kaggle**

2. Data Preprocessing: Remove redundant data rows and columns, and featurize the dataset

3. Data Split: Split the data into training dataset and validation dataset

4. Data Train: Train a random forest model.

5. Evaluation: Generate a report with metrics, as well as a feature importance report. Once evaluation is complete, the artifacts will be **pushed to AWS S3**.
![](/images/files.png)

6. Deployment Check: A trigger for deployment. Check accuracy computed in the evaluation task is greater than 0.6, then start deployment. More trigger conditions can be added.

7. Deployment: Deployment stage is implemented with **BentoML**. BentoML is able to build deployment artifacts and deploy as an API on BentoCloud. This has been tested in the local environment. However, there is an issue currently being troubleshooted with BentoML team.

Extra: Logs are uploaded to **AWS CloudWatch**.
![](/images/log.png)