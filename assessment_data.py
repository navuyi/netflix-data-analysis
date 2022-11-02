from __config__ import TESTER_ID
from sql import sql


def assessment_data(fields):
    response = []

    fields_string = f'assessment.' + f', assessment.'.join([str(elem) for elem in fields])

    sql_request = f"select {fields_string} from assessment " \
                  f"inner join experiment " \
                  f"on assessment.video_id = experiment.id " \
                  f"where experiment.tester_id=='{TESTER_ID}'"

    data = sql(sql_request)

    for data in data:
        row = {}
        for (field, value) in zip(fields, data):
            row[field] = value
        response.append(row)

    response.reverse()

    return response
