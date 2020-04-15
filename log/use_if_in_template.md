# template(html)에서 if문 사용하기

## 이미지가 있을 때만 나타내기

```django
{% if p.head_image %}
<img
    class="card-img-top"
    src="{{p.head_image.url}}"
    alt="Card image cap"
/>
{% endif %}
```

`{% if %}`문을 이용하여 처리를 한다.

## Lorem Picsum 이용하기

```django
{% if p.head_image %}
<img
    class="card-img-top"
    src="{{p.head_image.url}}"
    alt="Card image cap"
/>
{% else %}
<img
    class="card-img-top"
    src="https://picsum.photos/seed/picsum/750/300"
    alt="Card image cap"
/>
{% endif %}
```

이미지가 없을 경우 Lorem Picsum으로부터 이미지를 가져온다.
