# Table of Contents

- [Original exercise](#original-exercise)
- [System architecture](#system-architecture)
- [Quickstart](#quickstart)

# Original exercise

** Removed **

# System architecture

Project based on microservices. Right now there's just one - the crawler. In case this needs to add more functionalities, each one should be a new micro. There's a folder with utilities that might be common to all (or several) microservices: [`common-utils`](./common-utils/README.md)

The microservice is structured in three layers, to increase modularity:
- Action layer: the internal API
- Repository layer: used for transformations and/or modifications to the raw data coming from DBs or 3rd parties. For instance, if there's a need to modify the sitemap urls to remove the 'https://', that should be done here.
- Client layer: communication with 3rd parties. Ideally, no data modification should be performed here.

Also, there's a server built on FastAPI to communicate with the system. Right now the only endpoints are a simple healthcheck (currently unused, necessary for a future deployment) and the GET crawl, that returns the sitemap. To access the swagger, go to [http://localhost:8081/docs](http://localhost:8081/docs) with the docker container up and running.

There's also a Redis microservice for caching - if two identical requests come through within the expiration window, the first one will be fulfilled by the system and stored into Redis; the second one will be served from Redis.

# Quickstart

* To get the docker container and hence the server up and running:

```
docker-compose up --build crawler
```  

* Getting the sitemap of a webpage is as easy as hitting the crawl endpoint. From a terminal, or postman (note that this example will crawl `https://news.ycombinator.com`):

```
curl -X 'GET' \
  'http://localhost:8081/api/crawl?url=https%3A%2F%2Fnews.ycombinator.com' \
  -H 'accept: application/json'
```

* To run tests locally you need to use virtualenv
```
virtualenv -p python3.7 venv
source venv/bin/activate
pip install -r requirements.txt
pytest --cov
```

* To run linter locally you need pycodestyle:
```
pip install pycodestyle
pycodestyle --max-line-length=120 --exclude='*env' crawler
```
