# Code Challenge Template

Do
`
docker-compose up --build
`
in root. It will run tests. Ingest data and Perform Analysis.

Ingesting data takes 200 secs average.

Swagger is available at http://localhost:8000/docs endpoint.

## Deployment
For deployment I would use tools like jenkins and git. I would also use EC2, ElasticIP and RDBMS services of AWS. 
For ingesting the data and performing analytics over it I have created 2 scripts in weatherproject/scripts directory. We can extract that logic into a celery periodic task. For this we may also choose to use redis as a broker.

Screenshots are in answers/ directory.
