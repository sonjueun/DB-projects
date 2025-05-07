from DB.database import Database

class AdminController:
    def __init__(self):
        self.db = Database()

    def get_or_add_artist(self, artist_name):
        # 아티스트 중복 확인
        query_check = "SELECT Artist_id, AtName FROM Artist WHERE AtName LIKE %s"
        result = self.db.execute_query(query_check, (f"%{artist_name}%", ))
        #print(result)

        if result:
            print("\n해당 아티스트 목록")
            for row in result:
                print(f"ID: {row['Artist_id']}, Name: {row['AtName']}")
            while True:

                choice = input("기존 아티스트를 선택하려면 ID를 입력하고, 새로 추가하려면 Enter를 누르세요: ").strip()
                if choice.isdigit():
                    selected_index = int(choice) 
                    if any(row['Artist_id']== selected_index for row in result):
                        return selected_index
                    else:
                        print("잘못된 번호입니다. 다시 시도하세요.")
                        
                elif choice == "":
                    break
                else:
                    print("잘못된 입력입니다. 다시 시도하세요.")
                                

        
        # 새로운 아티스트 추가
        print("새로운 아티스트를 추가합니다.")

        while True:
            sex = input("성별을 입력하세요 (남성/여성/혼성): ").strip()
            if sex == "남성":
                sex = "M"
            elif sex ==  "여성":
                sex = "F"
            elif sex == "혼성":
                sex = "Other"
            else:
                print("잘못된 성별 입력입니다. 다시 입력해주세요.")
                continue
            break

        while True:
            artist_type = input("아티스트 유형을 입력하세요(솔로/듀오/그룹): " ).strip()
            if artist_type == "솔로":
                artist_type = "Solo"
            elif artist_type == "듀오":
                artist_type = "Duo"
            elif artist_type == "그룹":
                artist_type = "Group"
            else:
                print("잘못된 유형 입력입니다. 다시 입력해주세요.")
                continue
            break

        query_add = "INSERT INTO Artist (AtName, Sex, Type) VALUES (%s, %s ,%s)"
        self.db.execute_query(query_add, (artist_name, sex, artist_type))
        new_artist_id = self.db.get_last_insert_id()
        print(f"아티스트 '{artist_name}'가 추가되었습니다. ID: {new_artist_id}")
        return new_artist_id
    
    def get_or_add_album(self, album_title, album_release_date, artist_id):
        # 앨범 중복 확인
        query_check = """
        SELECT Album_id, AbTitle, AbReleaseDate
        FROM Album
        WHERE AbTitle = %s AND Artist = %s
        """
        result = self.db.execute_query(query_check, (album_title, artist_id ))

        if result:
            print("\n해당 앨범 목록")
            for row in result:
                print(f"ID: {row['Album_id']}, Title: {row['AbTitle']}, ReleaseDate: {row['AbReleaseDate']}")

                choice = input("기존 앨범을 선택하려면 ID를 입력하고, 새로 추가하려면 Enter를 누르세요: ").strip()
                if choice.isdigit():
                    selected_index = int(choice) 
                    if any(row['Album_id']== selected_index for row in result):
                        return selected_index
                    else:
                        print("잘못된 번호입니다. 다시 시도하세요.")
                        
                elif choice == "":
                    break
                else:
                    print("잘못된 입력입니다. 다시 시도하세요.")
                             
       

        # 새로운 앨범 추가
        print("새로운 앨범을 추가합니다.")
        
        #album_release_date= input("발매일을 입력하세요(yyyy-mm-dd): ").strip()


        query_add = "INSERT INTO Album (AbTitle, AbReleaseDate, Artist) VALUES (%s, %s ,%s)"
        self.db.execute_query(query_add, (album_title, album_release_date, artist_id))

        new_album_id = self.db.get_last_insert_id()
        print(f"앨범 '{album_title}'가 추가되었습니다. ID: {new_album_id}")
        return new_album_id

    def add_song_to_db(self, song_title, release_date, genre, album_id, lyrics):
        query_add_song = """
        INSERT INTO SONG(Title, ReleaseDate, Genre, Album, Lyrics)
        VALUES(%s,%s,%s,%s,%s)
        """

        self.db.execute_query(query_add_song, (song_title, release_date, genre, album_id, lyrics))
        new_song_id = self.db.get_last_insert_id()
        print(f"곡 '{song_title}'가 성공적으로 추가되었습니다. ID: {new_song_id}")

        #앨범의 곡 개수 업데이트
        query_update_album = "UPDATE Album SET NumOfSongs = NumOfSongs + 1 WHERE Album_id = %s"
        self.db.execute_query(query_update_album, (album_id,))

        return new_song_id
        
    def update_songs(self, song_id, new_title = None, new_release_date = None, new_genre = None, new_lyrics = None):
        # 현재 곡 정보 가져오기
        query_get_song = "SELECT Title, ReleaseDate, Genre, Lyrics FROM SONG WHERE Song_id = %s"
        song = self.db.execute_query(query_get_song, (song_id,))

        if not song:
            print("해당 곡 ID를 찾을 수 없습니다.")
            return
        
        song = song[0]
        updated_title = new_title or song['Title']
        updated_release_date = new_release_date or song['ReleaseDate']
        updated_genre = new_genre or song['Genre']
        updated_lyrics = new_lyrics or song['Lyrics']

        #곡 정보 업데이트
        query_update_song ="""
        UPDATE SONG
        SET Title = %s, ReleaseDate = %s, Genre  = %s, Lyrics = %s
        WHERE Song_id = %s 
        """

        self.db.execute_query(query_update_song, (updated_title, updated_release_date, updated_genre, updated_lyrics, song_id))
        print(f"곡 ID {song_id}의 정보가 성공적으로 수정되었습니다.")
    
    def delete_songs(self, song_id):
        query_get_album = "SELECT Album FROM SONG WHERE Song_id = %s"
        result = self.db.execute_query(query_get_album, (song_id, ))
        if not result:
            print("해당 곡 ID를 찾을 수 없습니다.")
            return
        album_id = result[0]['Album']

        #곡 삭제
        query_delete_song = "DELETE FROM SONG WHERE Song_id = %s"
        self.db.execute_query(query_delete_song, (song_id,))
        print(f"곡 ID {song_id}가 성공적으로 삭제되었습니다.")

        #앨범의 곡 개수 업데이트
        query_update_album = "UPDATE Album SET NumOfSongs = NumOfSongs -1 WHERE Album_id = %s"
        self.db.execute_query(query_update_album, (album_id,))

    def delete_artist(self, artist_id):
        query_check_songs = "SELECT COUNT(*) AS SongCount FROM SONG WHERE Album IN (SELECT Album_id FROM Album WHERE Artist = %s)"
        query_check_albums = "SELECT COUNT(*) AS AlbumCount FROM Album WHERE Artist = %s"

        #곡과 앨범 확인
        song_count  = self.db.execute_query(query_check_songs, (artist_id,))
        album_count = self.db.execute_query(query_check_albums, (artist_id,))

        if song_count[0]['SongCount'] > 0 or album_count[0]['AlbumCount'] > 0:
            print(f"해당 아티스트와 연결된 곡 {song_count[0]['SongCount']}개, 앨범 {album_count[0]['AlbumCount']}개가 있습니다.")
            confirm = input("이 아티스트와 관련된 모든 데이터를 삭제하시겠습니까? (Y/N): ").strip().lower()
            if confirm !='y':
                print("삭제가 취소되었습니다.")
                return
            
            #연결된 곡 삭제
            query_delete_songs = """
            DELETE FROM SONG
            WHERE Album IN (SELECT Album_id FROM Album WHERE Artist = %s)
            """
            self.db.execute_query(query_delete_songs, (artist_id,))
            print(f"연결된 곡 {song_count[0]['SongCount']}개가 삭제되었습니다.")

            #연결된 앨범 삭제
            query_delete_albums = "DELETE FROM ALBUM WHERE Artist = %s"
            self.db.execute_query(query_delete_albums, (artist_id,))
            print(f"연결된 앨범 {album_count[0]['AlbumCount']}개가 삭제되었습니다.")

        # 아티스트 삭제
        query_delete_artist = "DELETE FROM Artist WHERE Artist_id = %s"
        self.db.execute_query(query_delete_artist, (artist_id,))
        print(f"아티스트 ID {artist_id}가 성공적으로 삭제되었습니다.")


    def get_all_artists(self):
        query = "SELECT Artist_id, AtName, Sex, Type FROM Artist"
        return self.db.execute_query(query)
    
    def update_artist(self, artist_id, new_name, new_sex, new_type):
        query = """
        UPDATE Artist
        SET AtName = %s, Sex = %s, Type = %s
        WHERE Artist_id = %s
        """
        self.db.execute_query(query, (new_name,new_sex,new_type, artist_id))

    def search_artists(self, artist_name):
        query = "SELECT Artist_id, AtName, Sex, Type FROM Artist WHERE AtName LIKE %s"
        return self.db.execute_query(query, (f"%{artist_name}%",))
    
    def search_albums(self, album_title):
        query = """
        SELECT Album_id, AbTitle, AbReleaseDate, Artist
        FROM Album
        WHERE AbTitle LIKE %s
        """

        return self.db.execute_query(query, (f"%{album_title}%",))
    
    def get_all_albums(self):
        query = """
        SELECT Album_id, AbTitle, AbReleaseDate, Artist
        FROM Album
        """
        return self.db.execute_query(query)

    def update_album(self, album_id, new_title, new_release_date):
        query = """
        UPDATE Album
        SET AbTitle = %s, AbReleaseDate = %s
        WHERE Album_id = %s
        """
        self.db.execute_query(query, (new_title, new_release_date, album_id))

    def delete_album(self, album_id):
        query = "DELETE FROM Album WHERE Album_id = %s"
        self.db.execute_query(query, (album_id,))