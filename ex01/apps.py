from django.apps import AppConfig


class Ex01Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ex01' # 이 이름을 config/settings.py 에 INSTALLED_APPS 에다가  추가를 해줘야 app이 실행이 된다.
    # apps.py 는 앱등록을 위한 기능을 한다
