import json

from __config__ import TESTER_ID
from sql import sql
from text_colours import colours_ids


def extract_scenario():
    sql_request = (f"select configuration from experiment "
                   f"where experiment.tester_id=='{TESTER_ID}'")

    configuration = json.loads(sql(sql_request)[0][0])

    raw = f"Scenariusz: {configuration['videos'][0]['vmaf_template_scenario']}"

    formatted = f"{colours_ids.UNDERLINE}Scenariusz:{colours_ids.END} " \
                f"{configuration['videos'][0]['vmaf_template_scenario']}"

    return [raw, formatted]
