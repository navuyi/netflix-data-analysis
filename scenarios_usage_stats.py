import matplotlib.pyplot as plt
import numpy as np

from __config__ import TESTERS_ID
from extract_scenario import extract_scenario
from sql import sql


def scenarios_usage_stats():
    distribution = {
        'sc_20_01': 0, 'sc_20_02': 0, 'sc_20_03': 0,
        'sc_30_01': 0, 'sc_30_02': 0, 'sc_30_03': 0,
        'sc_40_01': 0, 'sc_40_02': 0, 'sc_40_03': 0,
        'sc_60_01': 0, 'sc_60_02': 0, 'sc_60_03': 0
    }

    for TESTER_ID in TESTERS_ID:
        sql_request = f"select video.video_index from video " \
                      f"inner join experiment " \
                      f"on video.experiment_id = experiment.id " \
                      f"where experiment.tester_id == '{TESTER_ID}'"

        video_indexes = sql(sql_request)

        for video in video_indexes:
            distribution[extract_scenario(TESTER_ID, video[0])[2]] += 1

    fig5, ax5 = plt.subplots(figsize=(10, 2.7), layout='constrained')

    ax5.bar([name for name, item in distribution.items()], np.array([item for name, item in distribution.items()]))

    ax5.set_title(f'Scenario usage stats', fontsize=10)
    ax5.set_ylabel('Frequency')

    return fig5
