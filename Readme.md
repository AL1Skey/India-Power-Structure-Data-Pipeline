# India Power Structure Data Pipeline

This project are about Data Pipeline and clean data with airflow and then save it in local

# Tools

1. Docker
2. ElasticSearch
3. Pandas
4. Airflow
5. Great Expectations

# How it's Works

1. Main Data will be stored on dataset folder with name 'dataset.csv'
2. Docker will deploy the airflow and airflow can be accessed with airflow-webserver container in localhost with port 8080
3. DAGS will be shown on airflow and can be running
4. When DAGS running, file will be retreived from docker server, then it'll be preprocessing the data like changing the columns name, handling missing values, and changing data type to expected dataset.
5. After that, data that has been cleaned will be saved on docker server
6. Clean data will be deployed on elastic search kibana for Data Analyst to analyze the data.

# Great Expectation

> Notes: Great Expectation Using Data that has been cleaned by Data Pipeline

1. Year Column Not Null(result:success)
2. Teritory Column Not Null(result:success)
3. Power_Spec Column Must be Integer(result:success)
4. Power_Needed Column Must be Integer(result:success)
5. Kwh_Needed Column Must be Number(result:success)
6. Megawatt_Capacity Column Must be Number(result:success)
