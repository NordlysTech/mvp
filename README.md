# mvp


## Getting Started


```bash

docker network create mvp_network

docker build -t nordlys-tech .  


docker run -d --name solvi_mvp --network mvp_network -p 5008:5000 nordlys-tech:latest

docker run -d --name prometheus --network mvp_network -p 9090:9090 -v /Users/salaheddinealabouch/projects/nordlys_tech/mvp/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus

docker run -d --name grafana --network mvp_network -p 3000:3000 grafana/grafana


```