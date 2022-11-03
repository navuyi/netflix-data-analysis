import datetime
import time

from assessment_data import assessment_data
from text_colours import colours_ids


def mean_time():
    fields = ['id', 'started', 'timestamp', 'duration']

    assessment = assessment_data(fields)
    avenge = 0

    for first_time, second_time in zip(assessment[0:19], assessment[1:20]):
        first_timestamp = time.mktime(datetime.datetime.strptime(first_time['started'],
                                                                 "%Y-%m-%dT%H:%M:%S.%f").timetuple())
        second_timestamp = time.mktime(datetime.datetime.strptime(second_time['timestamp'],
                                                                  "%Y-%m-%dT%H:%M:%S.%f").timetuple())
        avenge += first_timestamp - second_timestamp

    avenge = float(avenge) / (len(assessment) - 1)

    raw = f"Średni czas między ekranami ankiety: " \
          f"{int(avenge // 60)}m {int(avenge - (avenge // 60 * 60))}s"

    formatted = f"{colours_ids.UNDERLINE}Średni czas między ekranami ankiety:{colours_ids.END}" \
                f"{colours_ids.OK_GREEN if 2.0 < avenge / 60 < 3.0 else colours_ids.FAIL}" \
                f" {int(avenge // 60)}m {int(avenge - (avenge // 60 * 60))}s{colours_ids.END}"

    return [raw, formatted]
