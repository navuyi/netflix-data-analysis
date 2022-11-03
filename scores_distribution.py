import text_colours
from assessment_data import assessment_data
import matplotlib.pyplot as plt
import numpy as np

fields = ['id', 'value']
names = {5: 'excellent', 4: 'good', 3: 'average', 2: 'poor', 1: 'bad'}


def scores_distribution():
    distribution = {'bad': 0, 'poor': 0, 'average': 0, 'good': 0, 'excellent': 0}
    data = assessment_data(fields)

    for data in data:
        distribution[names[data['value']]] += 1

    fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')

    ax.bar([name for name, item in distribution.items()], np.array([item for name, item in distribution.items()]))

    plt.yticks(np.arange(0, 6, 1))
    plt.title('Score distribution', fontsize=10)
    plt.ylabel('Score')

    return fig
