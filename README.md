<div align="center">

# 대기업 코테 로드맵

**국내 대기업 신입 SW 코딩테스트를 16주 안에 준비하는 커리큘럼과 대시보드**

![문제](https://img.shields.io/badge/%EB%AC%B8%EC%A0%9C-179%EA%B0%9C-2f5bea) ![기간](https://img.shields.io/badge/%EA%B8%B0%EA%B0%84-16%EC%A3%BC-6a53c9) ![기업](https://img.shields.io/badge/%EA%B8%B0%EC%97%85-10%EA%B3%B3-1d7f55) ![링크 확인](https://img.shields.io/badge/%EB%A7%81%ED%81%AC%20%ED%99%95%EC%9D%B8-2026--09--26-b7730f) ![백준](https://img.shields.io/badge/%EB%B0%B1%EC%A4%80-%EB%AF%B8%EC%82%AC%EC%9A%A9%20%28%EC%84%9C%EB%B9%84%EC%8A%A4%20%EC%A2%85%EB%A3%8C%29-b4323c)

[**대시보드 열기**](https://bk11052.github.io/coding-test-roadmap/) · [AI용 요약 (llms.txt)](https://bk11052.github.io/coding-test-roadmap/llms.txt) · [데이터 (curriculum.json)](https://bk11052.github.io/coding-test-roadmap/curriculum.json)

</div>

> [!IMPORTANT]
> 백준(BOJ)은 2026년 4월 28일 서비스를 종료해 현재 채점이 되지 않습니다. 이 커리큘럼의 문제는 모두 프로그래머스와 코드트리 문제입니다.

## 목차

- [이 저장소 사용법](#이-저장소-사용법)
- [AI로 활용하기](#ai로-활용하기)
- [핵심 요약](#핵심-요약)
- [기업별 시험 형식](#기업별-시험-형식)
- [유형별 출제 빈도](#유형별-출제-빈도)
- [16주 한눈에 보기](#16주-한눈에-보기)
- [주차별 문제](#주차별-문제)
- [핵심 템플릿 (Python)](#핵심-템플릿-python)
- [도구](#도구)
- [검증한 유튜브 영상](#검증한-유튜브-영상)
- [걸러낸 정보](#걸러낸-정보)
- [출처](#출처)

## 이 저장소 사용법

1. **[대시보드](https://bk11052.github.io/coding-test-roadmap/)를 엽니다.** 지원 회사, 시험 날짜, 하루 공부 시간을 넣으면 오늘 풀 문제와 남은 일정을 계산합니다.
2. **주차 순서대로 공부합니다.** 강의를 보고, 필수 문제를 풀고, 통과 기준을 확인합니다. 문제 옆 **기록** 버튼으로 풀이 상태와 메모를 남기면 해설을 본 문제는 1·3·7·14일 뒤 복습으로 다시 나옵니다.
3. **13주차부터 실전입니다.** 지원 회사 기출을 풀고, 모의고사 타이머로 실제 시험 시간에 맞춰 연습합니다.

진행 기록은 브라우저에 저장됩니다. 기기를 바꿀 때는 대시보드의 **기록 내보내기 / 가져오기**를 쓰세요. GitHub에서 직접 볼 때는 아래 주차별 체크박스를 복사해 자기 저장소나 노트에 붙여 쓰면 됩니다.

## AI로 활용하기

HTML을 해석하지 않아도 되도록 같은 내용을 파일 3개로 따로 올렸습니다. Codex, 다른 계정의 Claude, ChatGPT 같은 AI에게 아래 주소 중 하나를 주면 됩니다.

| 파일 | 내용 |
|---|---|
| [`llms.txt`](https://bk11052.github.io/coding-test-roadmap/llms.txt) | 한 문단 요약과 나머지 파일 안내. AI에게 처음 줄 주소로 적당합니다 |
| [`README.md`](https://bk11052.github.io/coding-test-roadmap/README.md) | 전체 내용을 Markdown으로 정리한 이 문서. 주차별 문제 링크, 템플릿, 출처까지 들어 있습니다 |
| [`curriculum.json`](https://bk11052.github.io/coding-test-roadmap/curriculum.json) | 같은 내용을 구조화한 JSON. 프로그램이나 에이전트가 문제 목록을 다룰 때 씁니다 |

이렇게 요청해 보세요.

```text
https://bk11052.github.io/coding-test-roadmap/llms.txt 읽고 내 진도에 맞춰 이번 주 문제 골라 줘. 나는 5주차까지 끝냈고 삼성 지원 예정이야.
https://bk11052.github.io/coding-test-roadmap/curriculum.json 에서 카카오 관련 필수 문제만 뽑아 하루 2시간 기준 4주 계획으로 다시 짜 줘.
README의 7주차 '자주 하는 실수'를 기준으로 내 코드를 검토해 줘. (코드 붙여 넣기)
```

`curriculum.json`의 주요 필드: `company_formats`, `type_frequency`, `curriculum[].problem_sets[].problems[]` (`title`, `platform`, `level`, `est_minutes`, `url`), `curriculum[].common_mistakes`, `templates_python`, `sources`.

## 핵심 요약

- 구현·시뮬레이션과 BFS/DFS가 모든 회사의 공통 뼈대입니다.
- 목표 수준은 백준 기준 골드 4~3입니다.
- 다 풀 필요는 없습니다. 카카오 1차는 7문제 중 3~4솔로 합격한 후기가 있습니다.
- 연습은 프로그래머스(카카오·네이버·SK·한화)와 코드트리(삼성·HSAT)로 합니다.
- 삼성 A형, 현대차 HSAT, PCCP 인증으로 코테를 면제받을 수 있습니다.
- 네이버·카카오 등 대부분은 시험 중 AI 사용을 금지합니다.

## 기업별 시험 형식

| 기업 | 플랫폼 | 구성·시간 | 난이도·유형 | 특이사항 | 신뢰도 |
|---|---|---|---|---|---|
| **삼성전자 (DX·DS SW)** | 자체 시험장 (오프라인) | 2문제 · 4시간 | 1번 복잡한 구현/시뮬레이션, 2번 큰 입력 대비 효율적 탐색. 격자, 회전, 확산, BFS/DFS, 백트래킹 | Java·C++·Python. PyCharm·VS Code 제공. SWEA 상시 A형(2문제·3시간)과 비슷 | 여러 출처 일치 |
| **카카오 (신입크루 공채)** | 프로그래머스 | 1차 7문제 · 5시간 / 2차 알고리즘 5 + CS 12 · 4.5시간 | 1~2번 브론즈, 3~5번 실버~골드, 6~7번 골드 상위. 문자열, 구현, 트리, 그래프. 2차는 백트래킹, 이분탐색, 그리디, 누적합 | 1차 3솔 합격 후기 있음. 2차 영상 감독. 2025년부터 점수 비공개, 검색 제한 | 여러 출처 일치 |
| **네이버 (팀네이버 공채)** | 프로그래머스 | 알고리즘 3 + SQL 1 · 약 2시간, CS 약 20문항 | 실버 상위~골드 4. 한 문제에 여러 알고리즘을 섞음 | C/C++/Java/JS/Python/Swift/Kotlin | 여러 출처 일치 |
| **현대차그룹 (현대차·기아·모비스·오토에버 등)** | Softeer | HSAT 정기 인증 2문제 | 실버~골드. 기초 알고리즘과 구현 | 2문제 모두 맞히면 인증, 2년간 6개 계열사 SW 코테 면제 | 여러 출처 일치 |
| **한화시스템 ICT** | 프로그래머스 | 알고리즘 3 + SQL 1 · 2시간 | 해시 구현, 수학, 부분 문자열(골드 4~5), SQL LV2~3 | 1차 면접에서 코테 1문제 풀이 발표 | 후기 1건 |
| **LG CNS** | 구름 (이전 프로그래머스) | 3문제 | LV2에서 최근 골드 4~3으로 상승. 다익스트라, DP | 2025년 한 차수는 코테 대신 인성 검사 후기 | 후기 1건 |
| **토스** | 자체 | 5문제 · 4시간 | 구현, 자료구조 | 부분 점수 있음 | 후기 1건 |
| **라인** | 프로그래머스 | 3문제 · 2시간 | 브론즈~골드 5 | 신입 공채 빈도 낮음 | 후기 1건 |
| **SK 계열** | 계열사별 상이 | 미확인 | 프로그래머스 기반 알고리즘 코테가 일반적 | 2025년 이후 공개 후기 부족 | 정보 부족 |
| **대한항공·포스코DX·롯데이노베이트 등** | 공고별 상이 | 미확인 | 대체로 실버~골드 하위 | 공개 후기 부족 | 정보 부족 |

지원 전에 반드시 채용 공고를 확인하세요. 신뢰도가 "후기 1건"이나 "정보 부족"인 항목은 달라졌을 수 있습니다.

## 유형별 출제 빈도

| 유형 | 삼성 | 카카오 | 네이버 | 현대차 HSAT | 프로그래머스형 (SK·한화·LG 등) |
|---|---|---|---|---|---|
| **구현·시뮬레이션** | 매우 자주 | 매우 자주 | 자주 | 매우 자주 | 자주 |
| **BFS·DFS** | 매우 자주 | 자주 | 자주 | 자주 | 자주 |
| **완전탐색·백트래킹** | 매우 자주 | 자주 | 가끔 | 자주 | 가끔 |
| **문자열·파싱·해시** | 가끔 | 매우 자주 | 자주 | 가끔 | 매우 자주 |
| **정렬·그리디** | 가끔 | 자주 | 자주 | 자주 | 자주 |
| **이분탐색·투포인터·누적합** | 가끔 | 자주 | 자주 | 가끔 | 자주 |
| **DP** | 가끔 | 자주 | 자주 | 가끔 | 자주 |
| **다익스트라·최단 경로** | 가끔 | 자주 | 가끔 | 가끔 | 가끔 |
| **우선순위 큐·스케줄링** | 가끔 | 자주 | 가끔 | 가끔 | 가끔 |
| **트리·Union-Find** | 드묾 | 자주 | 가끔 | 드묾 | 가끔 |
| **SQL** | 없음 | 없음 | 1문제 | 없음 | 1문제 (한화·금융권) |
| **CS 객관식** | 없음 | 2차에 12문항 | 약 20문항 | 없음 | 드묾 |

여러 후기와 기출 해설을 종합한 정성 평가입니다.

## 16주 한눈에 보기

| 주차 | 주제 | 필수·모의고사 | 도전 | 예상 시간 |
|:--:|---|:--:|:--:|:--:|
| [01](#week-1) | 언어 기본기 · 입출력 · 문자열 | 7 | 2 | 1시간 45분 |
| [02](#week-2) | 시간복잡도 · 배열 · 스택 · 큐 · 덱 | 7 | 3 | 3시간 |
| [03](#week-3) | 해시 · 정렬 | 9 | 3 | 3시간 30분 |
| [04](#week-4) | 재귀 · 완전탐색 · 백트래킹 | 7 | 3 | 3시간 |
| [05](#week-5) | BFS · DFS 기본 | 8 | 2 | 4시간 40분 |
| [06](#week-6) | BFS 심화 · 상태 확장 | 5 | 3 | 3시간 50분 |
| [07](#week-7) | 구현 · 시뮬레이션 1 | 7 | 2 | 9시간 50분 |
| [08](#week-8) | 삼성형 시뮬레이션 2 · 첫 모의고사 | 8 | — | 20시간 |
| [09](#week-9) | 그리디 · 이분탐색 · 투포인터 · 누적합 | 10 | 3 | 6시간 5분 |
| [10](#week-10) | 다이나믹 프로그래밍 | 8 | 3 | 5시간 20분 |
| [11](#week-11) | 그래프 심화 · 우선순위 큐 · 다익스트라 · Union-Find | 8 | 3 | 6시간 |
| [12](#week-12) | 카카오형 문자열 · 파싱 + SQL | 17 | 3 | 7시간 20분 |
| [13](#week-13) | 지원 회사 기출 집중 | 18 | — | 25시간 |
| [14](#week-14) | 실전 모의고사 1 | 13 | — | 11시간 5분 |
| [15](#week-15) | 약점 보완 · 인증 시험 응시 | 6 | — | 7시간 20분 |
| [16](#week-16) | 실전 모의고사 2 · 템플릿 점검 | 11 | — | 10시간 35분 |

예상 시간 기준: LV1 15분, LV2 30분, LV3 50분, LV4 70분, LV5 90분, 코드트리 삼성 기출 150분, HSAT 기출 60분, SQL LV3 20분·LV4 이상 30분.

## 주차별 문제

주차마다 강의를 보고 필수 문제를 모두 푼 뒤 통과 기준을 만족하면 다음 주로 넘어갑니다. 도전 문제는 선택입니다. 13~16주는 지원 회사 세트만 골라도 됩니다. 한 문제에 30분 고민해도 방향이 안 잡히면 해설을 보고, 다음 날 해설 없이 다시 풉니다.

### 1–3주 · 기초 체력

<a id="week-1"></a>
<details>
<summary><b>01주 · 언어 기본기 · 입출력 · 문자열</b> — 필수 7개 · 약 1시간 45분</summary>

**강의:** [이코테 2021 (Python, 나동빈) 재생목록](https://www.youtube.com/playlist?list=PLRx0vPvlEmdAghTr5mXQxGpHjWqSz0dgC) · [바킹독 0x01 기초 코드 작성 요령 I](https://blog.encrypted.gg/922) · [0x02 기초 코드 작성 요령 II](https://blog.encrypted.gg/923)

**익힐 것:** 문자열 슬라이싱·split·join, 정렬 key, 리스트/딕셔너리 컴프리헨션, 날짜·시간 문자열 다루기

**자주 하는 실수**

- 파이썬 문자열에 += 를 반복하면 느립니다. 리스트에 모아 join 하세요
- 대소문자·공백·특수문자 처리 조건을 지문에서 먼저 표시하세요
- 날짜 계산은 윤년과 월별 일수를 확인하세요

**필수**

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [시저 암호](https://school.programmers.co.kr/learn/courses/30/lessons/12926) | 프로그래머스 | LV1 | 15분 |
| ☐ | [이상한 문자 만들기](https://school.programmers.co.kr/learn/courses/30/lessons/12930) | 프로그래머스 | LV1 | 15분 |
| ☐ | [문자열 내 마음대로 정렬하기](https://school.programmers.co.kr/learn/courses/30/lessons/12915) | 프로그래머스 | LV1 | 15분 |
| ☐ | [가장 가까운 같은 글자](https://school.programmers.co.kr/learn/courses/30/lessons/142086) | 프로그래머스 | LV1 | 15분 |
| ☐ | [2016년](https://school.programmers.co.kr/learn/courses/30/lessons/12901) | 프로그래머스 | LV1 | 15분 |
| ☐ | [바탕화면 정리](https://school.programmers.co.kr/learn/courses/30/lessons/161990) | 프로그래머스 | LV1 | 15분 |
| ☐ | [공원 산책](https://school.programmers.co.kr/learn/courses/30/lessons/172928) | 프로그래머스 | LV1 | 15분 |

**도전**

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [[1차] 다트 게임](https://school.programmers.co.kr/learn/courses/30/lessons/17682) | 프로그래머스 | LV1 | 15분 |
| ☐ | [신규 아이디 추천](https://school.programmers.co.kr/learn/courses/30/lessons/72410) | 프로그래머스 | LV1 | 15분 |

**통과 기준:** LV1 문제를 15분 안에 푼다

</details>

<a id="week-2"></a>
<details>
<summary><b>02주 · 시간복잡도 · 배열 · 스택 · 큐 · 덱</b> — 필수 7개 · 약 3시간</summary>

**강의:** [0x03 배열](https://blog.encrypted.gg/927) · [0x05 스택](https://blog.encrypted.gg/933) · [0x06 큐](https://blog.encrypted.gg/934) · [0x07 덱](https://blog.encrypted.gg/935) · [0x08 스택의 활용](https://blog.encrypted.gg/936)

**익힐 것:** deque로 큐 구현, 괄호 짝 검사, 단조 스택(뒤에 있는 큰 수), 큐 시뮬레이션

**자주 하는 실수**

- 빈 스택에서 pop 하기 전에 비었는지 확인하세요
- list.pop(0)은 O(N)입니다. 큐는 deque를 쓰세요
- 시뮬레이션의 시간 단위가 1씩 어긋나지 않는지(off-by-one) 확인하세요

**필수**

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [같은 숫자는 싫어](https://school.programmers.co.kr/learn/courses/30/lessons/12906) | 프로그래머스 | LV1 | 15분 |
| ☐ | [올바른 괄호](https://school.programmers.co.kr/learn/courses/30/lessons/12909) | 프로그래머스 | LV2 | 30분 |
| ☐ | [기능개발](https://school.programmers.co.kr/learn/courses/30/lessons/42586) | 프로그래머스 | LV2 | 30분 |
| ☐ | [프로세스](https://school.programmers.co.kr/learn/courses/30/lessons/42587) | 프로그래머스 | LV2 | 30분 |
| ☐ | [다리를 지나는 트럭](https://school.programmers.co.kr/learn/courses/30/lessons/42583) | 프로그래머스 | LV2 | 30분 |
| ☐ | [괄호 회전하기](https://school.programmers.co.kr/learn/courses/30/lessons/76502) | 프로그래머스 | LV2 | 30분 |
| ☐ | [크레인 인형뽑기 게임](https://school.programmers.co.kr/learn/courses/30/lessons/64061) | 프로그래머스 | LV1 | 15분 |

**도전**

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [주식가격](https://school.programmers.co.kr/learn/courses/30/lessons/42584) | 프로그래머스 | LV2 | 30분 |
| ☐ | [뒤에 있는 큰 수 찾기](https://school.programmers.co.kr/learn/courses/30/lessons/154539) | 프로그래머스 | LV2 | 30분 |
| ☐ | [택배상자](https://school.programmers.co.kr/learn/courses/30/lessons/131704) | 프로그래머스 | LV2 | 30분 |

**통과 기준:** 입력 크기를 보고 허용 복잡도를 바로 말할 수 있다

</details>

<a id="week-3"></a>
<details>
<summary><b>03주 · 해시 · 정렬</b> — 필수 9개 · 약 3시간 30분</summary>

**강의:** [0x15 해시](https://blog.encrypted.gg/1009) · [0x0E 정렬 I](https://blog.encrypted.gg/955) · [0x0F 정렬 II](https://blog.encrypted.gg/966)

**익힐 것:** dict·Counter·defaultdict, set 연산, 정렬 key에 튜플과 음수 쓰기, 커스텀 비교

**자주 하는 실수**

- 없는 키는 dict.get이나 defaultdict로 처리하세요
- 문자열로 된 숫자는 "10" < "9"로 정렬됩니다. 비교 기준을 확인하세요
- 리스트는 해시 키가 될 수 없습니다. tuple로 바꾸세요

**필수**

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [완주하지 못한 선수](https://school.programmers.co.kr/learn/courses/30/lessons/42576) | 프로그래머스 | LV1 | 15분 |
| ☐ | [폰켓몬](https://school.programmers.co.kr/learn/courses/30/lessons/1845) | 프로그래머스 | LV1 | 15분 |
| ☐ | [전화번호 목록](https://school.programmers.co.kr/learn/courses/30/lessons/42577) | 프로그래머스 | LV2 | 30분 |
| ☐ | [의상](https://school.programmers.co.kr/learn/courses/30/lessons/42578) | 프로그래머스 | LV2 | 30분 |
| ☐ | [K번째수](https://school.programmers.co.kr/learn/courses/30/lessons/42748) | 프로그래머스 | LV1 | 15분 |
| ☐ | [가장 큰 수](https://school.programmers.co.kr/learn/courses/30/lessons/42746) | 프로그래머스 | LV2 | 30분 |
| ☐ | [H-Index](https://school.programmers.co.kr/learn/courses/30/lessons/42747) | 프로그래머스 | LV2 | 30분 |
| ☐ | [신고 결과 받기](https://school.programmers.co.kr/learn/courses/30/lessons/92334) | 프로그래머스 | LV1 | 15분 |
| ☐ | [오픈채팅방](https://school.programmers.co.kr/learn/courses/30/lessons/42888) | 프로그래머스 | LV2 | 30분 |

**도전**

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [베스트앨범](https://school.programmers.co.kr/learn/courses/30/lessons/42579) | 프로그래머스 | LV3 | 50분 |
| ☐ | [달리기 경주](https://school.programmers.co.kr/learn/courses/30/lessons/178871) | 프로그래머스 | LV1 | 15분 |
| ☐ | [[3차] 파일명 정렬](https://school.programmers.co.kr/learn/courses/30/lessons/17686) | 프로그래머스 | LV2 | 30분 |

**통과 기준:** 해시로 집계하고, 기준이 여러 개인 정렬을 막힘없이 쓴다

</details>

### 4–8주 · 1순위 유형

<a id="week-4"></a>
<details>
<summary><b>04주 · 재귀 · 완전탐색 · 백트래킹</b> — 필수 7개 · 약 3시간</summary>

**강의:** [0x0B 재귀](https://blog.encrypted.gg/943) · [0x0C 백트래킹](https://blog.encrypted.gg/945)

**익힐 것:** itertools permutations/combinations/product, 재귀로 직접 구현(넣기→재귀→빼기), 가지치기

**자주 하는 실수**

- 재귀에서 돌아올 때 방문 표시·선택을 되돌렸는지 확인하세요
- 조합은 시작 인덱스를 넘겨야 중복이 생기지 않습니다
- 경우의 수가 입력 크기로 감당되는지 먼저 계산하세요

**필수**

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [모의고사](https://school.programmers.co.kr/learn/courses/30/lessons/42840) | 프로그래머스 | LV1 | 15분 |
| ☐ | [최소직사각형](https://school.programmers.co.kr/learn/courses/30/lessons/86491) | 프로그래머스 | LV1 | 15분 |
| ☐ | [카펫](https://school.programmers.co.kr/learn/courses/30/lessons/42842) | 프로그래머스 | LV2 | 30분 |
| ☐ | [소수 찾기](https://school.programmers.co.kr/learn/courses/30/lessons/42839) | 프로그래머스 | LV2 | 30분 |
| ☐ | [피로도](https://school.programmers.co.kr/learn/courses/30/lessons/87946) | 프로그래머스 | LV2 | 30분 |
| ☐ | [모음사전](https://school.programmers.co.kr/learn/courses/30/lessons/84512) | 프로그래머스 | LV2 | 30분 |
| ☐ | [N-Queen](https://school.programmers.co.kr/learn/courses/30/lessons/12952) | 프로그래머스 | LV2 | 30분 |

**도전**

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [양궁대회](https://school.programmers.co.kr/learn/courses/30/lessons/92342) | 프로그래머스 | LV2 | 30분 |
| ☐ | [이모티콘 할인행사](https://school.programmers.co.kr/learn/courses/30/lessons/150368) | 프로그래머스 | LV2 | 30분 |
| ☐ | [불량 사용자](https://school.programmers.co.kr/learn/courses/30/lessons/64064) | 프로그래머스 | LV3 | 50분 |

**통과 기준:** 순열·조합·부분집합을 템플릿 없이 5분 안에 쓴다

</details>

<a id="week-5"></a>
<details>
<summary><b>05주 · BFS · DFS 기본</b> — 필수 8개 · 약 4시간 40분</summary>

**강의:** [0x09 BFS](https://blog.encrypted.gg/941) · [0x0A DFS](https://blog.encrypted.gg/942)

**익힐 것:** 방향 배열 dy/dx, 범위 체크, 방문 처리는 큐에 넣을 때, 거리 배열 -1 초기화, 여러 시작점 동시 BFS

**자주 하는 실수**

- 방문 표시는 큐에 넣을 때 하세요. 꺼낼 때 하면 중복으로 들어갑니다
- 행(N)과 열(M), 좌표 (y, x) 순서가 뒤바뀌지 않았는지 확인하세요
- Python 재귀 DFS는 setrecursionlimit이 필요합니다

**필수**

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [타겟 넘버](https://school.programmers.co.kr/learn/courses/30/lessons/43165) | 프로그래머스 | LV2 | 30분 |
| ☐ | [네트워크](https://school.programmers.co.kr/learn/courses/30/lessons/43162) | 프로그래머스 | LV3 | 50분 |
| ☐ | [게임 맵 최단거리](https://school.programmers.co.kr/learn/courses/30/lessons/1844) | 프로그래머스 | LV2 | 30분 |
| ☐ | [단어 변환](https://school.programmers.co.kr/learn/courses/30/lessons/43163) | 프로그래머스 | LV3 | 50분 |
| ☐ | [무인도 여행](https://school.programmers.co.kr/learn/courses/30/lessons/154540) | 프로그래머스 | LV2 | 30분 |
| ☐ | [미로 탈출](https://school.programmers.co.kr/learn/courses/30/lessons/159993) | 프로그래머스 | LV2 | 30분 |
| ☐ | [리코쳇 로봇](https://school.programmers.co.kr/learn/courses/30/lessons/169199) | 프로그래머스 | LV2 | 30분 |
| ☐ | [전력망을 둘로 나누기](https://school.programmers.co.kr/learn/courses/30/lessons/86971) | 프로그래머스 | LV2 | 30분 |

**도전**

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [거리두기 확인하기](https://school.programmers.co.kr/learn/courses/30/lessons/81302) | 프로그래머스 | LV2 | 30분 |
| ☐ | [외벽 점검](https://school.programmers.co.kr/learn/courses/30/lessons/60062) | 프로그래머스 | LV3 | 50분 |

**통과 기준:** 격자 BFS 최단 거리와 연결 요소 세기를 10분 안에 쓴다

</details>

<a id="week-6"></a>
<details>
<summary><b>06주 · BFS 심화 · 상태 확장</b> — 필수 5개 · 약 3시간 50분</summary>

**강의:** [0x09 BFS 후반부 (벽 부수기 유형)](https://blog.encrypted.gg/941) · [최백준 특강 (다리 K개 미로)](https://youtu.be/iVfgiqM4has)

**익힐 것:** visited[r][c][k] 설계, 방향을 상태로 넣기, 0-1 BFS, 좌표 2배 확대(아이템 줍기)

**자주 하는 실수**

- 같은 칸이라도 추가 상태(부순 횟수·방향)가 다르면 다른 정점입니다
- 상태를 늘리면 메모리가 N×M×K로 커집니다. 범위를 확인하세요
- 가중치가 0과 1로 섞이면 일반 BFS가 아니라 0-1 BFS나 다익스트라입니다

**필수**

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [여행경로](https://school.programmers.co.kr/learn/courses/30/lessons/43164) | 프로그래머스 | LV3 | 50분 |
| ☐ | [아이템 줍기](https://school.programmers.co.kr/learn/courses/30/lessons/87694) | 프로그래머스 | LV3 | 50분 |
| ☐ | [경주로 건설](https://school.programmers.co.kr/learn/courses/30/lessons/67259) | 프로그래머스 | LV3 | 50분 |
| ☐ | [숫자 변환하기](https://school.programmers.co.kr/learn/courses/30/lessons/154538) | 프로그래머스 | LV2 | 30분 |
| ☐ | [부대복귀](https://school.programmers.co.kr/learn/courses/30/lessons/132266) | 프로그래머스 | LV3 | 50분 |

**도전**

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [퍼즐 조각 채우기](https://school.programmers.co.kr/learn/courses/30/lessons/84021) | 프로그래머스 | LV3 | 50분 |
| ☐ | [카드 짝 맞추기](https://school.programmers.co.kr/learn/courses/30/lessons/72415) | 프로그래머스 | LV3 | 50분 |
| ☐ | [블록 이동하기](https://school.programmers.co.kr/learn/courses/30/lessons/60063) | 프로그래머스 | LV3 | 50분 |

**통과 기준:** 방문 배열에 (행, 열, 추가 상태)를 넣는 문제를 알아본다

</details>

<a id="week-7"></a>
<details>
<summary><b>07주 · 구현 · 시뮬레이션 1</b> — 필수 7개 · 약 9시간 50분</summary>

**강의:** [0x0D 시뮬레이션](https://blog.encrypted.gg/948) · [큰돌의터전 삼성 기출 분석](https://youtu.be/w9dyVCvFCkw)

**익힐 것:** 90도 회전 b[j][n-1-i]=a[i][j], 동시 처리는 임시 배열, 상태 변수 먼저 정의, 단계마다 출력해 확인

**자주 하는 실수**

- "동시에" 일어나는 변화를 순서대로 처리하면 틀립니다. 임시 배열을 쓰세요
- 직사각형을 회전하면 N×M이 M×N이 됩니다
- 격자 밖으로 나갈 때 규칙(멈춤, 튕김, 반대편)을 지문에서 확인하세요

**필수**

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [삼각 달팽이](https://school.programmers.co.kr/learn/courses/30/lessons/68645) | 프로그래머스 | LV2 | 30분 |
| ☐ | [방문 길이](https://school.programmers.co.kr/learn/courses/30/lessons/49994) | 프로그래머스 | LV2 | 30분 |
| ☐ | [[1차] 프렌즈4블록](https://school.programmers.co.kr/learn/courses/30/lessons/17679) | 프로그래머스 | LV2 | 30분 |
| ☐ | [자물쇠와 열쇠](https://school.programmers.co.kr/learn/courses/30/lessons/60059) | 프로그래머스 | LV3 | 50분 |
| ☐ | [회전하는 빙하](https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/rotating-glacier/description) | 코드트리 삼성 기출 | 삼성 기출 | 2시간 30분 |
| ☐ | [바이러스 실험](https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/virus-experiment/description) | 코드트리 삼성 기출 | 삼성 기출 | 2시간 30분 |
| ☐ | [2048 게임](https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/2048-game/description) | 코드트리 삼성 기출 | 삼성 기출 | 2시간 30분 |

**도전**

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [기둥과 보 설치](https://school.programmers.co.kr/learn/courses/30/lessons/60061) | 프로그래머스 | LV3 | 50분 |
| ☐ | [n^2 배열 자르기](https://school.programmers.co.kr/learn/courses/30/lessons/87390) | 프로그래머스 | LV2 | 30분 |

**통과 기준:** 지문을 단계별 함수로 나눠 LV2 구현을 40분 안에 푼다

</details>

<a id="week-8"></a>
<details>
<summary><b>08주 · 삼성형 시뮬레이션 2 · 첫 모의고사</b> — 필수 8개 · 약 20시간</summary>

**강의:** [코드트리 기출 문제 목록](https://www.codetree.ai/ko/frequent-problems)

**익힐 것:** 문제를 읽고 30분 동안 설계(상태, 순서, 함수)만 하고, 그다음 코딩합니다. 디버깅은 단계별 격자 출력으로

**자주 하는 실수**

- 설계 없이 바로 코딩하면 디버깅에 시간을 다 씁니다. 30분은 설계하세요
- 동점일 때의 우선순위 규칙(행 작은 순, 열 작은 순 등)을 빠뜨리기 쉽습니다
- 한 문제에 3시간 넘게 쓰지 않도록 시간을 나눠 두세요

**필수**

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [나무박멸](https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/tree-kill-all/description) | 코드트리 삼성 기출 | 삼성 기출 | 2시간 30분 |
| ☐ | [예술성](https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/artistry/description) | 코드트리 삼성 기출 | 삼성 기출 | 2시간 30분 |
| ☐ | [꼬리잡기놀이](https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/tail-catch-play/description) | 코드트리 삼성 기출 | 삼성 기출 | 2시간 30분 |
| ☐ | [싸움땅](https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/battle-ground/description) | 코드트리 삼성 기출 | 삼성 기출 | 2시간 30분 |
| ☐ | [코드트리 빵](https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/codetree-mon-bread/description) | 코드트리 삼성 기출 | 삼성 기출 | 2시간 30분 |
| ☐ | [메이즈 러너](https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/maze-runner/description) | 코드트리 삼성 기출 | 삼성 기출 | 2시간 30분 |

**모의고사 · 2문제 4시간** (제한 4시간 · 삼성)

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [포탑 부수기](https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/destroy-the-turret/description) | 코드트리 삼성 기출 | 삼성 기출 | 2시간 30분 |
| ☐ | [루돌프의 반란](https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/rudolph-rebellion/description) | 코드트리 삼성 기출 | 삼성 기출 | 2시간 30분 |

**통과 기준:** 삼성 기출 1문제를 2시간 안에 완주한다

</details>

### 9–12주 · 2순위 유형

<a id="week-9"></a>
<details>
<summary><b>09주 · 그리디 · 이분탐색 · 투포인터 · 누적합</b> — 필수 10개 · 약 6시간 5분</summary>

**강의:** [0x11 그리디](https://blog.encrypted.gg/975) · [0x13 이분탐색](https://blog.encrypted.gg/985) · [0x14 투 포인터](https://blog.encrypted.gg/1004)

**익힐 것:** 정렬 후 그리디, bisect, 매개변수 탐색, 슬라이딩 윈도우, 1차원·2차원 누적합(차분 배열)

**자주 하는 실수**

- 그리디는 반례를 하나 찾아보고 확신한 뒤 쓰세요
- 이분탐색 무한 루프: lo < hi 조건과 mid 계산 방향을 맞추세요
- 답의 범위 상한을 너무 작게 잡지 마세요 (예: 10^18)

**필수**

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [체육복](https://school.programmers.co.kr/learn/courses/30/lessons/42862) | 프로그래머스 | LV1 | 15분 |
| ☐ | [구명보트](https://school.programmers.co.kr/learn/courses/30/lessons/42885) | 프로그래머스 | LV2 | 30분 |
| ☐ | [큰 수 만들기](https://school.programmers.co.kr/learn/courses/30/lessons/42883) | 프로그래머스 | LV2 | 30분 |
| ☐ | [단속카메라](https://school.programmers.co.kr/learn/courses/30/lessons/42884) | 프로그래머스 | LV3 | 50분 |
| ☐ | [요격 시스템](https://school.programmers.co.kr/learn/courses/30/lessons/181188) | 프로그래머스 | LV2 | 30분 |
| ☐ | [입국심사](https://school.programmers.co.kr/learn/courses/30/lessons/43238) | 프로그래머스 | LV3 | 50분 |
| ☐ | [징검다리 건너기](https://school.programmers.co.kr/learn/courses/30/lessons/64062) | 프로그래머스 | LV3 | 50분 |
| ☐ | [연속된 부분 수열의 합](https://school.programmers.co.kr/learn/courses/30/lessons/178870) | 프로그래머스 | LV2 | 30분 |
| ☐ | [보석 쇼핑](https://school.programmers.co.kr/learn/courses/30/lessons/67258) | 프로그래머스 | LV3 | 50분 |
| ☐ | [연속 부분 수열 합의 개수](https://school.programmers.co.kr/learn/courses/30/lessons/131701) | 프로그래머스 | LV2 | 30분 |

**도전**

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [징검다리](https://school.programmers.co.kr/learn/courses/30/lessons/43236) | 프로그래머스 | LV4 | 1시간 10분 |
| ☐ | [파괴되지 않은 건물](https://school.programmers.co.kr/learn/courses/30/lessons/92344) | 프로그래머스 | LV3 | 50분 |
| ☐ | [광고 삽입](https://school.programmers.co.kr/learn/courses/30/lessons/72414) | 프로그래머스 | LV3 | 50분 |

**통과 기준:** "답을 정하고 가능한지 검사"하는 매개변수 탐색을 쓴다

</details>

<a id="week-10"></a>
<details>
<summary><b>10주 · 다이나믹 프로그래밍</b> — 필수 8개 · 약 5시간 20분</summary>

**강의:** [0x10 다이나믹 프로그래밍](https://blog.encrypted.gg/974)

**익힐 것:** 테이블 정의 → 점화식 → 초기값 순서. 배낭, LIS, 격자 경로, 원형 배열 처리

**자주 하는 실수**

- 테이블의 의미와 초기값(기저)을 먼저 적으세요
- 0/1 배낭을 1차원으로 쓸 때는 용량을 역순으로 돌아야 합니다
- 나머지 연산 지시가 있으면 매 단계에서 나누세요

**필수**

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [멀리 뛰기](https://school.programmers.co.kr/learn/courses/30/lessons/12914) | 프로그래머스 | LV2 | 30분 |
| ☐ | [2 x n 타일링](https://school.programmers.co.kr/learn/courses/30/lessons/12900) | 프로그래머스 | LV2 | 30분 |
| ☐ | [땅따먹기](https://school.programmers.co.kr/learn/courses/30/lessons/12913) | 프로그래머스 | LV2 | 30분 |
| ☐ | [정수 삼각형](https://school.programmers.co.kr/learn/courses/30/lessons/43105) | 프로그래머스 | LV3 | 50분 |
| ☐ | [등굣길](https://school.programmers.co.kr/learn/courses/30/lessons/42898) | 프로그래머스 | LV3 | 50분 |
| ☐ | [가장 큰 정사각형 찾기](https://school.programmers.co.kr/learn/courses/30/lessons/12905) | 프로그래머스 | LV2 | 30분 |
| ☐ | [거스름돈](https://school.programmers.co.kr/learn/courses/30/lessons/12907) | 프로그래머스 | LV3 | 50분 |
| ☐ | [N으로 표현](https://school.programmers.co.kr/learn/courses/30/lessons/42895) | 프로그래머스 | LV3 | 50분 |

**도전**

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [도둑질](https://school.programmers.co.kr/learn/courses/30/lessons/42897) | 프로그래머스 | LV4 | 1시간 10분 |
| ☐ | [코딩 테스트 공부](https://school.programmers.co.kr/learn/courses/30/lessons/118668) | 프로그래머스 | LV3 | 50분 |
| ☐ | [연속 펄스 부분 수열의 합](https://school.programmers.co.kr/learn/courses/30/lessons/161988) | 프로그래머스 | LV3 | 50분 |

**통과 기준:** 점화식을 말로 먼저 쓰고 코드로 옮긴다

</details>

<a id="week-11"></a>
<details>
<summary><b>11주 · 그래프 심화 · 우선순위 큐 · 다익스트라 · Union-Find</b> — 필수 8개 · 약 6시간</summary>

**강의:** [0x17 우선순위 큐](https://blog.encrypted.gg/1015) · [0x18 그래프](https://blog.encrypted.gg/1016) · [0x19 트리](https://blog.encrypted.gg/1019) · [0x1D 다익스트라](https://blog.encrypted.gg/1037) · [부록 D Union-Find](https://blog.encrypted.gg/1097)

**익힐 것:** heapq, 다익스트라(거리 비교로 오래된 항목 건너뛰기), 플로이드, Union-Find 경로 압축, 크루스칼

**자주 하는 실수**

- 다익스트라는 음수 가중치에서 쓸 수 없습니다
- 무방향 그래프는 간선을 양쪽에 넣으세요
- 노드 번호가 1부터인지 0부터인지 확인하세요

**필수**

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [더 맵게](https://school.programmers.co.kr/learn/courses/30/lessons/42626) | 프로그래머스 | LV2 | 30분 |
| ☐ | [이중우선순위큐](https://school.programmers.co.kr/learn/courses/30/lessons/42628) | 프로그래머스 | LV3 | 50분 |
| ☐ | [디스크 컨트롤러](https://school.programmers.co.kr/learn/courses/30/lessons/42627) | 프로그래머스 | LV3 | 50분 |
| ☐ | [가장 먼 노드](https://school.programmers.co.kr/learn/courses/30/lessons/49189) | 프로그래머스 | LV3 | 50분 |
| ☐ | [배달](https://school.programmers.co.kr/learn/courses/30/lessons/12978) | 프로그래머스 | LV2 | 30분 |
| ☐ | [합승 택시 요금](https://school.programmers.co.kr/learn/courses/30/lessons/72413) | 프로그래머스 | LV3 | 50분 |
| ☐ | [섬 연결하기](https://school.programmers.co.kr/learn/courses/30/lessons/42861) | 프로그래머스 | LV3 | 50분 |
| ☐ | [순위](https://school.programmers.co.kr/learn/courses/30/lessons/49191) | 프로그래머스 | LV3 | 50분 |

**도전**

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [등산코스 정하기](https://school.programmers.co.kr/learn/courses/30/lessons/118669) | 프로그래머스 | LV3 | 50분 |
| ☐ | [길 찾기 게임](https://school.programmers.co.kr/learn/courses/30/lessons/42892) | 프로그래머스 | LV3 | 50분 |
| ☐ | [호텔 방 배정](https://school.programmers.co.kr/learn/courses/30/lessons/64063) | 프로그래머스 | LV4 | 1시간 10분 |

**통과 기준:** 다익스트라와 Union-Find를 보지 않고 쓴다

</details>

<a id="week-12"></a>
<details>
<summary><b>12주 · 카카오형 문자열 · 파싱 + SQL</b> — 필수 17개 · 약 7시간 20분</summary>

**강의:** [부록 A 문자열 기초](https://blog.encrypted.gg/1081) · [프로그래머스 SQL 고득점 Kit](https://school.programmers.co.kr/learn/challenges?tab=sql_practice_kit)

**익힐 것:** 시간 문자열 → 분 변환, 정규식, 진법 변환, 집합 연산. SQL은 GROUP BY·HAVING, JOIN, 서브쿼리, 날짜 함수, 재귀 CTE

**자주 하는 실수**

- 시간 문자열은 분이나 초 단위 정수로 바꿔 계산하세요
- SQL에서 NULL 비교는 = 가 아니라 IS NULL입니다
- GROUP BY에 없는 컬럼을 SELECT 하지 마세요

**필수**

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [문자열 압축](https://school.programmers.co.kr/learn/courses/30/lessons/60057) | 프로그래머스 | LV2 | 30분 |
| ☐ | [괄호 변환](https://school.programmers.co.kr/learn/courses/30/lessons/60058) | 프로그래머스 | LV2 | 30분 |
| ☐ | [[1차] 뉴스 클러스터링](https://school.programmers.co.kr/learn/courses/30/lessons/17677) | 프로그래머스 | LV2 | 30분 |
| ☐ | [[1차] 캐시](https://school.programmers.co.kr/learn/courses/30/lessons/17680) | 프로그래머스 | LV2 | 30분 |
| ☐ | [주차 요금 계산](https://school.programmers.co.kr/learn/courses/30/lessons/92341) | 프로그래머스 | LV2 | 30분 |
| ☐ | [k진수에서 소수 개수 구하기](https://school.programmers.co.kr/learn/courses/30/lessons/92335) | 프로그래머스 | LV2 | 30분 |
| ☐ | [메뉴 리뉴얼](https://school.programmers.co.kr/learn/courses/30/lessons/72411) | 프로그래머스 | LV2 | 30분 |
| ☐ | [튜플](https://school.programmers.co.kr/learn/courses/30/lessons/64065) | 프로그래머스 | LV2 | 30분 |
| ☐ | [개인정보 수집 유효기간](https://school.programmers.co.kr/learn/courses/30/lessons/150370) | 프로그래머스 | LV1 | 15분 |
| ☐ | [가장 많이 받은 선물](https://school.programmers.co.kr/learn/courses/30/lessons/258712) | 프로그래머스 | LV1 | 15분 |

**SQL** (네이버·SK·한화·LG 등)

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [즐겨찾기가 가장 많은 식당 정보 출력하기](https://school.programmers.co.kr/learn/courses/30/lessons/131123) | 프로그래머스 | LV3 | 20분 |
| ☐ | [카테고리 별 도서 판매량 집계하기](https://school.programmers.co.kr/learn/courses/30/lessons/144855) | 프로그래머스 | LV3 | 20분 |
| ☐ | [대여 횟수가 많은 자동차들의 월별 대여 횟수 구하기](https://school.programmers.co.kr/learn/courses/30/lessons/151139) | 프로그래머스 | LV3 | 20분 |
| ☐ | [자동차 대여 기록에서 대여중 / 대여 가능 여부 구분하기](https://school.programmers.co.kr/learn/courses/30/lessons/157340) | 프로그래머스 | LV3 | 20분 |
| ☐ | [년, 월, 성별 별 상품 구매 회원 수 구하기](https://school.programmers.co.kr/learn/courses/30/lessons/131532) | 프로그래머스 | LV4 | 30분 |
| ☐ | [연간 평가점수에 해당하는 평가 등급 및 성과금 조회하기](https://school.programmers.co.kr/learn/courses/30/lessons/284528) | 프로그래머스 | LV4 | 30분 |
| ☐ | [특정 세대의 대장균 찾기](https://school.programmers.co.kr/learn/courses/30/lessons/301650) | 프로그래머스 | LV4 | 30분 |

**도전**

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [순위 검색](https://school.programmers.co.kr/learn/courses/30/lessons/72412) | 프로그래머스 | LV2 | 30분 |
| ☐ | [[3차] 방금그곡](https://school.programmers.co.kr/learn/courses/30/lessons/17683) | 프로그래머스 | LV2 | 30분 |
| ☐ | [표 편집](https://school.programmers.co.kr/learn/courses/30/lessons/81303) | 프로그래머스 | LV3 | 50분 |

**통과 기준:** 긴 지문을 요구사항 목록으로 바꾼 뒤 코딩한다

</details>

### 13–16주 · 실전

<a id="week-13"></a>
<details>
<summary><b>13주 · 지원 회사 기출 집중</b> — 필수 18개 · 약 25시간</summary>

**강의:** [2026 카카오 1차 공식 해설](https://tech.kakao.com/posts/813) · [2026 카카오 2차 공식 해설](https://tech.kakao.com/posts/814)

**익힐 것:** 삼성·카카오·현대 중 지원하는 곳만 골라 푸세요. 시간은 실제 시험의 절반 비율로 잽니다

**자주 하는 실수**

- 기출은 실제 시간의 절반 비율로 잽니다
- 같은 회사 기출은 비슷한 구조가 반복됩니다. 공통 패턴을 메모하세요

**삼성** (삼성)

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [마법의 숲 탐색](https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/magical-forest-exploration/description) | 코드트리 삼성 기출 | 삼성 기출 | 2시간 30분 |
| ☐ | [고대 문명 유적 탐사](https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/ancient-ruin-exploration/description) | 코드트리 삼성 기출 | 삼성 기출 | 2시간 30분 |
| ☐ | [메두사와 전사들](https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/medusa-and-warriors/description) | 코드트리 삼성 기출 | 삼성 기출 | 2시간 30분 |
| ☐ | [미생물 연구](https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/microbial-research/description) | 코드트리 삼성 기출 | 삼성 기출 | 2시간 30분 |
| ☐ | [민트 초코 우유](https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/mint-choco-milk/description) | 코드트리 삼성 기출 | 삼성 기출 | 2시간 30분 |
| ☐ | [왕실의 기사 대결](https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/royal-knight-duel/description) | 코드트리 삼성 기출 | 삼성 기출 | 2시간 30분 |

**카카오** (카카오)

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [택배 배달과 수거하기](https://school.programmers.co.kr/learn/courses/30/lessons/150369) | 프로그래머스 | LV2 | 30분 |
| ☐ | [미로 탈출 명령어](https://school.programmers.co.kr/learn/courses/30/lessons/150365) | 프로그래머스 | LV3 | 50분 |
| ☐ | [표현 가능한 이진트리](https://school.programmers.co.kr/learn/courses/30/lessons/150367) | 프로그래머스 | LV3 | 50분 |
| ☐ | [표 병합](https://school.programmers.co.kr/learn/courses/30/lessons/150366) | 프로그래머스 | LV3 | 50분 |
| ☐ | [도넛과 막대 그래프](https://school.programmers.co.kr/learn/courses/30/lessons/258711) | 프로그래머스 | LV2 | 30분 |
| ☐ | [주사위 고르기](https://school.programmers.co.kr/learn/courses/30/lessons/258709) | 프로그래머스 | LV3 | 50분 |
| ☐ | [산 모양 타일링](https://school.programmers.co.kr/learn/courses/30/lessons/258705) | 프로그래머스 | LV3 | 50분 |
| ☐ | [n + 1 카드게임](https://school.programmers.co.kr/learn/courses/30/lessons/258707) | 프로그래머스 | LV3 | 50분 |

**현대차그룹** (현대차그룹)

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [편안한 워크숍](https://www.codetree.ai/ko/frequent-problems/hsat/problems/easy-workshop/description) | 코드트리 HSAT 기출 | HSAT 기출 | 1시간 |
| ☐ | [디지털 로직 패턴 검사](https://www.codetree.ai/ko/frequent-problems/hsat/problems/check-digital-logic-pattern/description) | 코드트리 HSAT 기출 | HSAT 기출 | 1시간 |
| ☐ | [배터리 효율 최적화 하기](https://www.codetree.ai/ko/frequent-problems/hsat/problems/optimizing-battery-efficiency/description) | 코드트리 HSAT 기출 | HSAT 기출 | 1시간 |
| ☐ | [도로 보수 로봇](https://www.codetree.ai/ko/frequent-problems/hsat/problems/road-repair-robot/description) | 코드트리 HSAT 기출 | HSAT 기출 | 1시간 |

**통과 기준:** 지원하는 회사의 최근 기출을 시간 재고 푼다

</details>

<a id="week-14"></a>
<details>
<summary><b>14주 · 실전 모의고사 1</b> — 필수 13개 · 약 11시간 5분</summary>

**익힐 것:** 휴대폰을 멀리 두고, 시작 10분 동안 전체를 훑어 순서를 정합니다. 끝나면 문제별로 쓴 시간과 막힌 지점을 기록하세요

**자주 하는 실수**

- 쉬운 문제부터 확실히 맞히고, 어려운 문제는 부분 점수를 노리세요
- 끝나면 문제별로 쓴 시간과 막힌 지점을 기록하세요

**카카오 2026 공채 1차 실제 기출 · 7문제 5시간** (제한 5시간 · 카카오)

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [노란불 신호등](https://school.programmers.co.kr/learn/courses/30/lessons/468371) | 프로그래머스 | LV1 | 15분 |
| ☐ | [중요한 단어를 스포 방지](https://school.programmers.co.kr/learn/courses/30/lessons/468370) | 프로그래머스 | LV1 | 15분 |
| ☐ | [바이러스 파이프](https://school.programmers.co.kr/learn/courses/30/lessons/468373) | 프로그래머스 | LV2 | 30분 |
| ☐ | [리프 노드 수 최대화](https://school.programmers.co.kr/learn/courses/30/lessons/468372) | 프로그래머스 | LV2 | 30분 |
| ☐ | [발전소 회로 복구](https://school.programmers.co.kr/learn/courses/30/lessons/468375) | 프로그래머스 | LV3 | 50분 |
| ☐ | [최고 속도](https://school.programmers.co.kr/learn/courses/30/lessons/468376) | 프로그래머스 | LV3 | 50분 |
| ☐ | [카카오 앱 정리하기](https://school.programmers.co.kr/learn/courses/30/lessons/468374) | 프로그래머스 | LV3 | 50분 |

**PCCP 세트 A · 4문제 120분** (제한 2시간 · 네이버·SK·한화·LG 등, 카카오, 현대차그룹)

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [[PCCP 기출문제] 1번 / 붕대 감기](https://school.programmers.co.kr/learn/courses/30/lessons/250137) | 프로그래머스 | LV1 | 15분 |
| ☐ | [[PCCP 기출문제] 2번 / 석유 시추](https://school.programmers.co.kr/learn/courses/30/lessons/250136) | 프로그래머스 | LV2 | 30분 |
| ☐ | [[PCCP 기출문제] 3번 / 아날로그 시계](https://school.programmers.co.kr/learn/courses/30/lessons/250135) | 프로그래머스 | LV2 | 30분 |
| ☐ | [[PCCP 기출문제] 4번 / 수레 움직이기](https://school.programmers.co.kr/learn/courses/30/lessons/250134) | 프로그래머스 | LV3 | 50분 |

**삼성 2025 하반기 · 2문제 4시간** (제한 4시간 · 삼성)

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [가로등 설치](https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/street-light-installation/description) | 코드트리 삼성 기출 | 삼성 기출 | 2시간 30분 |
| ☐ | [AI 로봇청소기](https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/ai-robot/description) | 코드트리 삼성 기출 | 삼성 기출 | 2시간 30분 |

**통과 기준:** 실제 시험과 같은 시간·환경으로 한 번 치른다

</details>

<a id="week-15"></a>
<details>
<summary><b>15주 · 약점 보완 · 인증 시험 응시</b> — 필수 6개 · 약 7시간 20분</summary>

**강의:** [Softeer HSAT 접수](https://softeer.ai) · [PCCP 접수](https://certi.programmers.co.kr/about/pccp) · [SWEA 상시 역량테스트](https://swexpertacademy.com)

**익힐 것:** 오답 노트에서 가장 많이 틀린 유형의 "도전" 문제를 다시 풉니다. 지원 회사에 맞는 인증 시험을 이 주에 응시하세요

**자주 하는 실수**

- 인증 시험은 실제 채용 코테와 같은 긴장감으로 치르세요

**보충 (삼성)** (삼성)

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [팩맨](https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/pacman/description) | 코드트리 삼성 기출 | 삼성 기출 | 2시간 30분 |
| ☐ | [술래잡기](https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/hide-and-seek/description) | 코드트리 삼성 기출 | 삼성 기출 | 2시간 30분 |

**보충 (카카오 기출)** (카카오)

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [두 큐 합 같게 만들기](https://school.programmers.co.kr/learn/courses/30/lessons/118667) | 프로그래머스 | LV2 | 30분 |
| ☐ | [수식 최대화](https://school.programmers.co.kr/learn/courses/30/lessons/67257) | 프로그래머스 | LV2 | 30분 |
| ☐ | [후보키](https://school.programmers.co.kr/learn/courses/30/lessons/42890) | 프로그래머스 | LV2 | 30분 |
| ☐ | [[1차] 셔틀버스](https://school.programmers.co.kr/learn/courses/30/lessons/17678) | 프로그래머스 | LV3 | 50분 |

**통과 기준:** 오답 노트 상위 2개 유형을 다시 풀고 인증을 딴다

</details>

<a id="week-16"></a>
<details>
<summary><b>16주 · 실전 모의고사 2 · 템플릿 점검</b> — 필수 11개 · 약 10시간 35분</summary>

**익힐 것:** 아래 "핵심 템플릿" 7종을 빈 파일에 외워서 써 보고, 모의고사로 마무리합니다

**자주 하는 실수**

- 템플릿을 외워서 쓰되, 문제에 맞게 고치는 연습을 함께 하세요

**카카오 2026 공채 2차 실제 기출 · 5문제 4시간 30분 (CS 제외)** (제한 4시간 30분 · 카카오)

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [선인장 숨기기](https://school.programmers.co.kr/learn/courses/30/lessons/468379) | 프로그래머스 | LV2 | 30분 |
| ☐ | [힌트 스테이지](https://school.programmers.co.kr/learn/courses/30/lessons/468377) | 프로그래머스 | LV2 | 30분 |
| ☐ | [기차 선로](https://school.programmers.co.kr/learn/courses/30/lessons/468381) | 프로그래머스 | LV3 | 50분 |
| ☐ | [제곱 개수 배열](https://school.programmers.co.kr/learn/courses/30/lessons/468380) | 프로그래머스 | LV3 | 50분 |
| ☐ | [보물 찾기](https://school.programmers.co.kr/learn/courses/30/lessons/468378) | 프로그래머스 | LV3 | 50분 |

**PCCP 세트 B · 4문제 120분** (제한 2시간 · 네이버·SK·한화·LG 등, 카카오, 현대차그룹)

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [[PCCP 기출문제] 1번 / 동영상 재생기](https://school.programmers.co.kr/learn/courses/30/lessons/340213) | 프로그래머스 | LV1 | 15분 |
| ☐ | [[PCCP 기출문제] 2번 / 퍼즐 게임 챌린지](https://school.programmers.co.kr/learn/courses/30/lessons/340212) | 프로그래머스 | LV2 | 30분 |
| ☐ | [[PCCP 기출문제] 3번 / 충돌위험 찾기](https://school.programmers.co.kr/learn/courses/30/lessons/340211) | 프로그래머스 | LV2 | 30분 |
| ☐ | [[PCCP 기출문제] 4번 / 수식 복원하기](https://school.programmers.co.kr/learn/courses/30/lessons/340210) | 프로그래머스 | LV3 | 50분 |

**삼성 2025 하반기 · 2문제 4시간** (제한 4시간 · 삼성)

| | 문제 | 플랫폼 | 난이도 | 예상 |
|:--:|---|---|:--:|:--:|
| ☐ | [해적 선장 코디](https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/pirate-captain-coddy/description) | 코드트리 삼성 기출 | 삼성 기출 | 2시간 30분 |
| ☐ | [택배 하차](https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/delivery-service/description) | 코드트리 삼성 기출 | 삼성 기출 | 2시간 30분 |

**통과 기준:** 템플릿 7종을 보지 않고 5분 안에 쓴다

</details>

## 핵심 템플릿 (Python)

16주차 점검 대상입니다. 보지 않고 5분 안에 쓸 수 있을 때까지 반복하세요.

<details>
<summary><b>매일 공부 루틴 (2~3시간)
        강의 30분 → 필수 문제 2개 → 전날 틀린 문제 1개 다시 풀기
        30분 고민해도 방향이 안 잡히면 해설을 보고, 다음 날 해설 없이 다시 풉니다
        맞힌 문제도 프로그래머스 "다른 사람의 풀이"를 한 개 읽습니다
        오답 노트에는 "왜 틀렸나"를 한 줄로 적습니다. 예: 범위 체크 누락, 동시 처리 순서
      시간이 4주뿐이라면
        1주: 4·5주차 필수 문제 (백트래킹, BFS/DFS)
        2주: 7·8주차 필수 문제 (구현·시뮬레이션)
        3주: 13주차 중 지원 회사 기출만
        4주: 14·16주차 모의고사 중 지원 회사 세트
        DP·그래프 심화는 과감히 건너뜁니다
      언어 선택
        Python: 구현이 빠르고 문자열 처리가 편해 카카오·네이버형에 유리합니다. 삼성 SW역량테스트 B형(Pro)은 Python 응시가 불가합니다
        C++ / Java: 속도가 안정적이고 삼성 B형 이상을 노린다면 필수입니다
        바킹독 강의는 C++이지만 파이썬·자바 코드가 추가됐습니다. Python이라면 이코테 소스코드도 함께 보세요
    
  

  
    핵심 템플릿 7종16주차 점검 대상입니다. Python 기준입니다. 보지 않고 5분 안에 쓸 수 있을 때까지 반복하세요.
    
      1. 격자 BFS 최단 거리</b></summary>

```python
from collections import deque
def bfs(sr, sc, grid):
    n, m = len(grid), len(grid[0])
    dist = [[-1]*m for _ in range(n)]
    dist[sr][sc] = 0
    q = deque([(sr, sc)])
    while q:
        r, c = q.popleft()
        for dr, dc in ((-1,0),(1,0),(0,-1),(0,1)):
            nr, nc = r+dr, c+dc
            if 0 <= nr < n and 0 <= nc < m \
               and grid[nr][nc] != '#' and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                q.append((nr, nc))
    return dist
```

</details>

<details>
<summary><b>2. 조합 백트래킹 (넣기 → 재귀 → 빼기)</b></summary>

```python
def comb(start, picked):
    if len(picked) == k:
        answers.append(picked[:])
        return
    for i in range(start, n):
        picked.append(arr[i])
        comb(i + 1, picked)
        picked.pop()
# 순열이면 used 배열로 모든 i를 돌고,
# 간단하면 itertools.combinations / permutations
```

</details>

<details>
<summary><b>3. 격자 회전 · 동시 갱신</b></summary>

```python
# 시계 방향 90도: b[j][n-1-i] = a[i][j]
def rotate(a):
    n = len(a)
    return [[a[n-1-j][i] for j in range(n)] for i in range(n)]
# 파이썬 한 줄: list(map(list, zip(*a[::-1])))

# "동시에" 퍼진다 → 새 배열에 모았다가 한 번에 교체
nxt = [row[:] for row in board]
# ... board를 읽고 nxt에 쓰기 ...
board = nxt
```

</details>

<details>
<summary><b>4. 매개변수 탐색 (이분탐색)</b></summary>

```python
def ok(x):          # x로 조건을 만족하는가?
    ...
lo, hi = 0, 10**18
while lo < hi:          # 조건을 만족하는 최솟값
    mid = (lo + hi) // 2
    if ok(mid): hi = mid
    else: lo = mid + 1
answer = lo
```

</details>

<details>
<summary><b>5. 다익스트라</b></summary>

```python
import heapq
def dijkstra(start, adj, n):
    INF = float('inf')
    dist = [INF] * n
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]: continue     # 오래된 항목
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(pq, (dist[v], v))
    return dist
```

</details>

<details>
<summary><b>6. Union-Find</b></summary>

```python
parent = list(range(n))
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]   # 경로 압축
        x = parent[x]
    return x
def union(a, b):
    a, b = find(a), find(b)
    if a == b: return False
    parent[b] = a
    return True
```

</details>

<details>
<summary><b>7. 누적합 · 2차원 차분 배열</b></summary>

```python
# 1차원 구간합
pre = [0]
for x in arr: pre.append(pre[-1] + x)
# arr[l..r] 합 = pre[r+1] - pre[l]

# 2차원 구간에 +v를 한꺼번에 (파괴되지 않은 건물)
d[r1][c1] += v; d[r1][c2+1] -= v
d[r2+1][c1] -= v; d[r2+1][c2+1] += v
# 행 방향, 열 방향으로 한 번씩 누적하면 완성
```

</details>

<details>
<summary><b>시작 코드 (Python 공통)</b></summary>

```python
import sys
input = sys.stdin.readline          # 입력이 많을 때
sys.setrecursionlimit(10**6)        # 깊은 재귀 DFS
from collections import deque, defaultdict, Counter
from itertools import permutations, combinations, product
import heapq, bisect
```

</details>

## 도구

| 도구 | 용도 |
|---|---|
| [프로그래머스](https://school.programmers.co.kr/learn/challenges) | 카카오·네이버·SK·한화 실제 시험 플랫폼. 카카오 기출, 고득점 Kit, SQL Kit, PCCP 기출 |
| [코드트리](https://www.codetree.ai/ko/frequent-problems) | 삼성 SW역량테스트 기출 복원, HSAT 기출 |
| [바킹독 실전 알고리즘](https://github.com/encrypted-def/basic-algo-lecture) | 무료 강의. 커리큘럼 강의 링크. 글 속 문제집은 백준 기반이라 현재 채점 불가 |
| [이코테 2021 (Python)](https://github.com/ndb796/python-for-coding-test) | 나동빈 《이것이 취업을 위한 코딩 테스트다》 소스코드와 강의 |
| [SW Expert Academy](https://swexpertacademy.com) | 삼성 상시 역량테스트 A형(2문제·3시간), B형(1문제·4시간, Python 불가) |
| [Softeer](https://softeer.ai) | 현대차그룹 HSAT 인증 (2년간 코테 면제) |
| [PCCP](https://certi.programmers.co.kr/about/pccp) | 4문제·120분, 5만 원. 일부 기업 LV.2 이상 코테 면제 |
| [백준 BOJ](https://www.acmicpc.net) | 2026-04-28 서비스 종료. 현재 채점 불가 (재개 예고만 있음) |

## 검증한 유튜브 영상

자막 전체를 읽고 확인했습니다.

| 영상 | 채널 | 판정 | 메모 |
|---|---|---|---|
| [2026년 코딩테스트 준비, 딱 정해드립니다](https://youtu.be/iWJUA78Fb8c) | 개발남노씨 | **먼저 보기** | 우선순위(구현·완전탐색·BFS/DFS → DP·다익스트라)와 10^8≈1초 기준은 정확. "1순위만 하면 대부분 통과"는 과장. 끝은 강의 홍보 |
| [2026 삼성전자 코딩테스트 기출 분석](https://youtu.be/w9dyVCvFCkw) | 큰돌의터전 | **삼성 지원자 필수** | 회전 공식, dy/dx, 동시 확산은 임시 배열, 조합 재귀, 끝값 반례. 예시는 C++ |
| [백준의 코딩테스트 벼락치기 · 2025 대기업 코테 풀이 특강](https://youtu.be/iVfgiqM4has) | 제로베이스 (출연 최백준) | **중급 이후** | 상태 BFS(행, 열, 다리 사용 횟수) 설명이 핵심. 실제 기출 아님. 첫 문제 풀이는 N=10^5에서 O(N^2) 위험 |
| [코딩테스트 벼락치기 · 2026 필수 코테 3문제](https://youtu.be/x0j8M4_-wT0) | 제로베이스 (출연 최백준) | **입문~중급** | 제약 조건으로 완전탐색 가능 여부 판단, 출력 디버깅 시연. 실버 수준 |
| [독학으로 코딩 테스트를 준비한다면](https://youtu.be/jDjs1NsCPo4) | 개발자 강민철 | **입문자만** | 일반론. 후반은 엘리스 광고. "1~2시간 고민"은 취업 준비엔 길다고 판단 |

## 걸러낸 정보

조사하면서 틀렸거나, 오래됐거나, 근거가 약하다고 판단해 넣지 않았거나 고친 내용입니다.

- "1순위(구현·BFS/DFS)만 하면 대부분 통과" — 과장. 카카오 2차·네이버는 이분탐색·그리디·누적합·SQL도 나옴
- "카카오 코테 인터넷 검색 가능, 점수 공개" — 2024년 이전 정보. 2025년부터 검색 제한·점수 비공개
- "네이버 코테 40분 내외" — 검색 요약에만 있고 실제 후기(약 2시간)와 모순
- "벼락치기 3문제", "10년치 패턴만 알면 된다" — 홍보 문구
- "삼성은 제출 시간도 평가" — 단일 후기, 공식 근거 없음
- "AI 허용 기업 34%" 등 비율 — 해외 설문 재인용, 국내와 무관
- "한 문제당 1~2시간 고민" — 취업 준비엔 30~45분 후 해설 권장
- 백준 기반 기존 가이드 — 백준 종료로 모든 문제를 프로그래머스·코드트리로 교체

## 출처

- [2025 상반기 삼성전자 SW역량테스트 후기](https://velog.io/@crm03008/2025-%EC%83%81%EB%B0%98%EA%B8%B0%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90-%EA%B0%9C%EB%B0%9C-%EC%A7%81%EB%AC%B4-SW%EC%97%AD%EB%9F%89%ED%85%8C%EC%8A%A4%ED%8A%B8-%ED%9B%84%EA%B8%B0)
- [2026 카카오 1차 문제해설 (tech.kakao.com)](https://tech.kakao.com/posts/813)
- [2026 카카오 2차 문제해설](https://tech.kakao.com/posts/814)
- [2026 카카오 신입공채 코딩 테스트 후기](https://velog.io/@pcjo1202/%ED%9B%84%EA%B8%B0-2026-%EC%B9%B4%EC%B9%B4%EC%98%A4-%EC%8B%A0%EC%9E%85%EA%B3%B5%EC%B1%84-%EC%BD%94%EB%94%A9-%ED%85%8C%EC%8A%A4%ED%8A%B8-%ED%9B%84%EA%B8%B0)
- [회사별 코딩테스트 스타일 및 후기](https://velog.io/@soonyoung/%ED%9A%8C%EC%82%AC%EB%B3%84-%EC%BD%94%EB%94%A9%ED%85%8C%EC%8A%A4%ED%8A%B8-%EC%8A%A4%ED%83%80%EC%9D%BC-%EB%B0%8F-%ED%9B%84%EA%B8%B0)
- [2025 네이버 신입공채 CS & 코딩테스트 후기](https://blog.similarchart.com/259)
- [Softeer HSAT 안내 (서울대 CSE)](https://cse.snu.ac.kr/en/community/notice/21926)
- [한화시스템 ICT 25년 하반기 후기](https://velog.io/@dbwls89173/%ED%95%9C%ED%99%94%EC%8B%9C%EC%8A%A4%ED%85%9C-ICT-25%EB%85%84-%ED%95%98%EB%B0%98%EA%B8%B0-%EC%84%9C%EB%B9%84%EC%8A%A4-%EA%B0%9C%EB%B0%9C-%EC%9A%B4%EC%98%81-%EC%B1%84%EC%9A%A9-%ED%9B%84%EA%B8%B0)
- [LG CNS 합격 후기 (자소설닷컴)](https://jasoseol.com/blog/post/lg-cns-%ED%95%A9%EA%B2%A9-%ED%9B%84%EA%B8%B0-%EC%9E%90%EC%86%8C%EC%84%9C-%EC%9D%B8%EC%A0%81%EC%84%B1-%EB%A9%B4%EC%A0%91-%EC%A7%88%EB%AC%B8-%EC%BD%94%EB%94%A9%ED%85%8C%EC%8A%A4%ED%8A%B8-%EC%9E%90/)
- [삼성 SW 역량테스트 A형·B형 후기](https://applelime.github.io/review/2022-03-27-review-samsung-sw-competency-test/)
- [PCCP 시험 소개](https://certi.programmers.co.kr/about/pccp)
- [AI 활용 코딩 테스트 분석 2026 (잡코리아)](https://www.jobkorea.co.kr/goodjob/tip/view?News_No=22546)
- [백준 서비스 종료 (kitpa)](https://kitpa.org/news/1366)
- [BOJ 인수·재개 예고 (kitpa)](https://kitpa.org/news/1640)
- [BOJ 서비스 종료에 따른 안내 (바킹독)](https://blog.encrypted.gg/1108)

---

문제 저작권은 각 플랫폼(프로그래머스, 코드트리)에 있으며 이 저장소는 링크만 제공합니다. 채용 형식은 해마다 바뀌므로 지원 전 채용 공고를 최종 기준으로 삼으세요. 최종 업데이트 2026-09-27.
