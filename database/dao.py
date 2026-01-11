from database.DB_connect import DBConnect
from model.album import Album


class DAO:
    @staticmethod
    def get_album(durata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT a.id, a.title, a.artist_id, SUM(t.milliseconds)/60000 AS duration
                FROM album a, track t
                WHERE a.id = t.album_id
                GROUP BY a.id, a.title, a.artist_id
                HAVING duration > %s
                """

        cursor.execute(query, (durata,))

        for row in cursor:
            result.append(Album(row['id'], row['title'], row['artist_id'], row['duration']))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_connessioni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT t1.album_id AS a1, t2.album_id AS a2
                    FROM playlist_track pt1, playlist_track pt2, track t1, track t2
                    WHERE pt1.playlist_id = pt2.playlist_id and pt1.track_id = t1.id and pt2.track_id = t2.id and t1.album_id < t2.album_id
                    GROUP BY t1.album_id, t2.album_id """

        cursor.execute(query)

        for row in cursor:
            result.append((row['a1'],row['a2']))

        cursor.close()
        conn.close()
        return result



