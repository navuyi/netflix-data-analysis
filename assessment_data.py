from sql import sql


def assessment_data(fields, video_id):
    response = []

    fields_string = f'assessment.' + f', assessment.'.join([str(elem) for elem in fields])

    sql_request = f"select {fields_string} from assessment " \
                  f"inner join video " \
                  f"on assessment.video_id = video.id " \
                  f"where video.id =='{video_id}'"

    data = sql(sql_request)

    for data in data:
        row = {}
        for (field, value) in zip(fields, data):
            row[field] = value
        response.append(row)

    response.reverse()

    return response
