import os
import glob
import warnings
import psycopg2
import pandas as pd
from sql_queries import song_table_insert, artist_table_insert,  \
                        time_table_insert, user_table_insert, \
                        songplay_table_insert, song_select


warnings.filterwarnings("ignore")


def process_song_file(cur, filepath):
    """
    Process an unique the json song file and insert the data into the database.

    parameters:
        cur(cursor): cursor to execute queries
        filepath(str): path to access the json file
    """

    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df.loc[0, ['song_id', 'title',
                           'artist_id', 'year', 'duration']].values.tolist()
    song_data = [float(elem) if type(
        elem) is not str else elem for elem in song_data]
    cur.execute(song_table_insert, song_data)

    # insert artist record
    artist_data = df.loc[0, ['artist_id', 'artist_name',
                            'artist_location', 'artist_latitude',
                            'artist_longitude']].values.tolist()
    artist_data = [float(elem) if type(elem) is not str else elem for elem in artist_data]
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Process an unique the json log file and insert the data into the database.

    parameters:
        cur(cursor): cursor to execute queries
        filepath(str): path to access the json file
    """

    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.loc[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    t = df['ts'].copy()
    t['ts'] = pd.to_datetime(df['ts'], unit='ms')

    # insert time data records
    time_data = (t['ts'], t['ts'].dt.hour, t['ts'].dt.day,
                t['ts'].dt.week, t['ts'].dt.month,
                t['ts'].dt.year, t['ts'].dt.dayofweek)

    column_labels = ('start_time', 'hour', 'day',
                    'week', 'month', 'year', 'weekday')

    date_dict = {}
    for serie, name in zip(time_data, column_labels):
        date_dict[name] = serie
    time_df = pd.DataFrame.from_dict(date_dict)

    for _, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df.loc[:, ['userId', 'firstName', 'lastName',
                         'gender', 'level']].drop_duplicates(subset=['userId'])

    # insert user records
    for _, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for _, row in df.iterrows():

        # get songid and artistid from song and artist tables
        results = cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        songid, artistid = results if results else None, None

        # insert songplay record
        songplay_data = (pd.Timestamp(row.ts, unit='ms'), row.userId,
                        row.level, songid, artistid, row.sessionId,
                        row.location, row.userAgent)

        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Access all files from defined path and process the files
    according to the func.

    parameters:
        cur(cursor): cursor to execute queries.
        conn(connection): database connection.
        filepath(str): path to walk and access all files.
        func(function): process function to treat the files.
    """

    # get all files matching extension from directory
    all_files = []
    for root, _, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for file in files:
            all_files.append(os.path.abspath(file))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    Process the ETL for data song and log data
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=postgres \
                            password=1234")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
