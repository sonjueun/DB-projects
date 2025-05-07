from Controllers.Admin_Controllers.admin_controller import AdminController
from Controllers.User_Controllers.songs_controller import SongsController

class EditSongsView:
    def __init__(self):
        self.songs_controller = SongsController()
        self.admin_controller = AdminController()

    def display(self):
        print("\n=== 곡 수정 및 삭제 ===")
        # 곡 검색 및 선택
        search_query = input("수정 또는 삭제할 곡의 제목을 입력하세요 (또는 '목록' 입력하여 전체 곡 보기): ").strip()
        if search_query != '목록':
            results = self.songs_controller.search_songs(search_query)
            if not results:
                print("해당 제목의 곡을 찾을 수 없습니다.")
                return
            print("\n=== 검색 결과 ===")
            print(f"{'ID':<5}{'제목':<20}{'아티스트':<20}")
            print("-" * 50)
            for song in results:
                print(f"{song['Song_id']:<5}{song['Title']:<20}{song['AtName']:<20}")
            print("-" * 50)
        else:
            # 곡 목록 전체 출력
            results = self.songs_controller.get_all_songs()
            if not results:
                print("등록된 곡이 없습니다.")
                return
            print("\n=== 곡 목록 ===")
            print(f"{'ID':<5}{'제목':<20}{'아티스트':<20}")
            print("-" * 50)
            for song in results:
                print(f"{song['Song_id']:<5}{song['Title']:<20}{song['AtName']:<20}")
            print("-" * 50)

        # 곡 선택
        try:
            song_id = int(input("수정 또는 삭제할 곡의 ID를 입력하세요: ").strip())
            selected_song = next((song for song in results if song['Song_id'] == song_id), None)
            if not selected_song:
                print("유효한 곡 ID를 선택하세요.")
                return
        except ValueError:
            print("숫자를 입력하세요.")
            return
        # 수정 또는 삭제 작업
        self.handle_song_edit_or_delete(selected_song)

    
    def handle_song_edit_or_delete(self, selected_song):
        print("\n0. 취소하기")
        print("1. 곡 수정하기")
        print("2. 곡 삭제하기")
        try:
            choice = int(input("원하는 작업을 선택하세요: ").strip())
            if choice == 0:
                print("작업이 취소되었습니다.")
                return
            elif choice == 1:
                self.edit_song(selected_song)
            elif choice == 2:
                self.delete_song(selected_song)
            else:
                print("잘못된 입력이빈다. 유효한 옵션을 선택하세요.")
        except ValueError:
            print("숫자를 입력하세요.")
            
    def edit_song(self, selected_song):
        print("\n=== 곡 수정하기 ===")
        new_title = input(f"새 제목 (현재: {selected_song['Title']}): ").strip() or selected_song['Title']
        new_release_date = input(f"새 발매일 (현재: {selected_song.get('ReleaseDate', 'N/A')}): ").strip() or selected_song.get('ReleaseDate', 'N/A')
        new_genre = input(f"새 장르 (현재: {selected_song.get('Genre', 'N/A')}): ").strip() or selected_song.get('Genre', 'N/A')
        new_lyrics = input(f"새 가사 (현재: {selected_song.get('Lyrics', 'N/A')}): ").strip() or selected_song.get('Lyrics', 'N/A')
        self.admin_controller.update_songs(selected_song['Song_id'], new_title, new_release_date, new_genre, new_lyrics)
        print("곡 정보가 성공적으로 수정되었습니다.")

    def delete_song(self, selected_song):
        print("\n=== 곡 삭제하기 ===")
        confirm = input(f"정말로 '{selected_song['Title']}' 곡을 삭제하시겠습니까? (Y/N): ").strip().lower()
        if confirm == 'y':
            self.admin_controller.delete_songs(selected_song['Song_id'])
            print("곡이 성공적으로 삭제되었습니다.")
        else:
            print("삭제가 취소되었습니다.")

