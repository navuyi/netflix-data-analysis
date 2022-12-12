from sql import sql
from text_colours import colours_ids


def average_answers_time(video_id):
    sql_request = f"select avg(duration) from assessment " \
                  f"inner join video " \
                  f"on assessment.video_id = video.id " \
                  f"where video.id=='{video_id}'"

    average = sql(sql_request)[0][0]

    raw = f"Średni czas odpowiedzi: " \
          f"{format(float(average) / 1000, '.2f')}s"
    formatted = f"{colours_ids.UNDERLINE}Średni czas odpowiedzi:{colours_ids.END}" \
                f"{colours_ids.OK_GREEN if 1000 < average < 30000 else colours_ids.FAIL}" \
                f" {format(float(average) / 1000, '.2f')}s{colours_ids.END}"

    return [raw, formatted]
