from Views.User.songs_view import SongsView
from Controllers.User_Controllers.songs_controller import SongsController
class LikedSongsView:
    def __init__ (self, logged_in_user):
        self.controller = SongsController()
        self.logged_in_user = logged_in_user
        self.songs_view = SongsView(logged_in_user)

    def display(self):
      
        # 좋아요 누른 곡 가쟈오기
        liked_songs = self.controller.get_liked_songs(self.logged_in_user['User_id'])
        print("\n=== 좋아요 누른 곡 목록 ===")
        if liked_songs:
            print(f"{'ID':<5}{'제목':<20}{'아티스트':<20}")
            print("-"*50)
            for song in liked_songs:
                print(f"{song['Song_id']:<5}{song['Title']:<20}{song['AtName']:<20}")
            print("-"*50)
        else:
            print("좋아요를 누른 곡이 없습니다.")
            return
        self.handle_results_menu(liked_songs)


    def handle_results_menu(self, liked_songs):
        while True:
            print("0. 이전 메뉴로")
            if liked_songs:
                print("1. 곡 재생하기")
                print("2. 곡 정보 보기")
                print("3. 좋아요 표시/수정하기\n")
            try:
                choice = int(input("원하는 작업을 선택하세요: ").strip())
                if choice == 0:
                    self.songs_view.go_to_main_page()
                    break
                elif choice == 1:
                    self.songs_view.play_song(liked_songs)
                elif choice == 2:
                    self.songs_view.show_song_info(liked_songs)
                elif choice == 3:
                    self.songs_view.toggle_like(liked_songs)
                else:
                    print("잘못된 입력입니다. 유효한 옵션을 선택하세요.")
            except ValueError:
                print("숫자를 입력하세요.")

                