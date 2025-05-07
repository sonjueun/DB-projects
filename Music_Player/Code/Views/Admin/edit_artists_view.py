from Controllers.Admin_Controllers.admin_controller import AdminController

class EditArtistsView:
    def __init__(self):
        self.admin_controller = AdminController()

    def display(self):
        print("\n=== 아티스트 수정 및 삭제 ===")

        #아티스트 검색 및 선택
        search_query = input("수정 또는 삭제할 아티스트의 이름을 입력하세요 (또는 '목록'을 입력하여 전체 아티스트 보기): ").strip()

        if search_query != '목록':
            results = self.admin_controller.search_artists(search_query)
            if not results:
                print("해당 이름의 아티스트를 찾을 수 없습니다.")
                return

            print("\n=== 검색 결과 ===")
            print(f"{'ID':<5}{'이름':<20}{'성별':<10}{'유형':<10}")
            print("-" * 50)
            for artist in results:
                print(f"{artist['Artist_id']:<5}{artist['AtName']:<20}{artist['Sex']:<10}{artist['Type']:<10}")
            print("-" * 50)
        else:
            # 아티스트 목록 전체 출력
            results = self.admin_controller.get_all_artists()
            if not results:
                print("등록된 아티스트가 없습니다.")
                return
            print("\n=== 아티스트 목록 ===")
            print(f"{'ID':<5}{'이름':<20}{'성별':<10}{'유형':<10}")
            print("-" * 50)
            for artist in results:
                print(f"{artist['Artist_id']:<5}{artist['AtName']:<20}{artist['Sex']:<10}{artist['Type']:<10}")
            print("-" * 50)

        # 아티스트 선택
        try:
            artist_id = int(input("수정 또는 삭제할 아티스트의 ID를 입력하세요: ").strip())
            selected_artist = next((artist for artist in results if artist['Artist_id'] == artist_id), None)
            if not selected_artist:
                print("유효한 곡 ID를 선택하세요.")
                return
        except ValueError:
            print("숫자를 입력하세요.")
            return
        
        # 수정 또는 삭제 작업
        self.handle_artist_edit_or_delete(selected_artist)

    def handle_artist_edit_or_delete(self, selected_artist):
        print("\n0. 취소하기")
        print("1. 아티스트 수정하기")
        print("2. 아티스트 삭제하기")

        try:
            choice = int(input("원하는 작업을 선택하세요: ").strip())
            if choice == 0:
                print("작업이 취소되었습니다.")
                return
            elif choice == 1:
                self.edit_artist(selected_artist)
            elif choice == 2:
                self.delete_artist(selected_artist)
            else:
                print("잘못된 입력입니다. 유효한 옵션을 선택하세요.")
        except ValueError:
            print("숫자를 입력하세요.")

    def edit_artist(self, selected_artist):
        print("\n=== 아티스트 수정하기 ===")
        new_name = input(f"새 이름 (현재: {selected_artist['AtName']}): ").strip() or selected_artist['AtName']
        new_sex = input(f"새 성별 (현재: {selected_artist['Sex']}, 남성/여성/혼성): ").strip()
        if new_sex in ["남성", "여성", "혼성"]:
            new_sex = {"남성": "M", "여성": "F", "혼성": "Other"}[new_sex]
        else:
            new_sex = selected_artist['Sex']
        new_type = input(f"새 유형 (현재: {selected_artist['Type']}, 솔로/듀오/그룹): ").strip()
        if new_type in ["솔로", "듀오", "그룹"]:
            new_type = {"솔로": "Solo", "듀오": "Duo", "그룹": "Group"}[new_type]
        else:
            new_type = selected_artist['Type']

        self.admin_controller.update_artist(selected_artist['Artist_id'], new_name, new_sex, new_type)
        print("아티스트 정보가 성공적으로 수정되었습니다.")

    def delete_artist(self, selected_artist):
        print("\n=== 아티스트 삭제하기 ===")
        confirm = input(f"정말로 '{selected_artist['AtName']}' 아티스트를 삭제하시겠습니까? (Y/N): ").strip().lower()
        if confirm == 'y':
            self.admin_controller.delete_artist(selected_artist['Artist_id'])
            print("아티스트가 성공적으로 삭제되었습니다.")
        else:
            print("삭제가 취소되었습니다.")

