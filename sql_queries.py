# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""
    CREATE TABLE songplays
    (songplay_id serial primary key, 
    start_time timestamp not null, 
    user_id int not null,
    level varchar,
    song_id int,
    artist_id int,
    session_id int,
    location varchar,
    user_agent varchar)
""")

user_table_create = ("""
    CREATE TABLE users
    (user_id int primary key,
    first_name varchar not null,
    last_name varchar not null,
    gender varchar,
    level varchar)
""")

song_table_create = ("""
    CREATE TABLE songs
    ( song_id varchar primary key,
    title varchar not null,
    artist_id varchar,
    year int,
    duration real)
""")

artist_table_create = ("""
    CREATE TABLE artists
    ( artist_id varchar primary key,
    name varchar,
    location varchar, 
    latitude real,
    longitude real)
""")

time_table_create = ("""
    CREATE TABLE time
    ( start_time timestamp primary key, 
    hour int not null,
    day int not null,
    week int not null,
    month int not null,
    year int not null,
    weekday int not null
    )
""")

# INSERT RECORDS

songplay_table_insert = ("""
    INSERT INTO songplays ( start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) 
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
""")

user_table_insert = ("""
    INSERT INTO users ( user_id, first_name, last_name, gender, level) 
    VALUES (%s,%s,%s,%s,%s)
    ON CONFLICT (user_id)
    DO UPDATE SET level = excluded.level;
""")

song_table_insert = ("""
    INSERT INTO songs (song_id, title, artist_id, year, duration) 
    VALUES (%s,%s,%s,%s,%s)
    ON CONFLICT (song_id)
    DO NOTHING
""")

artist_table_insert = (""" 
    INSERT INTO artists ( artist_id, name, location, latitude, longitude)
    VALUES (%s,%s,%s,%s,%s)
    ON CONFLICT (artist_id)
    DO NOTHING
""")

time_table_insert = ("""
    INSERT INTO time ( start_time , hour, day , week, month, year, weekday) 
    VALUES(%s,%s,%s,%s,%s,%s,%s)
    ON CONFLICT (start_time)
    DO NOTHING
""")

# FIND SONGS

song_select = ("""
    SELECT  son.song_id
            , art.artist_id               
    FROM  songs son
                    
    LEFT JOIN artists art
    ON son.artist_id = art.artist_id
                    
    WHERE
        son.title = %s
        AND art.name = %s
        AND son.duration = %s
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create,
                        song_table_create, artist_table_create,
                        time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
