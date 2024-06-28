# HotDeal Grouping Project

## :information_source: Introduction
국내 :kr:에 있는 모든 핫딜 게시판을 모아서 한 페이지에서 보고자 시작한 프로젝트입니다.몇 개의 핫딜 게시판부터 시작해서 점차 사이트를 늘릴 예정입니다. 모든 핫딜 게시판을 가지고 있는 사이트와 관리자 그리고 제보해주신 분들꼐 감사드리며, 크롤링을 할때 robots.txt를 보며 작업하지만 그럼에도 불구하고 문제가 생길시 지체 없이 프로젝트 중단 할 것을 약속드립니다.

## :sparkles: Features
- [x] __게시판 미러링__ 
    - [루리웹](https://bbs.ruliweb.com/market/board/1020)
    - [아카라이브](https://arca.live/b/hotdeal)
    - [퀘이사존](https://quasarzone.com/bbs/qb_saleinfo)
    - FM(X)
- [ ] __중복 제거__

## :pushpin: Rules
1. <b>robots.txt를 절대 준수합니다.</b><br>
    다른 무엇보다 중요한 규칙입니다. 각 사이트의 robots.txt를 엄격하게 준수하며, 놓쳤을 경우 제보해주시면 즉각 반영하겠습니다.

## :gear: Local Development
윈도우 환경(WSL) 또는 리눅스 환경에서 실행해주시면 됩니다:

```
docker-compose up -d
```

## :floppy_disk: Dependencies

#### Backend
- Python 3.12.2
- Scrapy 2.11.2
- Poetry
- Duckdb 1.0.0
- FastAPI 0.111.0

#### Frontend
- React 18

#### Build
- Docker-compose
- Nginx

