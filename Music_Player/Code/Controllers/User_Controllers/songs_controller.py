from DB.database import Database

class SongsController:
    def __init__(self):
        self.db = Database()

    def get_all_songs(self):
        query = """
            SELECT 
                SONG.Song_id, 
                SONG.Title,
                SONG.ReleaseDate,
                SONG.Genre,
                Album.AbTitle, 
                ARTIST.AtName 
            FROM 
                SONG
            JOIN    
                ALBUM
            ON 
                SONG.Album = Album.Album_id
            JOIN
                ARTIST
            ON ALBUM.Artist = ARTIST.Artist_id
            """
        try:
            return self.db.execute_query(query)
        except Exception as e:
            print(f"DB에서 곡 목록을 불러오는 중 오류가 발생했습니다.: {e}")
            return []
        
    def get_liked_songs(self, user_id):
        query = """
            SELECT 
                SONG.Song_id,
                SONG.Title,
                SONG.ReleaseDate,
                SONG.Genre,
                Album.AbTitle,
                ARTIST.AtName
            FROM
                LIKES
            JOIN
                SONG
            ON  
                LIKES.LSong = SONG.Song_id
            JOIN 
                ALBUM
            ON 
                SONG.Album = ALBUM.Album_id
            JOIN
                ARTIST
            ON
                ALBUM.Artist = ARTIST.Artist_id
            WHERE 
                LIKES.Who = %s
        """
        try:
            return self.db.execute_query(query, (user_id))
        except Exception as e:
            print(f"좋아요 누른 곡을 불러오는 중 오류가 발생했습니다.: {e}")
            return []

        
    def increment_play_count(self, user_id, song_id):
        try:
            # 전체 재생 횟수 증가
            update_song_query = "UPDATE SONG SET PlayCount = PlayCount + 1 WHERE Song_id = %s"
            self.db.execute_query(update_song_query, (song_id))
            # 개인 재생 횟수 업데이트
            check_play_query = "SELECT Ppc FROM PLAY WHERE Who = %s AND PSong = %s"
            play_record = self.db.execute_query(check_play_query, (user_id, song_id))
            if play_record:
                # 이미 재생 기록이 있으면 
                update_play_query = "UPDATE PLAY SET Ppc = Ppc + 1, Lpd = NOW() WHERE Who = %s AND PSong = %s"
                self.db.execute_query(update_play_query, (user_id, song_id))
            else:
                # 재생 기록이 없는 경우
                insert_play_query = "INSERT INTO PLAY (Who, PSong, Ppc, Lpd) VALUES (%s, %s, 1, NOW())"
                self.db.execute_query(insert_play_query, (user_id, song_id))
                default_playlist_id = self.get_or_create_default_playlist(user_id)
                self.add_song_to_playlist(default_playlist_id, song_id)
            print(f"재생 횟수가 업데이트되었습니다.: 사용자 {user_id}, 곡 {song_id}")
        except Exception as e:
            print("재생 횟수 업데이트 중 오류 발생: {e}")

    def search_songs(self, query):
        search_query = """
            SELECT
                SONG.Song_id,
                SONG.Title,
                SONG.ReleaseDate,
                SONG.Genre,
                ARTIST.AtName,
                ALBUM.AbTitle
            FROM
                SONG
            JOIN 
                ALBUM
            ON
                SONG.Album = ALBUM.Album_id
            JOIN
                ARTIST  
            ON
                ALBUM.Artist = ARTIST.Artist_id
            WHERE
                SONG.Title Like %s OR ARTIST.AtName Like %s
        """
        try:
            return self.db.execute_query(search_query, (f"%{query}%", f"%{query}%"))
        except Exception as e:
            print(f"곡 검색 중 오류 발생: {e}")
            return []
    
    def check_like_status(self, user_id, song_id):
        # 좋아요 상태 확인
            query = "SELECT 1 FROM LIKES WHERE Who = %s AND LSONG = %s"
            result = self.db.execute_query(query, (user_id, song_id))
            return bool(result)
    def add_like(self, user_id, song_id):
        query = "INSERT INTO LIKES (Who, LSong) VALUES (%s, %s)"
        self.db.execute_query(query, (user_id, song_id))

    def remove_like(self, user_id, song_id):
        query = "DELETE FROM LIKES WHERE Who = %s AND LSong = %s"
        self.db.execute_query(query, (user_id, song_id))
    
    def increment_like_count(self, song_id):
        query = """
                UPDATE SONG SET LikeCount = LikeCount + 1 
                WHERE Song_id = %s
                """
        try: 
            self.db.execute_query(query, (song_id))
        except Exception as e:
            print(f"LikeCount 증가 실패: {e}")

    def decrement_like_count(self, song_id):
        query = "UPDATE SONG SET LikeCount = GREATEST(0, LikeCount - 1) WHERE Song_id = %s"
        self.db.execute_query(query, (song_id))



    def create_playlist(self, user_id, playlist_name, content = None):
        query_check = """
        SELECT Playlist_id
        FROM PLAYLIST
        WHERE Owner = %s AND PlTitle = %s
        """
        existing_playlist = self.db.execute_query(query_check, (user_id, playlist_name))
        if existing_playlist:
            print("이미 동일한 이름의 플레이리스트가 존재합니다.")
            return
        query_add = """
        INSERT INTO PLAYLIST (PlTitle, Content, CreateDate, Owner, PnumberOfSongs)
        VALUES (%s, %s, NOW(), %s, 0)
        """
        self.db.execute_query(query_add, (playlist_name, content, user_id))
        #방금 추가한 플레이리스트 ID 가져오기
        new_playlist_id = self.db.get_last_insert_id()
        print(f"새로운 플레이리스트가 생성되었습니다. ID: {new_playlist_id}")
        return new_playlist_id
    
    def get_or_create_default_playlist(self, user_id):
        # 기본 플레이리스트 확인
        query_check= """
        SELECT Playlist_id
        FROM PLAYLIST
        WHERE Owner = %s AND PlTitle = '나의 플레이리스트'
        """
        default_playlist = self.db.execute_query(query_check, (user_id,))
        if default_playlist:
            return default_playlist[0]['Playlist_id']
        query_add = """
        INSERT INTO PLAYLIST (PlTitle, Content, CreateDate, Owner, PnumberOfSongs)
        VALUES ('나의 플레이리스트', 'default playlist', NOW(), %s, 0)
        """
        self.db.execute_query(query_add, (user_id,))
        return self.db.get_last_insert_id()
    

    def add_song_to_playlist(self, playlist_id, song_id):
        query_check = """
        SELECT * FROM INCLUDE
        WHERE WhatPl = %s AND WhichSong = %s
        """
        existing_entry = self.db.execute_query(query_check, (playlist_id, song_id))
        if existing_entry:
            print("이 곡은 이미 플레이리스트에 추가되어 있습니다.")
            return
        #곡 추가
        query_add = """
        INSERT INTO INCLUDE (WhatPl, WhichSong)
        VALUEs (%s, %s)
        """
        self.db.execute_query(query_add, (playlist_id, song_id))
        # PnumberOfSongs 업데이트
        query_update = """
        UPDATE PLAYLIST
        SET PnumberOfSongs = PnumberOfSongs + 1
        WHERE Playlist_id  = %s
        """
        self.db.execute_query(query_update, (playlist_id,))
        print("곡이 플레이리스트에 추가되었습니다.")
    
    def get_user_playlists(self, user_id):
        query = """
        SELECT Playlist_id, PlTitle, PnumberOfSongs
        FROM PLAYLIST
        WHERE Owner = %s
        """
        return self.db.execute_query(query, (user_id,))
    
    def get_songs_in_playlist(self, playlist_id):
        query = """
        SELECT S.Song_id, S.Title, A.AtName AS Artist, Alb.AbTitle AS Album
        FROM INCLUDE I
        JOIN SONG S ON I.WhichSong = S.Song_id
        JOIN ALBUM Alb ON S.Album = Alb.Album_id
        JOIN ARTIST A ON Alb.Artist = A.Artist_id
        WHERE I.WhatPl = %s
        """
        return self.db.execute_query(query, (playlist_id,))
    
    def remove_song_from_playlist(self, playlist_id, song_id):
        # INCLUDE 테이블에서 곡 삭제
        query_delete = "DELETE FROM INCLUDE WHERE WhatPl = %s AND WhichSong = %s"
        self.db.execute_query(query_delete, (playlist_id, song_id))
        # PLAYLIST 테이블의 곡 수 업데이트
        query_update = """
        UPDATE PLAYLIST
        SET PnumberOfSongs = PnumberOfSongs - 1
        WHERE Playlist_id = %s
        """
        self.db.execute_query(query_update, (playlist_id,))
        print("곡이 성공적으로 삭제되었습니다.")

    def delete_playlist(self, playlist_id):
        # INCLUDE 테이블에서 플레이리스트에 포함된 곡 삭제
        query_delete_includes = "DELETE FROM INCLUDE WHERE WhatPl = %s"
        self.db.execute_query(query_delete_includes, (playlist_id,))
        # PLAYLIST 테이블에서 플레이리스트 삭제
        query_delete_playlist = "DELETE FROM PLAYLIST WHERE Playlist_id = %s"
        self.db.execute_query(query_delete_playlist, (playlist_id,))
        print(f"플레이리스트 ID {playlist_id}가 성공적으로 삭제되었습니다.")