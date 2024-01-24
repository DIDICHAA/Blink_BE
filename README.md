# Blink BE Repo.
## 👋 팀원 소개
## Moin Back-End 팀
| 이름                        |Email               |
|-----------------------------|--------------------|
| 서지은     | jieun61586@gmail.com |
|이상준    | lsjmc0224@gmail.com |
| 차은호     | eunho2002@dgu.ac.kr |
|전병현    | -|
## Stack
- **server**  
    - django REST framework
## 초기 셋팅
### 1. 가상환경 생성
windows : python -m venv {가상 환경 이름}
mac : python3 -m venv {가상 환경 이름}
- **가상환경 이름은 venv**
- **가상환경 version은 3.11로 통일**
### 2. 가상환경 실행
- windows : source {가상 환경 이름}/Scripts/activate
- mac : source {가상 환경 이름}/bin/activate
### 3. 라이브러리 설치
pip install -r requirements.txt
- **추가된 pip 어쩌구 있으면 'pip freeze > requirements.txt' 명령어 꼭 사용**
### 4. db 마이그레이션 진행
- manage.py 파일이 있는 위치로 이동 후  
    - python manage.py makemigrations  
    - python manage.py migrate
### 4-1. 앱 추가
python manage.py createapp {앱 이름}
### 5. 서버 실행
python manage.py runserver
