import sqlite3
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np

from __config__ import DATABASES_DIR, DB_NAMES


def sql(request, database):
    response = []

    database.execute(request)

    for rows in database.fetchall():
        response.append(rows)

    return response


def global_average_vmaf_to_score(scope):
    vmaf_to_score = []

    for db_name in DB_NAMES:
        conn = sqlite3.connect(f"{DATABASES_DIR}/{db_name}")
        connection = conn.cursor()

        sql_request = f"select assessment.timestamp, assessment.value " \
                      f"from assessment "

        assessment = []
        sql_response = sql(sql_request, connection)

        for values in sql_response:
            row = {}
            for (field, value) in zip(['timestamp', 'value'], values):
                row[field] = value
            assessment.append(row)

        for timestamp in assessment:
            date = datetime.strptime(timestamp['timestamp'], "%Y-%m-%dT%H:%M:%S.%f") - timedelta(seconds=scope)
            start = date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]

            sql_request = f"select avg(playback_data.playing_vmaf) from playback_data " \
                          f"where playback_data.rendering_state=='Playing' " \
                          f"and playback_data.timestamp between '{start}' and '{timestamp['timestamp']}'"

            vmaf_to_score.append({"avg_vmaf": sql(sql_request, connection)[0][0], "score": timestamp['value']})

        conn.close()

    x = []
    y = []

    for value in vmaf_to_score:
        x.append(value['avg_vmaf'])
        y.append(value['score'])

    fig3, ax3 = plt.subplots()

    ax3.plot(x, y, 'ro')
    ax3.axis([20, 100, 1, 5])
    ax3.set_yticks(np.arange(1, 6, 1))

    ax3.set_title(f'Global average VMAF to score \u0394t={scope}s', fontsize=10)
    ax3.set_xlabel('VMAF')
    ax3.set_ylabel('Users score')

    return fig3
