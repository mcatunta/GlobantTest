# Coding challenge Globant

## 1. Local deployment

- *Install docker desktop.*
- *Update the configuration for docker-compose if you need (changing ports or other).*
- *Open a terminal an execute*

```
docker-compose up

```

## 2. Cloud deployment

- *Deploy or activate a database service on cloud (RDS PostgreSQL).*
- *Install docker.*
- *Open a terminal, join into __Api__ folder.*
- *Generate the image executing the command:*

```
docker build -t globant_api .

```
- *Upload the image to any cloud container register (ECR).*
- *Deploy the image using any any cloud container manager (ECS).*
- *Set the environment variable DATABASE_URI with credentials to connect to the database.*