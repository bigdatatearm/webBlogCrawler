# webBlogCrawler
블로그 크롤러

### 가상환경 생성
```bash
$ python -m venv <프로잭트 경로>
```

### 가상환경 활성화
```bash
$ source bin/activate 
```

### 가상환경 패키지 셋팅
```bash
$ pip freeze > requirements.txt
```

### 가상환경 패키지 설치
```bash
$ pip install -r requirements.txt
```


Coding Convention
-------------

### JavaScrypt Style Guide
* Airbnb의 [JavaScript Style Guide](https://github.com/airbnb/javascript)를 따름

### Lint
* [eslint](https://eslint.org/)

### Git
* [git flow](http://danielkummer.github.io/git-flow-cheatsheet/index.html)

* Commit Rule

  - 분류가 될 수 있는 항목을 대괄호 사이에 넣어서 명시적으로 표시
  - Github issue 번호 표시
  - e.g. ```[server, client][#312] Add feature to provide problems API and UI```
  - e.g. ```[server][#317] Fix bug to prevent long response time```
  
