from __config__ import CONNECTION


def sql(sql_request):
    response = []

    CONNECTION.execute(sql_request)

    for data in CONNECTION.fetchall():
        response.append(data)

    return response
