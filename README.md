# mvp


## Getting Started


**Build the Docker image:**

```bash
docker-compose build
```

**Run all services with a single command:**

```bash
docker-compose up -d
```

**Stop the services:**

```bash
docker-compose down
```


**Connecting Grafana to Prometheus :**

To add Prometheus as data source in Grafana :

Connect to Grafana :

```bash
user : admin
password : admin
```

In connections : add a new data source

Set the prometheus server URL : http://prometheus:9090


**LLM Config :**

To use a specific LLM go to config.yaml :

Under llms ==> llm_name write the code of the llm you want to use among those available in instantiate_llm_model function at services.llm_utils.py


docker run -p 9090:9090 -v /Users/salaheddinealabouch/projects/nordlys_tech/mvp/app/backend/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus



docker run -d --name solvi_mvp --network mvp_network -p 5008:5000 nordlys-tech:latest


docker pull mongodb/mongodb-community-server:latest
docker run --name mongodb --network mvp_network -p 27017:27017 -d mongodb/mongodb-community-server:latest


Connect to the MongoDB Deployment with mongosh

mongosh --port 27017