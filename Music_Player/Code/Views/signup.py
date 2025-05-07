from Controllers.signup_controller import SignupController

class SignupView:
    def __init__(self):
        self.controller = SignupController()

    def display(self):
        while True:
            print("=== 회원가입 화면 ===")
            username = input("이름을 입력하세요: ").strip()
            email = input("이메일을 입력하세요: ").strip()
            password = input("비밀번호를 입력하세요: ").strip()
            birthdate = input("생년월일을 입력하세요(ex, yyyy-mm-dd): ")

            if not email or not password or not username or not birthdate:
                print("입력되지 않은 항목이 있습니다.\n")
                continue

            if self.controller.register_user(username, email, password, birthdate):
                print("회원가입 성공!\n")
                return "success"  # 성공하면 다음 단계로 이동
            else:
                print("회원가입 실패, 다시 시도하세요.\n")
                retry = input("다시 시도하려면 Enter, 종료하려면 'q'를 입력하세요.").strip().lower()
                if retry == 'q':
                    return "exit" # 프로그램 종료
                


                
                