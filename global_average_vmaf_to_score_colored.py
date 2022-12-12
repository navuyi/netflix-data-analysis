import sqlite3

import matplotlib.pyplot as plt
import numpy as np

from __config__ import DATABASES_DIR, DB_NAMES


def sql(request, database):
    response = []

    database.execute(request)

    for rows in database.fetchall():
        response.append(rows)

    return response


def global_average_vmaf_to_score_colored():
    x = []
    y = []

    for db_name in DB_NAMES:
        conn = sqlite3.connect(f"{DATABASES_DIR}/{db_name}")
        connection = conn.cursor()

        ids = sql("select id from experiment", connection)

        for video_id in ids:
            vmaf_to_score = []
            assessment = []

            sql_request = f"select assessment.started, assessment.timestamp, assessment.value " \
                          f"from assessment " \
                          f"where video_id == {video_id[0]}"

            sql_response = sql(sql_request, connection)

            for values in sql_response:
                row = {}
                for (field, value) in zip(['started', 'timestamp', 'value'], values):
                    row[field] = value
                assessment.append(row)

            sql_request = f"select avg(playback_data.playing_vmaf) from playback_data " \
                          f"where playback_data.rendering_state=='Playing' " \
                          f"and playback_data.timestamp < '{assessment[0]['started']}' " \
                          f"and video_id == {video_id[0]}"

            vmaf_to_score.append({"avg_vmaf": sql(sql_request, connection)[0][0], "score": assessment[0]['value']})

            for (finish, start) in zip(assessment[1:len(assessment)], assessment[0:len(assessment) - 1]):
                sql_request = f"select avg(playback_data.playing_vmaf) from playback_data " \
                              f"where playback_data.rendering_state=='Playing' " \
                              f"and playback_data.timestamp between '{start['timestamp']}' and '{finish['started']}' " \
                              f"and video_id == {video_id[0]}"

                vmaf_to_score.append({"avg_vmaf": sql(sql_request, connection)[0][0], "score": finish['value']})

            temp_x = []
            temp_y = []

            for value in vmaf_to_score:
                temp_x.append(value['avg_vmaf'])
                temp_y.append(value['score'])

            x.append(temp_x.copy())
            y.append(temp_y.copy())

        conn.close()

    fig3, ax3 = plt.subplots()

    plots = []

    for (x_values, y_values, color) in zip(x, y, ['ro', 'go', 'bo', 'co', 'mo', 'yo', 'ko']):
        plots.append([x_values, y_values, color])

    for plot in plots:
        ax3.plot(plot[0], plot[1], plot[2])

    ax3.axis([20, 100, 1, 5])
    ax3.set_yticks(np.arange(1, 6, 1))

    ax3.set_title('Global average VMAF to score', fontsize=10)
    ax3.set_xlabel('VMAF')
    ax3.set_ylabel('User score')

    return fig3


global_average_vmaf_to_score_colored().savefig(f"./output/global_average_vmaf_to_score_colored")
