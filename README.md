# **Data Modeling with Postgres**


## **Purpose of database**

This project aims to model a database for the startup Sparkify that provides a music stream.

It is used the star schema to organize the information that is distributed among multiples json files. The ETL process involves accessing each file, reading them, and writing pieces of information in each table that represent the fact and dimensions. This database design facilitates that Sparkify develops analytics studies that were not possible in distributed json files.


## **Dataset**

### Song Dataset
Songs dataset is a subset of [Million Song Dataset](http://millionsongdataset.com/).

Sample Record :
```
{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
```

### Log Dataset

Log of all songs played in the app in a defined period.

Sample Record :
```
{"artist": null, "auth": "Logged In", "firstName": "Walter", "gender": "M", "itemInSession": 0, "lastName": "Frye", "length": null, "level": "free", "location": "San Francisco-Oakland-Hayward, CA", "method": "GET","page": "Home", "registration": 1540919166796.0, "sessionId": 38, "song": null, "status": 200, "ts": 1541105830796, "userAgent": "\"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"", "userId": "39"}
```


## **Database schema**

It was chosen the Star Schema that has the songplays as fact table, and the dimensions are represented by the tables users, songs, artists, and time.

### Fact Table 
**songplays** - records in log data associated with song plays. All records refers to the page 'NextSong'.

```
songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
```

###  Dimension Tables
**users**  - users in the app
```
user_id, first_name, last_name, gender, level
```
**songs**  - songs in music database
```
song_id, title, artist_id, year, duration
```
**artists**  - artists in music database
```
artist_id, name, location, latitude, longitude
```
**time**  - timestamps of records
```
start_time, hour, day, week, month, year, weekday
```


## **ETL pipeline**

```sql_queries.py``` : support file that contains sql queries to create and drop tables. The insert commands that are used to ETL process is also written in it.

```create_tables.py``` : the inicial set up for the Postgress database. It creates **sparkifydb** and the fact and dimension tables.

```etl.ipynb``` : notebook used to analyse how the etl.py would be developed. 

```etl.py``` : process **song_data** and **log_data** according to the steps present in the etl.ipynb.

```test.ipynb``` : a notebook to validate the data loaded.


## **How to run**

First, run the script ```create_tables.py``` that creates the database and tables at the Postgres. It is necessary to have the Postgres installed and the credencials users and password updated on this script.

Finally, run the ```etl.py``` that process all log and song data from the data directory. The process involves read all files, split the information according to the database schema explained above, and insert it into each table.



 
