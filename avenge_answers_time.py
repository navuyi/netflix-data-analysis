from __config__ import TESTER_ID
from sql import sql
from text_colours import colours_ids


def avenge_answers_time():
    sql_request = f"select avg(duration) from assessment " \
                  f"inner join experiment " \
                  f"on assessment.video_id = experiment.id " \
                  f"where experiment.tester_id=='{TESTER_ID}'"

    avenge = sql(sql_request)[0][0]

    raw = f"Średni czas odpowiedzi: " \
          f"{format(float(avenge) / 1000, '.2f')}s"
    formatted = f"{colours_ids.UNDERLINE}Średni czas odpowiedzi:{colours_ids.END}" \
                f"{colours_ids.OK_GREEN if 1000 < avenge < 30000 else colours_ids.FAIL}" \
                f" {format(float(avenge) / 1000, '.2f')}s{colours_ids.END}"

    return [raw, formatted]
