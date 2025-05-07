
class AdminMain:
    def __init__(self, user_data):
        self.user_data = user_data
    def display(self):
        while True:
            print("\n=== 관리자 메인 화면 ===")
            print("0. 로그아웃")
            print("1. 곡 관리하기")
            print("2. 아티스트 관리하기")
            print("3. 앨범 관리하기")
            try: 
                choice = int(input("원하는 작업을 선택하세요: "))
                if choice ==  0:
                    # 로그인 페이지로
                    self.go_to_login_page()
                    break
                elif choice == 1:
                    self.manage_songs()
                    break
                elif choice == 2:
                    self.manage_artists()
                    break
                elif choice == 3:
                    self.manage_albums()
                else:
                    print("잘못된 입력입니다. 유효한 옵션을 선택하세요.")
            except ValueError:
                print("숫자를 입력하세요.")

        
    

    def go_to_login_page(self):
        from Views.login import LoginView
        login_view = LoginView()
        login_view.display()  

    def manage_songs(self):
        from Views.Admin.manage_songs import ManageSongs
        manage_songs_view = ManageSongs(self.user_data)
        manage_songs_view.display()

    def manage_artists(self):
        from Views.Admin.manage_artists import ManageArtists
        manage_artists_view = ManageArtists(self.user_data)
        manage_artists_view.display()

    def manage_albums(self):
        from Views.Admin.manage_albums import ManageAlbums
        manage_albums_view = ManageAlbums(self.user_data)
        manage_albums_view.display()
