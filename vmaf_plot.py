import json

import matplotlib.pyplot as plt
import numpy as np

from __config__ import TESTER_ID
from sql import sql


def vmaf_buff_histogram():
    sql_request = f"select playback_data.buffering_vmaf from playback_data " \
                  f"inner join experiment " \
                  f"on playback_data.video_id = experiment.id " \
                  f"where experiment.tester_id=='{TESTER_ID}' " \
                  f"and playback_data.rendering_state=='Playing' "

    data = sql(sql_request)
    x_values = np.arange(0, len(data), 1)
    y_values = [int(data[value][0]) for value in x_values]

    return [x_values, y_values]


def vmaf_real_histogram():
    sql_request = f"select playback_data.playing_vmaf from playback_data " \
                  f"inner join experiment " \
                  f"on playback_data.video_id = experiment.id " \
                  f"where experiment.tester_id=='{TESTER_ID}' " \
                  f"and playback_data.rendering_state=='Playing' "

    data = sql(sql_request)
    x_values = np.arange(0, len(data), 1)
    y_values = [int(data[value][0]) for value in x_values]

    return [x_values, y_values]


def vmaf_scenario_and_diff_histogram():
    sql_request = (f"select configuration from experiment "
                   f"where experiment.tester_id=='{TESTER_ID}'")

    data = sql(sql_request)
    configuration = json.loads(data[0][0])
    interval = configuration['assessment_interval']

    x_values = np.arange(0, (len(configuration['videos'][0]['scenario'])) * interval, 150)
    y_values_template = [configuration['videos'][0]['scenario'][int(value / interval)]['vmaf_template']
                         for value in x_values]
    y_values_scenario = [configuration['videos'][0]['scenario'][int(value / interval)]['vmaf'] for value in x_values]
    y_values_diff = [configuration['videos'][0]['scenario'][int(value / interval)]['vmaf_diff'] for value in x_values]

    return [x_values, y_values_template, y_values_scenario, y_values_diff]


def vmaf_plot():
    scenario_vmaf = vmaf_scenario_and_diff_histogram()
    real_vmaf = vmaf_real_histogram()
    buff_vmaf = vmaf_buff_histogram()

    ax1 = plt.subplot(411)
    plt.step(scenario_vmaf[0], scenario_vmaf[1], 'r', where='post')

    if int(buff_vmaf[0][-1]) > int(scenario_vmaf[0][-1]):
        plt.axis([0, buff_vmaf[0][-1], 0, 105])
        plt.xticks(np.arange(0, buff_vmaf[0][-1] + 150, 150))
    else:
        plt.axis([0, scenario_vmaf[0][-1], 0, 110])
        plt.xticks(np.arange(0, scenario_vmaf[0][-1] + 150, 150))

    plt.yticks(np.arange(0, 101, 20))

    plt.title('VMAF template', fontsize=10)
    plt.xlabel('video duration')
    plt.ylabel('VMAF')

    plt.subplot(412, sharex=ax1, sharey=ax1)
    plt.step(scenario_vmaf[0], scenario_vmaf[2], 'y', where='post')

    plt.title('VMAF scenario', fontsize=10)
    plt.xlabel('video duration')
    plt.ylabel('VMAF')

    plt.subplot(413, sharex=ax1, sharey=ax1)
    plt.step(real_vmaf[0], real_vmaf[1], 'g', where='post')

    plt.title('Real VMAF', fontsize=10)
    plt.xlabel('video duration')
    plt.ylabel('VMAF')

    plt.subplot(414, sharex=ax1, sharey=ax1)
    plt.step(buff_vmaf[0], buff_vmaf[1], 'b', where='post')

    plt.title('Buffering VMAF', fontsize=10)
    plt.xlabel('video duration')
    plt.ylabel('VMAF')

    plt.gcf().set_size_inches(6, 8)
    plt.tight_layout()

    return plt
