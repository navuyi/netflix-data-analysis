import text_colours
from assessment_data import assessment_data

fields = ['id', 'value']
names = {5: 'excellent', 4: 'good', 3: 'average', 2: 'poor', 1: 'bad'}


def scores_distribution():
    distribution = {'excellent': 0, 'good': 0, 'average': 0, 'poor': 0, 'bad': 0}
    data = assessment_data(fields)

    for data in data:
        distribution[names[data['value']]] += 1

    return (f"{text_colours.colours_ids.UNDERLINE}Rozkład odpowiedzi w ankietach:{text_colours.colours_ids.END}\n"
            f"Doskonała: {distribution['excellent']}\n"
            f"Dobra: {distribution['good']}\n"
            f"Średnia: {distribution['average']}\n"
            f"Niska: {distribution['poor']}\n"
            f"Zła: {distribution['bad']}")
