from Views.User.songs_view import SongsView
from Controllers.User_Controllers.songs_controller import SongsController
class ManagePlaylists:
    def __init__(self, user_data):
        self.user_data = user_data
        self.songs_controller = SongsController()
        self.songs_view = SongsView(user_data)

    def display(self):
        while True:
            #현재 사용자의 플레이리스트 목록 가져오기
            print("\n=== 플레이리스트 ===")
            playlists = self.songs_controller.get_user_playlists(self.user_data["User_id"])
            if playlists:
                for playlist in playlists:
                    print(f"ID: {playlist['Playlist_id']}, 이름: {playlist['PlTitle']}, 곡 수: {playlist['PnumberOfSongs']}")
            else:
                print("플레이리스트가 없습니다.")

            print("0. 이전 메뉴로")
            print("1. 새 플레이리스트 생성")
            print("2. 플레이리스트 삭제")
            print("3. 플레이리스트 관리")

            try:
                choice = int(input("원하는 작업을 선택하세요: ").strip())
                if choice == 0:
                    self.songs_view.go_to_main_page()
                    break
                elif choice == 1:
                    self.create_playlist()
                elif choice == 2:
                    self.delete_playlist()
                elif choice == 3:
                    self.edit_playlist()
                else:
                    print("잘못된 입력입니다. 유효한 옵션을 선택하세요.")
            except ValueError:
                print("숫자를 입력하세요.")

    def create_playlist(self):
       
            playlist_name = input("새 플레이리스트 이름을 입력하세요: ").strip()
            if not playlist_name:
                print("플레이리스트 이름을 입력해야 합니다.")
                return
            self.songs_controller.create_playlist(self.user_data["User_id"], playlist_name)

    def edit_playlist(self):
        try:
            print("\n=== 플레이리스트 ===")
            playlists = self.songs_controller.get_user_playlists(self.user_data["User_id"])
            if playlists:
                for playlist in playlists:
                    print(f"ID: {playlist['Playlist_id']}, 이름: {playlist['PlTitle']}, 곡 수: {playlist['PnumberOfSongs']}")
            else:
                print("플레이리스트가 없습니다.")

            playlist_id = int(input("수정할 플레이리스트 ID를 입력하세요: ").strip())
             # 사용자의 플레이리스트 가져오기
            playlists = self.songs_controller.get_user_playlists(self.user_data["User_id"])
            selected_playlist = next((pl for pl in playlists if pl['Playlist_id'] == playlist_id), None)
            if not selected_playlist:
                print("유효한 플레이리스트 ID를 선택하세요.")
                return
        
            # 선택한 플레이리스트의 곡 목록
            songs_in_playlist = self.songs_controller.get_songs_in_playlist(playlist_id)
            print(f"\n=== 플레이리스트 '{selected_playlist['PlTitle']}'의 곡 목록 ===")
            if not songs_in_playlist:
                print("플레이리스트에 곡이 없습니다.")
            else:
                for song in songs_in_playlist:
                    print(f"ID: {song['Song_id']}, 제목: {song['Title']}, 아티스트: {song['Artist']}")

            #수정 작업 선택
            print("\n0. 이전메뉴로")
            print("1. 곡 삭제하기")
            choice = int(input("원하는 작업을 선택하세요: ").strip())
            if choice == 0:
                # 이전 메뉴로
                return
            elif choice == 1:
               self.remove_song_from_playlist(playlist_id)
            else:
                print("잘못된 입력입니다.")
        except ValueError:
            print("유효한 숫자를 입력하세요.")


    def remove_song_from_playlist(self, playlist_id):
        # 선택한 플레이리스트 내 곡 목록 가져오기
        songs_in_playlist = self.songs_controller.get_songs_in_playlist(playlist_id)
        if not songs_in_playlist:
            print("플레이리스트에 곡이 없습니다.")
            return

        print("\n=== 플레이리스트 내 곡 목록 ===")
        for song in songs_in_playlist:
            print(f"ID: {song['Song_id']}, 제목: {song['Title']}, 아티스트: {song['Artist']}")

        try:
            # 삭제할 곡 선택
            song_id = int(input("삭제할 곡 ID를 입력하세요: ").strip())
            selected_song = next((song for song in songs_in_playlist if song['Song_id'] == song_id), None)
            if not selected_song:
                print("유효한 곡 ID를 선택하세요.")
                return

            # 곡 삭제
            self.songs_controller.remove_song_from_playlist(playlist_id, song_id)
            print(f"곡 '{selected_song['Title']}'가 플레이리스트에서 삭제되었습니다.")
        except ValueError:
            print("유효한 숫자를 입력하세요.")

    def delete_playlist(self):
        # 사용자의 플레이리스트 목록 가져오기
        playlists = self.songs_controller.get_user_playlists(self.user_data["User_id"])
        if not playlists:
            print("삭제할 플레이리스트가 없습니다.")
            return
        print("\n=== 플레이리스트 목록 ===")
        for playlist in playlists:
            print(f"ID: {playlist['Playlist_id']}, 이름: {playlist['PlTitle']}, 곡 수: {playlist['PnumberOfSongs']}")
        try:
            # 삭제할 플레이리스트 선택
            playlist_id = int(input("삭제할 플레이리스트 ID를 입력하세요: ").strip())
            selected_playlist = next((pl for pl in playlists if pl['Playlist_id'] == playlist_id), None)
            if not selected_playlist:
                print("유효한 플레이리스트 ID를 선택하세요.")
                return
            # 삭제 확인
            confirm = input(f"'{selected_playlist['PlTitle']}' 플레이리스트를 삭제하시겠습니까? (Y/N): ").strip().lower()
            if confirm == 'y':
                self.songs_controller.delete_playlist(playlist_id)
                print(f"플레이리스트 '{selected_playlist['PlTitle']}'가 삭제되었습니다.")
            else:
                print("삭제가 취소되었습니다.")
        except ValueError:
            print("유효한 숫자를 입력하세요.")