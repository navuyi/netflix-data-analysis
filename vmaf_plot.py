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

    fig1, (ax1a, ax1b, ax1c, ax1d) = plt.subplots(nrows=4, ncols=1, sharex='all', sharey='all')

    ax1a.plot(411)
    ax1a.step(scenario_vmaf[0], scenario_vmaf[1], 'r', where='post')

    if int(buff_vmaf[0][-1]) > int(scenario_vmaf[0][-1]):
        ax1a.axis([0, buff_vmaf[0][-1], 0, 105])
        ax1a.set_xticks(np.arange(0, buff_vmaf[0][-1] + 150, 300))
    else:
        ax1a.axis([0, scenario_vmaf[0][-1], 0, 110])
        ax1a.set_xticks(np.arange(0, scenario_vmaf[0][-1] + 150, 150))

    ax1a.set_yticks(np.arange(0, 101, 20))

    ax1a.set_title(f'VMAF template {TESTER_ID}', fontsize=10)
    ax1a.set_xlabel('video duration')
    ax1a.set_ylabel('VMAF')

    ax1b.plot(412)
    ax1b.step(scenario_vmaf[0], scenario_vmaf[2], 'y', where='post')

    ax1b.set_title(f'VMAF scenario {TESTER_ID}', fontsize=10)
    ax1b.set_xlabel('video duration')
    ax1b.set_ylabel('VMAF')

    ax1c.plot(413)
    ax1c.step(real_vmaf[0], real_vmaf[1], 'g', where='post')

    ax1c.set_title(f'VMAF played {TESTER_ID}', fontsize=10)
    ax1c.set_xlabel('video duration')
    ax1c.set_ylabel('VMAF')

    ax1d.plot(414)
    ax1d.step(buff_vmaf[0], buff_vmaf[1], 'b', where='post')

    ax1d.set_title(f'VMAF buffered {TESTER_ID}', fontsize=10)
    ax1d.set_xlabel('video duration')
    ax1d.set_ylabel('VMAF')

    fig1.set_size_inches(6, 8)
    fig1.tight_layout()

    return fig1
