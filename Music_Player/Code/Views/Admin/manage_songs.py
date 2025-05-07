from Controllers.Admin_Controllers.admin_controller import AdminController
#from Controllers.User_Controllers.songs_controller import SongsController
from Views.Admin.edit_songs_view import EditSongsView
class ManageSongs:
    def __init__(self, logged_in_user):
        self.controller = AdminController()
        #self.songs_controller = SongsController()
        self.edit_songs_view = EditSongsView()
        self.logged_in_user = logged_in_user

    def display(self):
        while True:
            print("\n=== 곡 관리하기 ===")
            print("0. 이전 메뉴로")
            print("1. 추가하기")
            print("2. 수정 및 삭제하기")
            try: 
                choice = int(input("원하는 작업을 선택하세요: "))
                if choice == 0:
                    #이전 메뉴로
                    self.go_to_main_page()
                    break    
                elif choice == 1:
                    self.add_song()
                elif choice == 2:
                    self.edit_songs_view.display()
                else:
                    print("잘못된 입력입니다. 유효한 옵션을 선택하세요.")
            except ValueError:
                print("숫자를 입력하세요.")

    def go_to_main_page(self):
        from Views.Admin.admin_main import AdminMain
        main_view = AdminMain(self.logged_in_user)
        main_view.display() # 로그인 페이지로 이동

    def add_song(self):
        print("\n=== 곡 추가하기 ===")
        print("=== 1. 아티스트 정보 입력 및 확인 ===")
        artist_name = input("아티스트 이름을 입력하세요: ").strip()
        # 이름이 중복되면 화면 보여주고 관리자가 선택하게 하기
        artist_id = self.controller.get_or_add_artist(artist_name)
        
        print("=== 2. 앨범 정보 입력 및 확인 ===") 
        album_title = input("앨범명을 입력하세요: ").strip()
        album_release_date = input("발매일을 입력하세요(yyyy-dd-mm): ").strip()
        album_id = self.controller.get_or_add_album(album_title,album_release_date, artist_id)

        print("=== 3. 곡 정보 입력 및 확인 ===")
        song_title = input("곡 제목을 입력하세요: ").strip()
        genre = input("장르를 입력하세요: ").strip()
        lyrics = input("가사를 입력하세요: ").strip()
     
        if not song_title:
            print("곡 제목을 입력하세요.")
            return
        # db에 곡 등록
        self.controller.add_song_to_db(song_title, album_release_date, genre, album_id, lyrics)

       


        




     

