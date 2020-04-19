# 파이썬 사용자를 위한 웹 개발 입문

- [장고 프로젝트 만들기](log/make_django_project.md)
- [blog 앱 만들기, Post 모델 만들기, admin에 추가하기](log/make_blog.md)
- [django 지역(시간) 세팅 수정하기, Post 개선하기 str](log/django_time_setting.md)
- [MTV 구조 맛보기 : model, views, templates 사용하기](log/model_views_templates.md)

## ListView 사용하기

- [FBV -> MBV : 블로그 포스트 리스트](log/from_FBV_to_MBV_make_blog_post_list.md)

## Bootstrap 적용

- [static 파일 관리하기 : bootstrap 적용을 위해](log/manage_static_file_to_adapt_bootstrap.md)
- [navigation bar 만들기](log/navigation_bar.md)
- [Bootstrap Grid](log/bootstrap_grid.md)

## static files & Media files
- [CSS 수정하기](log/revise_css.md)
- [사진 업로드를 위한 ImageField와 업로드된 파일 관리 방법](log/ImageField_to_upload_iamge.md)

## 화면 구성 개선하기
- [template(html)에서 if문 사용하기](log/use_if_in_template.md)
- [템플릿에서 truncate로 앞 내용만 보여주기](log/use_truncate.md)

## DetailView 사용하기

- [Post Detail 페이지 만들기](log/make_post_detail.md)

## TDD

- TDD(Test Driven Development 소개)
- [Post List 페이지 테스트 코드 작성하기](log/page_test_code_partA.md)
- [Post Detail 페이지 테스트 코드 작성하기](log/detail_test_code.md)

## HTML 모듈별로 관리하기

- [HTML 분리해서 관리하기](log/divide_html.md)
- [read more 버튼 동작하게 하기, post_detail 페이지 개선하기](log/read_more_button_post_detail.md)

## Relation
- [카테고리, 태그 기능을 위한 django relation 설명 (ForeignKey, ManyToManyField)]


## Relation - ForiegnKey

- [블로그 post에 카테고리 추가하기](log/add_category.md)
- [블로그 post list와 post detail 페이지에 카테고리 추가하기](log/add_category_to_post_list_to_post_detail.md)
- [사소한 문제들 해결: 불필요한 내용 삭제하기; category 복수형 수정하기 (categorys -> categories)](log/revise_category.md)
- [Category 페이지 만들기 (slugField)](log/category_page.md)


## Relation - ManyToManyField

- Tag 모델 설명, 생성 & model test 코드 작성
- Tag: view test 코드 작성
- Tag 페이지 만들기

## Post Detail 페이지 개선하기

- [Post Detail 개선사항 도출하고 Test 코드 만들기](log/revise_post_detail_and_make_test_code.md)
- [마크다운적용하기, tag field에 공란 허용하기](log/adopt_markdown_and_arrow_tag_field_blank.md)
- [Post 수정 화면 / 기능 구현하기](log/revise_post.md)
- [Post 작성 화면 / 기능 구현하기](log/write_post_implement_function.md)
- [로그인 사용자만 접속 가능하게 하기 (LoginRequiredMixin)](log/access_who_login.md)


## Comment(댓글) 구현하기

- [Comment (댓글) 모델 구현하기](log/implement_comment_model.md)
- [Comment (댓글) view 구현하기](log/implement_comment_view.md)
- Comment (댓글) 작성창 구현하기
- Comment 작성일 추가하기, edit, delete 버튼 만들기

## Social Login

- django-allauth로 구글로그인 구현하기
- django-allauth 모양 부트스트랩으로 예쁘게 개선하기
- Comment (댓글) 삭제 기능 추가하기

## Comment 삭제 / 수정 구현하기

- Comment (댓글) 삭제하기 (Delete): CBV (Class Based View) 와 FBV(Function Based View) 비교
- Comment (댓글) 수정하기 (Update)

## 기타 편의성 제공

- 사용자 아바타 보여주기
- 이메일로 가입하기, 로그인하기
- Pagination: 여러페이지일 때 보여주기
- Search 기능 구현하기 (Test)
- Search: 검색 기능 추가하기 (Filter)

## About me 페이지 작성하기

- About me 페이지 작성하기: 불필요한 요소 제거하기, html 요소 include 하기
- About me 페이지 작성하기: 필요한 내용 채워넣기

## 드디어 서비스 제공

- VPS (가상사설서버) 임대하고 Deploy하기 (Vultr)
- VPS에 접속하는 방법: vultr console VS SSH
- VPS로 소스코드 내려받고 서비스 시작하기
- 도메인 구입하고 VPS에 연결하기
- Post Form (Create/Edit)에서 파일 업로드 안되던 버그 수정하기
- 로그인한 사용자만 댓글 남길 수 있게 수정하기
- 실제 서비스 사이트에서 google login 허용하기