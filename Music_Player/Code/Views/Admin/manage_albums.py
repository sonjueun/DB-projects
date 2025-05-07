from Views.Admin.manage_songs import ManageSongs
from Controllers.Admin_Controllers.admin_controller import AdminController
from Views.Admin.edit_albums_view import EditAlbumsView


class ManageAlbums:
    def __init__ (self, user_data):
        self.user_data = user_data
        self.manage_songs = ManageSongs(user_data)
        self.admin_controller = AdminController()
        self.edit_albums_view = EditAlbumsView()

    def display(self):
        while True:
            print("\n=== 앨범 관리 ===")
            print("0. 이전 메뉴로")
            print("1. 앨범 추가하기")
            print("2. 앨범 수정 및 삭제하기")
            try:
                choice = int(input("원하는 작업을 선택하세요: "))
                if choice == 0:
                    self.manage_songs.go_to_main_page()
                    break
                elif choice == 1:
                    self.add_album()
                elif choice == 2:
                    self.edit_albums_view.display()
                else:
                    print("잘못된 입력입니다. 유효한 옵션을 선택하세요.")
            except ValueError:
                print("숫자를 입력하세요.")

    
    def add_album(self):
        print("\n=== 앨범 추가 ===")
        #앨범 제목 입력
        album_title = input("앨범 제목을 입력하세요: ").strip()
        if not album_title:
            print("앨범 제목을 입력해야 합니다.")
            return
        #발매 날짜 입력
        release_date  = input("앨범 발매 일자를 입력하세요(yyyy-mm-dd): ").strip()
        if not release_date:
            print("발매 일자를 입력해야 합니다.")
            return
        #아티스트 선택 또는 추가
        artist_name = input("앨범의 아티스트 이름을 입력하세요: ").strip()
        if not artist_name:
            print("아티스트 이름을 입력해야 합니다.")
            return
        artist_id = self.admin_controller.get_or_add_artist(artist_name)
        #앨범 추가 
        self.admin_controller.get_or_add_album(album_title, release_date, artist_id)
