from Views.User.songs_view import SongsView
from Controllers.User_Controllers.songs_controller import SongsController
class SearchSong:
    def __init__(self, logged_in_user):
        self.logged_in_user = logged_in_user
        self.controller = SongsController()
        self.songs_view = SongsView(logged_in_user)

    def display(self):
        # 검색 화면 출력 및 사용자 입력 처리
        print("\n=== 곡 검색 ===")
        query = input("검색할 곡 제목이나 아티스트 이름을 입력하세요: ").strip()
        if not query:
            print("검색어를 입력해주세요.")
            return
        #검색 실행
        results = self.controller.search_songs(query)
        #검색 결과 출력
        if results:
            print("\n === 검색 결과 ===")
            print(f"{'ID':<5}{'제목':<20}{'아티스트':<20}")
            print("-"*50)
            for song in results:
                print(f"{song['Song_id']:<5}{song['Title']:<20}{song['AtName']:<20}")
            print("-"*50)
        else:
            print("검색 결과가 없습니다.")
            
        self.handle_results_menu(results)

    def handle_results_menu(self, results):
        while True:
            print("0. 이전 메뉴로")
            print("1. 재생하기")
            print("2. 곡 정보 보기")
            try:
                choice = int(input("원하는 작업을 선택하세요: ").strip())
                if choice == 0:
                    self.songs_view.go_to_main_page()
                    break
                elif choice == 1:
                    self.songs_view.play_song(results)
                elif choice == 2:
                    self.songs_view.show_song_info(results)
                else:
                    print("잘못된 입력입니다. 유효한 옵션을 선택하세요.")
            except ValueError:
                print("숫자를 입력하세요.")


    

