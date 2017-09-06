# Web
conceptproto : 프로토타입을 python 웹 프레임워크 django로 옮겼습니다. 폴더를 다운받은 후 아래 실행방법에 따라 장고를 설치하고 실행할 수 있습니다.
 - play-static-data에 그래프의 소스 데이터를 json형식으로 저장합니다. 아래에 자세한 설명이 있습니다.
 - 변수는 templates 폴더의 views.py 을 이용해 넘깁니다.

## 실행 방법
0. `conceptproto`폴더 다운로드.
1. `pip install django` 명령어로 장고를 설치합니다.
2. `conceptproto` 디렉토리로 이동한 후 `python manage.py runserver` 명령어로 서버 실행
3. 브라우저에서  `127.0.0.1:8000` 주소로 가면 볼 수 있습니다.

## To Do
- [x] 부트스트랩 말고 semantic.ui 쓰기
- [x] alchemy.js 말고 vis.js 쓰기
- [x] 비디오 아이디에 따라서 웹페이지 만들도록 수정
- [x] 그래프 계층적으로 표현
- [ ] 자막 시각화
- [ ] 클릭 이동 구현

## 데이터 설명
우선 그래프 시각화에 필요한 데이터는 `conceptproto/play/static/play/data` 디렉토리에 있는 아래와 같은 형태의  `비디오아이디.json` 파일을 불러오고 있습니다.

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
        ...
    ],
  "edges": [
        {
            "from": 0,
            "to": 2
        },
        {
            "from": 1,
            "to": 2
        },
        ...
    ]
}
```

예를 들어 `id`가 `bxe2T-V8XRs ` 인 동영상  `bxe2T-V8XRs.json ` 파일은 아래와 같습니다. 

```json
{
    "nodes": [
        {
            "id": 0,
            "label": "Synapse"
        },
        {
            "id": 1,
            "label": "Neuron"
        },
        {
            "id": 2,
            "label": "Artificial_neural_network"
        },
        {
            "id": 3,
            "label": "Deep_learning"
        },
        {
            "id": 4,
            "label": "Sigmoid_function"
        },
        {
            "id": 5,
            "label": "Machine_learning"
        },
        {
            "id": 6,
            "label": "Activation_function"
        },
        {
            "id": 7,
            "label": "Classification"
        },
        {
            "id": 8,
            "label": "Supervised_learning"
        }
    ],
    "edges": [
        {
            "from": 0,
            "to": 2
        },
        {
            "from": 1,
            "to": 2
        },
        {
            "from": 2,
            "to": 3
        },
        {
            "from": 4,
            "to": 6
        },
        {
            "from": 6,
            "to": 3
        },
        {
            "from": 5,
            "to": 7
        },
        {
            "from": 5,
            "to": 8
        },
        {
            "from": 5,
            "to": 3
        }
    ]
}
```

