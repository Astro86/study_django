# static File 관리하기 : bootstrap 적용을 위해

https://bootswatch.com/simplex/

## bootstrap을 적용해보기

> blog/templates/blog/post_index.html

### css 파일

```html
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta http-equiv="X-UA-Compatible" content="IE=edge" />
<link rel="stylesheet" href="../4/simplex/bootstrap.css" media="screen" />
<link rel="stylesheet" href="../_assets/css/custom.min.css" />
```

### javascript 파일

> blog/templates/blog/post_index.html

```html
<script src="../_vendor/jquery/dist/jquery.min.js"></script>
<script src="../_vendor/popper.js/dist/umd/popper.min.js"></script>
<script src="../_vendor/bootstrap/dist/js/bootstrap.min.js"></script>
<script src="../_assets/js/custom.js"></script>
```

bootstrap의 javascript를 사용하기 위해서 위 내용을 추가한다.

bootstrap의 style과 javascript를 사용하기 위해서 적용을 해준다.
저렇게 하면 css파일과 javascript파일이 경로가 이상하여 제대로 작동하지 않으므로 수정할 필요가 있다.

## static에 추가된 css파일 적용하기

> static/blog/

static 폴더를 만든 후 blog의 적용할 스타일들을 모아두기 위해 blog폴더를 하나 더 만들어 준다.

> blog/static/blog/bootstrap/bootstrap.css
> blog/static/blog/bootstrap/\_assets/css/custom.min.css

두 파일을 생성해준다.

### static 파일들 불러오기

> blog/templates/blog/post_index.html

```html
<!DOCTYPE html> {% load static %}
```

html 파일이 static 파일들을 가져올 수 있도록 load 명령어를 통해 가져온다.

### bootstrap.css 적용하기

> blog/templates/blog/bootstrap/post_index.html

```html
<!-- <link rel="stylesheet" href="../4/simplex/bootstrap.css" media="screen" /> -->
<link
  rel="stylesheet"
  href="{%static 'blog/bootstrap/bootstrap.css' %}"
  media="screen"
/>
```

### custom.min.css 적용하기

```html
<!-- <link rel="stylesheet" href="../_assets/css/custom.min.css" /> -->
<link rel="stylesheet" href="{%static 'blog/_assets/css/custom.min.css' %}" />
```

## 자바스크립트 경로 수정하기

> blog/static/blog/bootstrap/jqeury.min.js
> blog/static/blog/bootstrap/popper.min.js
> blog/static/blog/bootstrap/bootstrap.min.js
> blog/static/blog/\_assets/js/custom.js

4개의 파일

```django
<!-- <script src="../_vendor/jquery/dist/jquery.min.js"></script> -->
<!-- <script src="../_vendor/popper.js/dist/umd/popper.min.js"></script> -->
<!-- <script src="../_vendor/bootstrap/dist/js/bootstrap.min.js"></script> -->
<!-- <script src="../_assets/js/custom.js"></script> -->

<script src="{% static 'blog/_assets/js/jquery.min.js' %}"></script>
<script src="{% static 'blog/_assets/js/popper.min.js' %}"></script>
<script src="{% static 'blog/bootstrap/bootstrap.min.js' %}"></script>
<script src="{% static 'blog/_assets/js/custom.js' %}"></script>
```
