import csv
import sqlite3
import os
from config import DATABASES_DIR
from config import CSV_DIR

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def db_connect(database):
    conn = sqlite3.connect(database)
    conn.row_factory = dict_factory
    conn.isolation_level = None  # <-- Auto commit

    cursor = conn.cursor()
    return conn, cursor


def get_databases():
    entry = os.listdir(DATABASES_DIR)
    files = []
    for file in entry:
        if file.endswith(".db"):
            files.append(file)
        else:
            pass
    return files


def main():
    databases = get_databases()
    

    for database in databases:

        conn, cursor = db_connect(os.path.join(DATABASES_DIR, database))
        cursor.execute("SELECT * FROM video")
        videos = cursor.fetchall()

        for video in videos:
            # Get video's experiment data
            cursor.execute(f"SELECT id, tester_id, experiment_type FROM experiment WHERE id={video['experiment_id']}")
            exp_data = cursor.fetchall()[0]

            csv_filename = f"{exp_data['tester_id']}_{exp_data['experiment_type']}_expID_{exp_data['id']}_videoID_{video['id']}.csv"

            # Get video playback data
            cursor.execute(f"SELECT * FROM playback_data WHERE video_id={video['id']}")
            playback_data = cursor.fetchall()
            playback_data_keys = playback_data[0].keys()
            playback_data_values = [row.values() for row in playback_data]


            # Get assessments for video
            cursor.execute(f"SELECT * FROM assessment WHERE video_id={video['id']} ORDER BY id")
            assessments = cursor.fetchall()
            assessment_keys = None
            assessment_values = None

            if len(assessments) == 0:
                print(f"Assessments is empty for video ID: {video['id']}")
                keys = playback_data_keys
                values = playback_data_values
            else:
                assessment_keys = ["assessment_"+key for key in assessments[0].keys()]
                assessment_values = [row.values() for row in assessments]
                keys = list(playback_data_keys) + list(assessment_keys)
                values = list(playback_data_values)

                # Merge values from assessments and playback data
                for index, row in enumerate(assessment_values):
                    values[index] = list(values[index]) + list(row)


            with open(os.path.join(CSV_DIR, csv_filename), "w", encoding="UTF8", newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(keys)
                    writer.writerows(values)




if __name__ == "__main__":
    main()
