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