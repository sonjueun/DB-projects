from Controllers.login_controller import LoginController

class LoginView:
    def __init__(self):
        self.controller = LoginController()
        # 현재 로그인한 사용자 정보
        self.logged_in_user = None 

    def display(self):
        while True:
            print("=== 로그인 화면 ===")
            email = input("이메일을 입력하세요: ").strip()
            password = input("비밀번호를 입력하세요: ").strip()
            if not email or not password:
                print("이메일과 비밀번호를 모두 입력해주세요.\n")
                continue
            user_data = self.controller.authenticate(email, password)
            if user_data:
                print("로그인 성공!\n")
                # 로그인한 사용자 정보 저장
                self.logged_in_user = user_data
                # Role에 따라 메인 화면 호출
                if self.logged_in_user['Role'] == 'Admin':
                    from Views.Admin.admin_main import AdminMain
                    admin_main = AdminMain(self.logged_in_user)
                    admin_main.display()
                else:
                    #UserMain에 사용자 정보 전달
                    from Views.User.user_main import UserMain
                    user_main = UserMain(self.logged_in_user)
                    user_main.display()
                break
            else:
                print("로그인 실패, 다시 시도하세요.\n")
                retry = input("다시 시도하려면 Enter, 종료하려면 'q'를 입력하세요.").strip().lower()
                if retry == 'q':
                    print("프로그램을 종료합니다.")
                    import sys
                    sys.exit()
                    return "exit"
                


                