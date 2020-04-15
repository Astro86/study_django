# 템플릿에서 truncate로 앞 내용만 보여주기

```django
{{p.content | truncatewords:50}}
```

`truncatewords`를 이용해 50단어만 출력하도록 설정한다.
