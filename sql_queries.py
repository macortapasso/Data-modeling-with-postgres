# DROP TABLES

songplay_table_drop = "drop table if exists songplays"
user_table_drop = "drop table if exists users"
song_table_drop = "drop table if exists songs"
artist_table_drop = "drop table if exists artists"
time_table_drop = "drop table if exists time"

# CREATE TABLES

songplay_table_create = (""" create table songplays
                        ( songplay_id serial primary key not null
                        , start_time timestamp
                        , user_id int
                        , level varchar
                        , song_id int
                        , artist_id int
                        , session_id int
                        , location varchar
                        , user_agent varchar
                        )
                        """)

user_table_create = ("""create table users
                    ( user_id int primary key not null
                    , first_name varchar
                    , last_name varchar
                    , gender varchar
                    , level varchar
                    )
                       """)

song_table_create = ("""create table songs
                        ( song_id varchar primary key not null
                        , title varchar
                        , artist_id varchar
                        , year int
                        , duration real
                        )
                    """)

artist_table_create = ("""
                        create table artists
                        ( artist_id varchar primary key not null
                        , name varchar
                        , location varchar
                        , latitude real
                        , longitude real
                        )
                        """)

time_table_create = ("""
                        create table time
                        ( start_time timestamp
                        , hour int
                        , day int
                        , week int
                        , month int
                        , year int
                        , weekday int
                        )
                        """)

# INSERT RECORDS

songplay_table_insert = (""" insert into songplays ( start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) values(%s,%s,%s,%s,%s,%s,%s,%s)   """)

user_table_insert = (""" insert into users ( user_id, first_name, last_name, gender, level) values (%s,%s,%s,%s,%s) on conflict (user_id) do nothing;   """)

song_table_insert = (""" insert into songs (song_id, title, artist_id, year, duration) values (%s,%s,%s,%s,%s) on conflict (song_id) do nothing""")

artist_table_insert = (""" insert into artists ( artist_id, name, location, latitude, longitude) values (%s,%s,%s,%s,%s) on conflict (artist_id) do nothing""")

time_table_insert = (""" insert into time ( start_time , hour, day , week, month, year, weekday) values(%s,%s,%s,%s,%s,%s,%s) """)

# FIND SONGS

song_select = (""" select   son.song_id
                            , son.title
                            , son.duration
                            , art.artist_id
                            , art.name
                            
                    from  songs son
                    
                    left join artists art
                    on son.artist_id = art.artist_id
                    
                    where
                        1 = 1
                        and son.title = %s
                        and art.name = %s
                        and son.duration = %s
                    """)

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]