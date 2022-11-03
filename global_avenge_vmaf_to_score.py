import os
import sqlite3

import matplotlib.pyplot as plt

from __config__ import DATABASES_DIR


def sql(request, database):
    response = []

    database.execute(request)

    for rows in database.fetchall():
        response.append(rows)

    return response


def global_avenge_vmaf_to_score():
    db_names = os.listdir(f"./{DATABASES_DIR}")
    data = []

    for db_name in db_names:
        conn = sqlite3.connect(f"{DATABASES_DIR}/{db_name}")
        connection = conn.cursor()

        sql_request = f"select assessment.started, assessment.timestamp, assessment.value " \
                      f"from assessment "

        assessment = []
        sql_response = sql(sql_request, connection)

        for values in sql_response:
            row = {}
            for (field, value) in zip(['started', 'timestamp', 'value'], values):
                row[field] = value
            assessment.append(row)

        sql_request = f"select avg(playback_data.playing_vmaf) from playback_data " \
                      f"where playback_data.rendering_state=='Playing' " \
                      f"and playback_data.timestamp < '{assessment[0]['started']}'"

        data.append({"avg_vmaf": sql(sql_request, connection)[0][0], "score": assessment[0]['value']})

        for (finish, start) in zip(assessment[1:len(assessment)], assessment[0:len(assessment) - 1]):
            sql_request = f"select avg(playback_data.playing_vmaf) from playback_data " \
                          f"where playback_data.rendering_state=='Playing' " \
                          f"and playback_data.timestamp between '{start['timestamp']}' AND '{finish['started']}'"

            data.append({"avg_vmaf": sql(sql_request, connection)[0][0], "score": finish['value']})

        conn.close()

    x = []
    y = []

    for value in data:
        x.append(value['avg_vmaf'])
        y.append(value['score'])

    fig3, ax3 = plt.subplots()

    ax3.plot(x, y, 'ro')
    ax3.axis([0, 100, 0, 5])

    ax3.set_title('Global avenge VMAF to score', fontsize=10)
    ax3.set_xlabel('VMAF')
    ax3.set_ylabel('User score')

    return fig3
