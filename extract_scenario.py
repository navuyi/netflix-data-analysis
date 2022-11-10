import json

from sql import sql
from text_colours import colours_ids


def extract_scenario(TESTER_ID):
    sql_request = (f"select configuration from experiment "
                   f"where experiment.tester_id=='{TESTER_ID}'")
    scenarios_json = open('important_files/scenarios.json')

    configuration = json.loads(sql(sql_request)[0][0])
    current_scenario = configuration['videos'][0]['vmaf_template_scenario']
    current_scenario_symbol = ''
    scenarios = json.load(scenarios_json)

    for scenario_symbol in scenarios:
        if scenarios[scenario_symbol] == current_scenario:
            current_scenario_symbol += scenario_symbol
            break

    raw = f"Scenariusz: {current_scenario}"

    formatted = f"{colours_ids.UNDERLINE}Scenariusz:{colours_ids.END} " \
                f"{current_scenario}"

    return [raw, formatted, current_scenario_symbol, current_scenario]
