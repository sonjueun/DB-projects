from Controllers.Admin_Controllers.admin_controller import AdminController

class EditAlbumsView:
    def __init__(self):
        self.admin_controller = AdminController()

    def display(self):
        print("\n=== 앨범 수정 및 삭제 ===")

        #앨범 검색 및 선택
        search_query = input("수정 또는 삭제할 앨범의 제목을 입력하세요 (또는 '목록'을 입력하여 전체 앨범 보기): ").strip()

        if search_query != '목록':
            results = self.admin_controller.search_albums(search_query)
            if not results:
                print("해당 제목의 앨범을 찾을 수 없습니다.")
                return
            
            print("\n=== 검색 결과 ===")
            print(f"{'ID':<5}{'제목':<20}{'발매일':<15}{'아티스트':<20}")
            print("-" * 60)
            for album in results:
                release_date = album['AbReleaseDate']
                formatted_date = release_date.strftime('%Y-%m-%d')
                print(f"{album['Album_id']:<5}{album['AbTitle']:<20}{formatted_date:<15}{album['Artist']:<20}")
            print("-" * 60)
        else:
            #앨범 목록 전체 출력
            results = self.admin_controller.get_all_albums()
            if not results:
                print("등록된 앨범이 없습니다.")
                return
            print("\n=== 앨범 목록 ===")
            print(f"{'ID':<5}{'제목':<20}{'발매일':<15}{'아티스트':<20}")
            print("-" * 60)
            for album in results:
                release_date = album['AbReleaseDate']
                formatted_date = release_date.strftime('%Y-%m-%d')
                print(f"{album['Album_id']:<5}{album['AbTitle']:<20}{formatted_date:<15}{album['Artist']:<20}")
            print("-" * 60)

        #앨범 선택
        try:
            album_id = int(input("수정 또는 삭제할 앨범의 ID를 입력하세요: ").strip())
            selected_album = next((album for album in results if album['Album_id'] == album_id), None)
            if not selected_album:
                print("유효한 앨범 ID를 선택하세요.")
                return
        except ValueError:
            print("숫자를 입력하세요.")
            return
        
        #수정 또는 삭제 작업
        self.handle_album_edit_or_delete(selected_album)

    def handle_album_edit_or_delete(self, selected_album):
        print("\n0. 취소하기")
        print("1. 앨범 수정하기")
        print("2. 앨범 삭제하기")
        try:
            choice = int(input("원하는 작업을 선택하세요: ").strip())
            if choice == 0:
                print("작업이 취소되었습니다.")
                return
            elif choice == 1:
                self.edit_album(selected_album)
            elif choice == 2:
                self.delete_album(selected_album)
            else:
                print("잘못된 입력입니다. 유효한 옵션을 선택하세요.")
        except ValueError:
            print("숫자를 입력하세요.")

    def edit_album(self, selected_album):
        print("\n=== 앨범 수정하기 ===")
        new_title = input(f"새 제목 (현재: {selected_album['AbTitle']}): ").strip() or selected_album['AbTitle']
        new_release_date = input(f"새 발매일 (현재: {selected_album['AbReleaseDate']}): ").strip() or selected_album['AbReleaseDate']

        self.admin_controller.update_album(selected_album['Album_id'], new_title, new_release_date)
        print("앨범 정보가 성공적으로 수정되었습니다.")

    def delete_album(self, selected_album):
        print("\n=== 앨범 삭제하기 ===")
        confirm = input(f"정말로 '{selected_album['AbTitle']}' 앨범을 삭제하시겠습니까? (Y/N): ").strip().lower()
        if confirm == 'y':
            self.admin_controller.delete_album(selected_album['Album_id'])
            print("앨범이 성공적으로 삭제되었습니다.")
        else:
            print("삭제가 취소되었습니다.")

