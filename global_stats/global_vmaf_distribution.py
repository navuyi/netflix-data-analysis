import matplotlib.pyplot as plt
import numpy as np

from __config__ import TESTERS_ID
from extract_scenario import extract_scenario
from vmaf_plot import vmaf_scenario_and_diff_histogram


def vmaf_distribution_from_scenario():
    used_scenarios = []
    distribution = {
        '20': 0, '30': 0, '40': 0,
        '50': 0, '60': 0, '70': 0,
        '80': 0, '90': 0, '100': 0,
    }

    for TESTER_ID in TESTERS_ID:
        used_scenarios.append(extract_scenario(TESTER_ID)[3])

    for scenario in used_scenarios:
        for vmaf in scenario:
            distribution[str(vmaf)] += 1

    return distribution


def real_vmaf_distribution():
    used_vmafs = []
    distribution = {
        '20': 0, '30': 0, '40': 0,
        '50': 0, '60': 0, '70': 0,
        '80': 0, '90': 0, '100': 0,
    }

    for TESTER_ID in TESTERS_ID:
        used_vmafs.append(vmaf_scenario_and_diff_histogram(TESTER_ID)[2])

    for real_vmafs in used_vmafs:
        for vmaf in real_vmafs:
            distribution[str(vmaf // 10 * 10)] += 1

    return distribution


def global_vmaf_distribution():
    scenario_vmaf = vmaf_distribution_from_scenario()
    real_vmaf = real_vmaf_distribution()

    fig6, (ax6a, ax6b) = plt.subplots(nrows=2, ncols=1, layout='constrained')

    ax6a.bar([name for name, item in scenario_vmaf.items()], np.array([item for name, item in scenario_vmaf.items()]))
    ax6a.set_yticks(np.arange(0, max(scenario_vmaf.values()) + 5, 5))

    ax6a.set_title(f'VMAF distribution from scenarios', fontsize=10)
    ax6a.set_ylabel('Frequency')

    ax6b.bar([name for name, item in real_vmaf.items()], np.array([item for name, item in real_vmaf.items()]))
    ax6b.set_yticks(np.arange(0, max(real_vmaf.values()) + 5, 5))

    ax6b.set_title(f'Real VMAF distribution', fontsize=10)
    ax6b.set_ylabel('Frequency')

    return fig6
