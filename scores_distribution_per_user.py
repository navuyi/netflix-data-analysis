import matplotlib.pyplot as plt
import numpy as np

from __config__ import TESTER_ID
from assessment_data import assessment_data

fields = ['id', 'value']
names = {5: 'excellent', 4: 'good', 3: 'average', 2: 'poor', 1: 'bad'}


def scores_distribution_per_user():
    distribution = {'bad': 0, 'poor': 0, 'average': 0, 'good': 0, 'excellent': 0}
    data = assessment_data(fields)

    for data in data:
        distribution[names[data['value']]] += 1

    fig2, ax2 = plt.subplots(figsize=(5, 2.7), layout='constrained')

    ax2.bar([name for name, item in distribution.items()], np.array([item for name, item in distribution.items()]))

    ax2.set_title(f'Score distribution {TESTER_ID}', fontsize=10)
    ax2.set_ylabel('Score')

    return fig2
