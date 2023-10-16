# Machine Learning System
Before starting explaining the system I would just like to note that I overscoped this assignment, under-estimated some parts and therefore needed to take some shortcuts. With regards to the time-limit of 8 hours I am very happy with the outcome, however, there are some clear pitfalls that I could have avoided by spending more time in the design phase.


Things where I took shortcuts:
* Tests - I added 5 tests just to show you that I know that tests are important, however, test coverage is low.
* Env-variables - Some env variables are hardcoded, some are in config, and some in the config are not even used. This would be caught by more testing.
* Overall infrastructure - Separation of responsibility could have been better.
* Error handling - I would like to implement custom errors for easier debugging, also, adding error handling on all possible failing points.
* Monitoring - I assume a lot of things, like the fact that there is data etc. In real work I would like to check if the data is available or not before running the pipeline.
* Type-hinting - Since I write a lot of go and dart I believe type-hinting is crucial, but I decided to only type hints with standard types due to time constraint.


Known bugs:
* Celery workers sometimes do not find the pipelines, simply issue the command again to solve it, but yeah not sure why.
* The time travel function is not working, simply due to time constraint. But the idea is presented below.




## The System
The assignment was to build the pipeline for training a model and produce predictions with the said model.


I decided to overscope the assignment in order to show you my engineering skills and my interest. So instead of just a training and prediction pipeline, I tried to build a more complex ml-system.


The system I have built have following services:


* Training and Prediction pipelines (Mandatory)
* Scheduling for pipelines (Mandatory)
* Endpoint to trigger pipelines manually with custom parameters.
* Model registry to keep track of current production model and model-history.
* Run registry to keep track of previous runs.
* Automatic validation step of new models, if the model is accepted it is shipped to production, if it fails the user will be notified for manual inspection.
* Pub/Sub system for easier onboarding of external systems.




Here is a diagram over the overall architecture
![Alt text](<Untitled Diagram.drawio.png>)



### Controller service
Controller service is the user-interface of the ml-system, this is a rest-endpoint that is responsible for scheduling and submitting jobs and keeping track of previous states (models/data).


The controller service is backed by a Postgres Database for storing information, and a celery worker for scheduling.


The controller service is also the one notifying subscribers of new models and new prediction output.


### ML Job Service
The ml-job-service is a "dumb" service that is responsible for running jobs that the controller service is submitting. Similar to a spark-cluster, but it is celery.


The ml job service gets a job plus all its metadata from the controller service. The service will then fetch the data and/or model, perform the steps, save the output (model / data) and then inform the controller service about the run by sending data over HTTP.


It is then the Controller service that decides if the model should be promoted to production or not. The ml job service only does the job.


### Filestore
File store is some kind of blob storage.


### Redis
Right now redis is responsible for a lot, like the celery-queue and pub-sub. In production we would not use the same redis cluster.


### Timetravel
_Time travel is not implemented to 100%, so it is not working._


The idea is to append only data-sources with a `created_at` column. When using time-travel the data source will first be filtered with `created_at <= time_travel_date`. This is the data that was available on that day.


For prediction, the data source will be filtered with the same logic above. The model used will be fetched with following query
```
WITH LatestEntries AS (
SELECT model_name, MAX(created_at) as latest_created_at
FROM model_log
WHERE created_at <= <time_travevl_date>
GROUP BY model_name
)
SELECT ml.*
FROM model_log ml
JOIN LatestEntries le ON ml.model_name = le.model_name AND ml.created_at = le.latest_created_at;
```




If we want to retrain a model with the exact same parameters we simply fetch the metadata from the model_log table.


## Design choices


#### Modularity
The idea was to build a modular system to easily build more pipelines with different sources, destinations and models.


The pipelines are built around the `PredictPipeline` and the `TrainingPipeline`. A pipeline is composed of different `components`, all components have a `BaseClass`.


An example is the DataSource component in the ml-job-service.
```
class BaseDataSource(ABC):
@abstractmethod
def get_dataframe(self) -> pd.DataFrame:
pass
```


All DataSources need to have a `get_dataframe` method that returns a dataframe. This way we can simply build a new `DataSource`, ex `S3DataSource`, and just swap the current data-source object in the pipeline.


This is applicable for all components in the pipeline.


_8 hours is to little of time to make a perfect system, but I am happy with the overall outcome._


#### Dependency injection with factory functions
I decided to go with dependency injection since I believe it is a superior design, avoids nasty inheritance and makes testing easier by mocking.


To make it easier for use, I often pair DI with factory methods.


Dependency injection is also a modular design, making it easier to switch systems. Ex.


```
class ModelRegistryService:
def __init__(self, model_log_repository, pub_sub_client) -> None
```


If we decided to go with another pub-sub client we simply just implement a new class with this baseclass and inject


```
class BasePubSubClient(ABC):
@abstractmethod
def publish(self, topic: str, message: str):
pass
```


#### Pub-sub communication
By using pub-sub, new systems can easily be onboarded by simply subscribing to events that are of interest, instead of calling each service.


#### Celery - Distributed work queue
I wanted to do this a bit async and distributed and needed a scheduler. I did not feel like using Airflow, because I just didn't. So I started researching celery.


It sounded really promising, and I managed to implement the functionality I wanted, but I am not sure what I think about it.


Could probably be done in a better way.




#### Trunk-based - Append only
I decided to go with an append-only design. I believe this makes sense with time series data since a value should not be able to change in the past, if it does, it should be added as a new record or an adjustment.


This design choice is also in the model-registry. There is no way to "demote" a model, instead demotion is done by promoting a new model. So if you want to "roll-back" to an earlier model you need to promote the old model to production.


This way we keep all history, making time travel and auditing possible.


## How to run
The full system is deployed with docker-compose. First you need to install docker-compose, this is not a guide on how to do that.


From the root directory of this project


First run:
```
docker compose build
```
Second run:
```
docker compose up
```


Third run(optional):
```
curl -X GET http://localhost:5050/health/
curl -X GET http://localhost:5000/health/
```


Fourth migrate database:

!!! Have not had time to look into why this does not work, but if you get `zsh: no matches found: http://localhost:5000/migrate/?version=000` then just use your webbrowser to invoke that endpoint !!!

```
curl http://localhost:5000/migrate/?version=000
```


If you need to downgrade and start over:
```
curl -X http://localhost:5000/migrate?version=000?direction=down
```


## Invoke endpoints
Below are curl commands on how to invoke different endpoints, if you don't have curl you are on your own.


### Submit training job - Internal
If you get an error first time, just send the same request again. This has something to do with how celery discover tasks and handles the queque. I have not had time to dig into this.

```
curl -X POST http://localhost:5000/job/train \
-H "Content-Type: application/json" \
-d '{
"file_path": "/data/solar-dataset.pq",
"start_date": "2017-01-01",
"end_date": "2017-12-31",
"model_name": "forecast_model"
}'
```


If you want to replicate the training-step from a previous time you can use the time-travel function by adding


NOT IMPLEMENTED
```
{
"time_travel": "true",
"time_travel_date": "2017-01-01"
}
```


This would filter the data so only data available on that day is used for training.


### Submit prediction job - Internal
If you get an error first time, just send the same request again. This has something to do with how celery discover tasks and handles the queque. I have not had time to dig into this.

```
curl -X POST http://localhost:5000/job/predict \
-H "Content-Type: application/json" \
-d '{
"file_path": "/data/solar-dataset.pq",
"model_name": "forecast_model",
"start_date": "2017-01-01",
"end_date": "2017-01-02"
}'
```


If you want to re-create output with the model that was in production the specific day you can add time-travel parameters:


NOT IMPLEMENTED
```
{
"time_travel": "true",
"time_travel_date": "2017-01-01"
}
```


This will take the model that was in production that given day and make predictions with it.


### Promote Model - Internal
If a model fails the evaluation criteria the user can promote it to prod manually.


You can also promote a old model.


```
curl -X POST http://localhost:5000/model/promote \
-H "Content-Type: application/json" \
-d '{
"model_name": "forecast_model",
"model_version_id": "yYcatdlFCk"
}'


```


### Demote Model - Internal
You could demote a model by putting the previous production model in production.


_Known issue: you can only demote once, then it will just start switching between the models, use /promote instead._


```
curl -X GET http://localhost:5000/model/demote?model_name=forecast_model
```
