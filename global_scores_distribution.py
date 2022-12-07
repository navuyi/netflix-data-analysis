import sqlite3

import matplotlib.pyplot as plt
import numpy as np

from __config__ import DATABASES_DIR, DB_NAMES

fields = ['id', 'value']
names = {5: 'excellent', 4: 'good', 3: 'average', 2: 'poor', 1: 'bad'}


def sql(request, database):
    response = []

    database.execute(request)

    for rows in database.fetchall():
        response.append(rows)

    return response


def global_scores_distribution():
    distribution = {'bad': 0, 'poor': 0, 'average': 0, 'good': 0, 'excellent': 0}

    for db_name in DB_NAMES:
        conn = sqlite3.connect(f"{DATABASES_DIR}/{db_name}")
        connection = conn.cursor()

        sql_request = f"select value from assessment"

        sql_response = sql(sql_request, connection)

        for values in sql_response:
            for value in values:
                distribution[names[value]] += 1

        conn.close()

    fig4, ax4 = plt.subplots(figsize=(5, 2.7), layout='constrained')

    ax4.bar([name for name, item in distribution.items()], np.array([item for name, item in distribution.items()]))

    ax4.set_title(f'Global score distribution', fontsize=10)
    ax4.set_ylabel('Score')

    return fig4
