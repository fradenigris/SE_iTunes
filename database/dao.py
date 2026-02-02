from database.DB_connect import DBConnect
from model.album import Album
from model.playlist import Playlist

class DAO:
    @staticmethod
    def get_album(minuti):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT a.id, a.title, a.artist_id, SUM(t.milliseconds) as durata
                    FROM album a, track t
                    WHERE a.id = t.album_id
                    GROUP BY a.id, a.title, a.artist_id
                    HAVING durata > %s """

        cursor.execute(query, (minuti,))

        for row in cursor:
            result.append(Album(
                id=row['id'],
                title=row['title'],
                artist_id=row['artist_id'],
                durata=(row['durata'] / 60000)
            ))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_tracks_for_each_album(album_id):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT t.id
                    FROM track t
                    WHERE t.album_id = %s """

        cursor.execute(query, (album_id,))

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_all_playlist():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT *
                    FROM playlist """

        cursor.execute(query)

        for row in cursor:
            result.append(Playlist(
                id=row['id'],
                name=row['name']
            ))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_tracks_for_each_playlist(playlist_id):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT track_id
                    FROM playlist_track
                    WHERE playlist_id = %s """

        cursor.execute(query, (playlist_id,))

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result