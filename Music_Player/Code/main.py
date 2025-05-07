from Views.signup import SignupView
from Views.login import LoginView


def main():
    while True:
        print("\n=== 메인 메뉴 ===")
        print("0. 프로그램 종료")
        print("1. 로그인")
        print("2. 회원가입")

        try:
            choice = int(input("원하는 작업을 선택하세요: ").strip())
            if choice == 0:
                print("프로그램을 종료합니다.")
                break
            elif choice == 1:
                login_view = LoginView()
                result = login_view.display()
                if result:
                    print("로그인 성공 ! 다음단계로 이동합니다.")
                elif result == "exit":
                    print("프로그램을 종료합니다.")
            elif choice == 2:
                 signup_view = SignupView()
                 signup_view.display()
            else:
                print("잘못된 입력입니다. 유효한 옵션을 선택하세요.")
        except ValueError:
            print("유효한 숫자를 입력하세요.")



if __name__ == "__main__":
   
    main()