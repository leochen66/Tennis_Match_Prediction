# Tennis_Match_Prediction
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

3. Build docker image and regist the image to cluster
```
docker build -t localhost:30000/tennis-predictor:v1.0.0 .
docker tag localhost:30000/tennis-predictor:v1.0.0 localhost:30000/tennis-predictor:v1.0.0
docker push localhost:30000/tennis-predictor:v1.0.0
```

4. Run workflow
```
pyflyte run --remote -p tennis-match-prediction -d development --copy-all workflows/model_deployment.py wf
```