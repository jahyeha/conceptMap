# graph-test

그래프 테스트때문에 프로토타입의 장고 `runserver` 하기 번거로워서 그래프 만드는 부분만 페이지 하나로 따로 뺐습니다.

`data.json` 파일에 아래와 같은 형식의 `nodes`,  `edges` 데이터를 넣은 후 `index.html`을 브라우저로 열면 그래프가 그려집니다.



```json
{
  "nodes": [
        {
            "id": 0,
            "label": "concept1"
        },
        {
            "id": 1,
            "label": "concept2"
        },
            {
            "id": 2,
            "label": "concept3"
        }
    ],
  "edges": [
        {
            "from": 0,
            "to": 1
        },
        {
            "from": 1,
            "to": 2
        }
    ]
}
```



