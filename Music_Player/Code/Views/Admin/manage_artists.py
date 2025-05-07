
from Views.Admin.manage_songs import ManageSongs
from Controllers.Admin_Controllers.admin_controller import AdminController
from Views.Admin.edit_artists_view import EditArtistsView
class ManageArtists:
    def __init__(self, user_data):
        self.user_data = user_data
        self.manage_songs = ManageSongs(user_data)
        self.admin_controller = AdminController()
        self.edit_artist_view = EditArtistsView()
    
    def display(self):
        while True:
            print("\n=== 아티스트 관리 ===")
            print("0. 이전 메뉴로")
            print("1. 아티스트 추가하기")
            print("2. 아티스트 수정 및 삭제하기")
            try:
                choice = int(input("원하는 작업을 선택하세요: "))
                if choice == 0:
                    self.manage_songs.go_to_main_page()
                    break
                elif  choice == 1:
                    self.add_artist()
                elif choice == 2:
                    self.edit_artist_view.display()
                else:
                    print("잘못된 입력입니다. 유효한 옵션을 선택하세요.")
            except ValueError:
                print("숫자를 입력하세요.")

    
    def add_artist(self):
        print("\n=== 아티스트 추가 ===")
        # 아티스트 이름 입력
        artist_name = input("아티스트 이름을 입력하세요: ").strip()
        if not artist_name:
            print("아티스트 이름을 입력해야 합니다.")
            return
        self.admin_controller.get_or_add_artist(artist_name)
      


