from Controllers.User_Controllers.songs_controller import SongsController
class SongsView:
    def __init__(self, logged_in_user):
        self.controller = SongsController()
        self.logged_in_user = logged_in_user

    def display(self):
        while True:
            songs = self.controller.get_all_songs()
            print("\n=== 곡 목록 ===")
            print(f"{'ID':<5}{'제목':<20}{'아티스트':<20}")
            print("-"*50)

            for song in songs:
                print(f"{song['Song_id']:<5}{song['Title']:<20}{song['AtName']:<20}")
            print("-"*50)

            print("0. 이전 메뉴로")
            print("1. 재생하기")
            print("2. 곡 정보 보기")
            print("3. 좋아요 표시 / 취소")
            print("4. 플레이리스트에 곡 추가하기") ## 수정하기
            
            choice = int(input("원하는 작업을 선택하세요: ").strip())
            if choice == 0:
                self.go_to_main_page()
                break
                #return
            elif choice == 1:
                self.play_song(songs)
            elif choice == 2:
                self.show_song_info(songs)
            elif choice == 3:
                self.toggle_like(songs)
            elif choice == 4:
                self.add_song_to_playlist(songs)
            else:
                print("잘못된 입력입니다. 유효한 옵션을 선택하세요.")


    def go_to_main_page(self):
        
        from Views.User.user_main import UserMain
        main_view = UserMain(self.logged_in_user)
        main_view.display() # 로그인 페이지로 이동
        

   
    def play_song(self, songs):
        song_id = input("재생할 곡의 ID를 입력하세요: ").strip()
        song = next((song for song in songs if str(song['Song_id'])== song_id), None)
        if song:
            user_id = self.logged_in_user['User_id']
            self.controller.increment_play_count(user_id, song_id)
            print(f"\n🎶 '{song['Title']}' by {song['AtName']} 재생 중 ... \n")   
        else:
            print("유효하지 않은 ID입니다. 다시 시도하세요.\n")

    def toggle_like(self, songs):
        # 좋아요 토글 기능
        song_id = input("좋아요를 변경할 곡의 ID를 입력하세요: ").strip()
        song = next((song for song in songs if str(song['Song_id'])== song_id), None)
        if song:
            user_id = self.logged_in_user['User_id']
        
            if self.controller.check_like_status(user_id, song_id):
                #이미 좋아요를 누른 경우 -> 좋아요 취소
                confirm = input("이미 좋아요를 누른 곡입니다. 좋아요를 취소하시겠습니까? (y/n): ").strip().lower()
                if confirm == 'y':
                    self.controller.remove_like(user_id, song_id)
                    self.controller.decrement_like_count(song_id)
                    print("좋아요가 취소되었습니다.")
                else:
                    print("좋아요를 유지합니다.")
            else:
                # 좋아요를 누르지 않은 경우 -> 좋아요 추가
                    confirm = input("이 곡을 좋아요 하시겠습니끼? (y/n): ").strip().lower()
                    if confirm == 'y':
                        self.controller.add_like(user_id,song_id)
                        self.controller.increment_like_count(song_id)
                        print("좋아요가 추가되었습니다.")
                    else:
                        print("좋아요를 취소하였습니다.")
        else:
            print("유효하지 않은 ID입니다. 다시 시도하세요.\n")

    def show_song_info(self, songs):
        song_id = input("정보를 확인할 곡의 ID를 입력하세요: ").strip()
        song = next((song for song in songs if str(song['Song_id'])== song_id), None)
        if song:
            print(f"\n=== 곡 정보 ===")
            print(f"ID: {song['Song_id']}")
            print(f"제목: {song['Title']}")
            print(f"아티스트: {song['AtName']}")
            print(f"발매일: {song['ReleaseDate']}")
            print(f"장르: {song['Genre']}")
            print(f"앨범명: {song['AbTitle']}")
            #발매일, 
            print("=" *30 + "\n")
        else:
            print("\n유효하지 않은 ID입니다. 다시 시도하세요.\n")
        
    def add_song_to_playlist(self, songs):
        try:
            song_id = int(input("플레이리스트에 추가할 곡의 ID를 입력하세요: ").strip())
            selected_song = next((song for song in songs if song['Song_id'] == song_id), None)
            if not selected_song:
                print("유효한 곡 ID를 선택하세요.")
                return
        except ValueError:
            print("유효한 숫자를 입력하세요.")
            return
        
        # 사용자 플레이리스트 목록 가져오기
        playlists = self.controller.get_user_playlists(self.logged_in_user["User_id"])
        if not playlists:
            print("플레이리스트가 없습니다.")
            return 
        
        # 플레이리스트 선택
        print("\n=== 내 플레이리스트 목록 ===")
        for playlist in playlists:
            print(f"ID: {playlist['Playlist_id']}, 이름: {playlist['PlTitle']}, 곡 수: {playlist['PnumberOfSongs']}")
        try:
            playlist_id = int(input("곡을 추가할 플레이리스트 ID를 입력하세요: ").strip())
            selected_playlist = next((pl for pl in playlists if pl['Playlist_id'] == playlist_id), None)
            if not selected_playlist:
                print("유효한 플레이리스트 ID를 선택하세요.")
                return
        except ValueError:
            print("유효한 숫자를 입력하세요.")
            return

        # 곡 추가
        self.controller.add_song_to_playlist(playlist_id, song_id)
        