# 파이썬 사용자를 위한 웹 개발 입문

## 장고 프로젝트 만들기

### 장고 설치하기

```python
pip install django
```

### 장고 프로젝트 시작하기

```python
django-admin startproject mysite
```

### 마이그레이션 파일 생성

```python
python manage.py makemigrations
```

### 마이그레이션 적용

```python
python manage.py migrate
```

- [blog 앱 만들기, Post 모델 만들기, admin에 추가하기](log/make_blog.md)
- [django 지역(시간) 세팅 수정하기, Post 개선하기 str](log/django_time_setting.md)
