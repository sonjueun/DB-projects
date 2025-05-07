

class UserMain:
    def __init__(self, logged_in_user):
        self.logged_in_user = logged_in_user

    def display(self):
        while True:
            print("\n메인 화면")
            print("0. 로그아웃")
            print("1. 곡 보기")
            print("2. 곡 찾기")
            print("3. 플레이리스트 관리하기")
            print("4. 좋아요 표시한 곡 보기")
           

            try: 
                choice = int(input("원하는 작업을 선택하세요: "))
                if choice == 0:
                    self.go_to_login_page()
                    break

                elif choice == 1:
                    self.view_songs()
                    break

                elif choice == 2:
                    self.search_song()
                    break
                
                elif choice == 3:
                    self.manage_playlists()
                    break

                elif choice == 4:
                    self.view_liked_songs()
                    break

                else:
                    print("잘못된 입력입니다. 유효한 옵션을 선택하세요.")
                
            except ValueError:
                print("숫자를 입력하세요.")

    def go_to_login_page(self):
        from Views.login import LoginView
        login_view = LoginView()
        login_view.display() 
        

    def view_songs(self):
        from Views.User.songs_view import SongsView
        songs_view = SongsView(self.logged_in_user)
        songs_view.display()
       
    def search_song(self):
        from Views.User.search_song import SearchSong
        search_view = SearchSong(self.logged_in_user)
        search_view.display()
    
    def manage_playlists(self):
        from Views.User.manage_playlists import ManagePlaylists
        manage_playlists_view = ManagePlaylists(self.logged_in_user)
        manage_playlists_view.display()

    def view_liked_songs(self):
        from Views.User.liked_songs_view import LikedSongsView
        liked_songs_view = LikedSongsView(self.logged_in_user)
        liked_songs_view.display()


