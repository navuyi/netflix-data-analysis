import matplotlib.pyplot as plt

from __config__ import TESTER_ID
from sql import sql

sql_request = f"select assessment.started, assessment.timestamp, assessment.value " \
              f"from assessment " \
              f"inner join experiment " \
              f"on assessment.video_id = experiment.id " \
              f"where experiment.tester_id=='{TESTER_ID}'"

assessment = []
data = []
response = sql(sql_request)

for values in response:
    row = {}
    for (field, value) in zip(['started', 'timestamp', 'value'], values):
        row[field] = value
    assessment.append(row)

sql_request = f"select avg(playback_data.playing_vmaf) from playback_data " \
              f"inner join experiment " \
              f"on playback_data.video_id = experiment.id " \
              f"where experiment.tester_id=='{TESTER_ID}' " \
              f"and playback_data.rendering_state=='Playing' " \
              f"and playback_data.timestamp < '{assessment[0]['started']}'"

data.append({"avg_vmaf": sql(sql_request)[0][0], "score": assessment[0]['value']})

for (finish, start) in zip(assessment[1:len(assessment)], assessment[0:len(assessment) - 1]):
    sql_request = f"select avg(playback_data.playing_vmaf) from playback_data " \
                  f"inner join experiment " \
                  f"on playback_data.video_id = experiment.id " \
                  f"where experiment.tester_id=='{TESTER_ID}' " \
                  f"and playback_data.rendering_state=='Playing' " \
                  f"and playback_data.timestamp between '{start['timestamp']}' AND '{finish['started']}'"

    data.append({"avg_vmaf": sql(sql_request)[0][0], "score": finish['value']})

x = []
y = []
for value in data:
    x.append(value['avg_vmaf'])
    y.append(value['score'])

plt.plot(x, y, 'ro')
plt.axis([0, 100, 0, 5])
plt.xlabel('VMAF')
plt.ylabel('User score')
plt.show()
