# Tennis Match Prediction
## Overview
This is an end-to-end Flyte project orchestrates a seamless pipeline from data fetching and preprocessing to model training and deployment. The model is a random forest model predicting tennis matches, it is eventually deployed on AWS EKS with Seldon as API service.
![](/images/cluster.png)

## Dataset
The dataset is pulled from Kaggle: https://www.kaggle.com/datasets/dissfya/atp-tennis-2000-2023daily-pull

## Run workflow on Remote Flyte cluster

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

## Run workflow on local machine
```
cd Tennis_Match_Prediction/workflows
pyflyte run model_deployment.py wf
```

## How to install Seldon on AWS EKS
1. Create EKS cluster
```
eksctl create cluster \
--name seldon-python-cluster \
--region ap-southeast-2 \
--node-type t3.medium \
--nodes 2 \
--nodes-min 1 \
--nodes-max 3
```
2. Connect to cluster
```
aws eks update-kubeconfig --region ap-southeast-2 --name seldon-python-cluster
```
3. Install Istio
```
curl -L https://istio.io/downloadIstio | sh -
cd istio-1.22.0
export PATH=$PWD/bin:$PATH
istioctl install --set profile=demo -y
kubectl label namespace default istio-injection=enabled
```
```
kubectl apply -f - << END
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: seldon-gateway
  namespace: istio-system
spec:
  selector:
    istio: ingressgateway # use istio default controller
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "*"
END
```
4. Install Seldon Core
```
kubectl create namespace seldon-system

helm install seldon-core seldon-core-operator \
    --repo https://storage.googleapis.com/seldon-charts \
    --set usageMetrics.enabled=true \
    --set istio.enabled=true \
    --namespace seldon-system
```
5. Get cluster IP and port
```
export INGRESS_HOST=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
export INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].port}')
export INGRESS_URL=$INGRESS_HOST:$INGRESS_PORT
echo $INGRESS_URL
a247d8084dcf14021ae98c9bea35fe4a-186038092.ap-southeast-2.elb.amazonaws.com:80
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

7. Deployment: Deployment stage is implemented with **Seldon**. Seldon is able to pack machine learning models in a docker container and deploy as an API on Kubernetes. An API document can be found on: http://<ingress_url>/seldon/seldon/tennis-model/api/v1.0/doc/
![](/images/api.png)

Extra: Logs are uploaded to **AWS CloudWatch**.