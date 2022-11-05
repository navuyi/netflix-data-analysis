import sqlite3

conn = sqlite3.connect('db/imdb-data.db')
c = conn.cursor()


def select(title):
    result = []
    c.execute(
        f"select titleId, title, startYear, runtimeMinutes, genres "
        f"from akas inner join basic on akas.titleId = basic.tconst "
        f"where title like '{title}'")
    for record in c.fetchall():
        result.append({
            'titleId': record[0],
            'title': record[1],
            'startYear': record[2],
            'runtimeMinutes': record[3],
            'genres': record[4]
        })

    return result


print(select('wielka woda'))
