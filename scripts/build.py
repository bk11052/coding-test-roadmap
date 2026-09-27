"""Build README.md, curriculum.json and llms.txt from data/*.json.

Usage: python3 scripts/build.py
"""
import json
import pathlib
from urllib.parse import quote

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://bk11052.github.io/coding-test-roadmap"
UPDATED = "2026-09-27"
CHECKED = "2026-09-26"

weeks_raw = json.loads((ROOT / "data" / "weeks.json").read_text())
static = json.loads((ROOT / "data" / "static.json").read_text())

SRC = {"P": "프로그래머스", "C": "코드트리 삼성 기출", "H": "코드트리 HSAT 기출"}
CO = {"samsung": "삼성", "kakao": "카카오", "pg": "네이버·SK·한화·LG 등", "hyundai": "현대차그룹"}
PHASES = ["1–3주 · 기초 체력", "4–8주 · 1순위 유형", "9–12주 · 2순위 유형", "13–16주 · 실전"]
LVMIN = {"LV1": 15, "LV2": 30, "LV3": 50, "LV4": 70, "LV5": 90}


def url(x):
    if x["s"] == "P":
        return f"https://school.programmers.co.kr/learn/courses/30/lessons/{x['id']}"
    kind = "samsung-sw" if x["s"] == "C" else "hsat"
    return f"https://www.codetree.ai/ko/frequent-problems/{kind}/problems/{x['id']}/description"


def est(x, sql=False):
    if x["s"] == "C":
        return 150
    if x["s"] == "H":
        return 60
    if sql:
        return 20 if x["lv"] == "LV3" else 30
    return LVMIN.get(x["lv"], 40)


def fmt_h(m):
    h, r = divmod(m, 60)
    return f"{h}시간 {r}분" if h and r else f"{h}시간" if h else f"{r}분"


def problem(x, sql=False):
    return {"title": x["t"], "platform": SRC[x["s"]], "level": x["lv"], "est_minutes": est(x, sql), "url": url(x)}


weeks = []
for w in weeks_raw:
    sets = []
    if w.get("must"):
        sets.append({"name": "필수", "kind": "required", "problems": [problem(x) for x in w["must"]]})
    if w.get("sql"):
        sets.append({"name": "SQL", "kind": "required", "companies": [CO["pg"]], "problems": [problem(x, True) for x in w["sql"]]})
    for name, items, cos in w.get("groups", []):
        sets.append({"name": name, "kind": "required", "companies": [CO[c] for c in cos], "problems": [problem(x) for x in items]})
    for m in ([w["mock"]] if "mock" in w else []) + w.get("mocks", []):
        sets.append({"name": m["t"], "kind": "mock_exam", "time_limit_minutes": m["min"], "companies": [CO[c] for c in m["co"]], "problems": [problem(x) for x in m["items"]]})
    if w.get("more"):
        sets.append({"name": "도전", "kind": "optional", "problems": [problem(x) for x in w["more"]]})
    core = [p for s in sets if s["kind"] != "optional" for p in s["problems"]]
    weeks.append({
        "week": w["n"], "phase": PHASES[w["ph"]], "topic": w["t"],
        "lectures": [{"title": l["t"], "url": l["u"]} for l in w["lec"]],
        "learn": w["learn"], "common_mistakes": w.get("pit", []), "pass_criterion": w["goal"],
        "required_count": len(core), "optional_count": sum(len(s["problems"]) for s in sets if s["kind"] == "optional"),
        "est_minutes_required": sum(p["est_minutes"] for p in core), "problem_sets": sets,
    })

HOW_TO = "주차마다 강의를 보고 필수 문제를 모두 푼 뒤 통과 기준을 만족하면 다음 주로 넘어갑니다. 도전 문제는 선택입니다. 13~16주는 지원 회사 세트만 골라도 됩니다. 한 문제에 30분 고민해도 방향이 안 잡히면 해설을 보고, 다음 날 해설 없이 다시 풉니다."
NOTICE = "백준(BOJ)은 2026년 4월 28일 서비스를 종료해 현재 채점이 되지 않습니다. 이 커리큘럼의 문제는 모두 프로그래머스와 코드트리 문제입니다."

total = sum(len(s["problems"]) for w in weeks for s in w["problem_sets"])
data = {
    "name": "코딩테스트 로드맵", "site": SITE + "/", "updated": UPDATED, "links_checked": CHECKED, "language": "ko",
    "description": f"국내 대기업 신입 SW 코딩테스트 준비 가이드: 기업별 형식, 출제 유형, 16주 커리큘럼(문제 {total}개)",
    "important_notice": NOTICE, "how_to_use": HOW_TO,
    "est_minutes_rule": "LV1 15분, LV2 30분, LV3 50분, LV4 70분, LV5 90분, 코드트리 삼성 기출 150분, HSAT 기출 60분, SQL LV3 20분·LV4 이상 30분",
    "company_formats": static["company_formats"], "frequency_columns": static["frequency_columns"], "type_frequency": static["type_frequency"],
    "curriculum": weeks, "templates_python": static["templates_python"], "tools": static["tools"],
    "verified_videos": static["verified_videos"], "dropped_claims": static["dropped_claims"], "sources": static["sources"],
}
(ROOT / "curriculum.json").write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")


L = []
A = L.append
A("# 코딩테스트 로드맵\n")
A("국내 대기업 신입 개발자 코딩테스트를 16주 동안 준비하는 계획입니다. 한 주에 한 가지 유형을 공부하고, 프로그래머스와 코드트리 문제 " + str(total) + "개를 풉니다.\n")
A(f"**[대시보드 열기]({SITE}/)** — 지원 회사와 시험 날짜를 넣으면 하루에 풀 문제를 골라 주고, 푼 문제와 복습 일정을 기록합니다.\n")
A(f"> 백준(BOJ)은 2026년 4월 28일 서비스를 종료해 채점이 되지 않습니다. 그래서 모든 문제를 프로그래머스와 코드트리에서 골랐습니다. 문제 링크는 {CHECKED}에 확인했습니다.\n")
A("## 목차\n")
for t_, a in [("사용법", "사용법"), ("AI에게 맡기기", "ai에게-맡기기"), ("16주 계획", "16주-계획"), ("주차별 문제", "주차별-문제"),
              ("기업별 시험 형식", "기업별-시험-형식"), ("자주 나오는 유형", "자주-나오는-유형"), ("외워 둘 코드", "외워-둘-코드"),
              ("공부 도구", "공부-도구"), ("참고 영상", "참고-영상"), ("주의할 정보", "주의할-정보"), ("출처", "출처")]:
    A(f"- [{t_}](#{a})")
A("\n## 사용법\n")
A("1. 한 주에 한 가지 유형을 공부합니다. 강의를 보고, 필수 문제를 모두 풀고, 통과 기준을 확인한 뒤 다음 주로 넘어갑니다.")
A("2. 한 문제에 30분을 고민해도 방향이 보이지 않으면 해설을 봅니다. 해설을 본 문제는 다음 날 다시 풉니다.")
A("3. 13주차부터는 지원할 회사의 기출과 모의고사를 실제 시험 시간에 맞춰 풉니다.\n")
A(f"[대시보드]({SITE}/)를 쓰면 이 과정을 기록할 수 있습니다. 기록은 브라우저에 저장되고, 기기를 바꿀 때는 기록 내보내기와 가져오기를 씁니다.\n")
A("## AI에게 맡기기\n")
A("같은 내용을 AI가 읽기 쉬운 파일로도 올려 두었습니다. Codex, Claude, ChatGPT 같은 AI에게 주소를 주고 계획을 맡길 수 있습니다.\n")
A("| 파일 | 내용 |\n|---|---|")
A(f"| [llms.txt]({SITE}/llms.txt) | 요약과 파일 안내. AI에게 처음 줄 주소 |")
A(f"| [README.md]({SITE}/README.md) | 이 문서 전체 |")
A(f"| [curriculum.json]({SITE}/curriculum.json) | 주차, 문제, 기업 정보를 담은 JSON |\n")
A("예시:\n")
A("```text")
A(f"{SITE}/llms.txt 를 읽고, 5주차까지 끝낸 삼성 지원자에게 이번 주에 풀 문제를 골라 줘.")
A(f"{SITE}/curriculum.json 에서 카카오 관련 필수 문제만 뽑아 하루 2시간 기준 4주 계획으로 짜 줘.")
A("```\n")
A("## 16주 계획\n")
A("| 주차 | 주제 | 필수 | 선택 | 예상 시간 |\n|:--:|---|:--:|:--:|:--:|")
for w in weeks:
    A(f"| [{w['week']:02d}](#week-{w['week']}) | {w['topic']} | {w['required_count']} | {w['optional_count'] or '—'} | {fmt_h(w['est_minutes_required'])} |")
A(f"\n예상 시간은 난이도별 평균입니다. {data['est_minutes_rule']}.\n")
A("## 주차별 문제\n")
last = None
for w in weeks:
    if w["phase"] != last:
        A(f"### {w['phase']}\n")
        last = w["phase"]
    A(f'<a id="week-{w["week"]}"></a>')
    A(f"<details>\n<summary><b>{w['week']:02d}주 · {w['topic']}</b> — 필수 {w['required_count']}문제, 약 {fmt_h(w['est_minutes_required'])}</summary>\n")
    if w["lectures"]:
        A("**강의** " + " · ".join(f"[{l['title']}]({l['url']})" for l in w["lectures"]) + "\n")
    A(f"**배울 것** {w['learn']}\n")
    if w["common_mistakes"]:
        A("**자주 하는 실수**\n")
        for x in w["common_mistakes"]:
            A(f"- {x}")
        A("")
    A(f"**통과 기준** {w['pass_criterion']}\n")
    for s in w["problem_sets"]:
        extra = []
        if s.get("time_limit_minutes"):
            extra.append(f"제한 {fmt_h(s['time_limit_minutes'])}")
        if s.get("companies"):
            extra.append(", ".join(s["companies"]))
        name = {"도전": "선택"}.get(s["name"], s["name"])
        A(f"**{name}**" + (f" ({' · '.join(extra)})" if extra else "") + "\n")
        A("| 문제 | 사이트 | 난이도 | 예상 |\n|---|---|:--:|:--:|")
        for x in s["problems"]:
            A(f"| [{x['title']}]({x['url']}) | {x['platform']} | {x['level']} | {fmt_h(x['est_minutes'])} |")
        A("")
    A("</details>\n")
A("## 기업별 시험 형식\n")
A("최근 응시 후기와 기업 공개 자료를 모았습니다. 형식은 해마다 바뀌니 지원 전에 채용 공고를 확인하세요.\n")
A("| 기업 | 시험 환경 | 구성 | 출제 경향 | 참고 |\n|---|---|---|---|---|")
for c in static["company_formats"]:
    conf = "" if c["confidence"] == "여러 출처 일치" else f" ({c['confidence']})"
    A(f"| {c['company']} | {c['platform']} | {c['format']} | {c['content']} | {c['notes']}{conf} |")
A("\n## 자주 나오는 유형\n")
A("●●● 매우 자주 · ●● 자주 · ● 가끔 · 빈칸은 거의 안 나옴\n")
dot = {"매우 자주": "●●●", "자주": "●●", "가끔": "●", "드묾": "", "없음": ""}
cols = [c.replace(" (SK·한화·LG 등)", "") for c in static["frequency_columns"]]
A("| " + " | ".join(cols) + " |\n|" + "---|" * len(cols))
for r in static["type_frequency"]:
    A("| " + r[0] + " | " + " | ".join(dot.get(v, v) for v in r[1:]) + " |")
A("\n## 외워 둘 코드\n")
A("Python 기준입니다. 16주차에 보지 않고 쓸 수 있는지 확인합니다.\n")
for x in static["templates_python"]:
    A(f"<details>\n<summary>{x['name'].split('. ', 1)[-1]}</summary>\n\n```python\n{x['code']}\n```\n\n</details>\n")
A("## 공부 도구\n")
A("| 이름 | 쓰는 곳 |\n|---|---|")
for x in static["tools"]:
    A(f"| [{x['name']}]({x['url']}) | {x['use']} |")
A("\n## 참고 영상\n")
A("| 영상 | 추천 | 내용 |\n|---|---|---|")
for v in static["verified_videos"]:
    A(f"| [{v['title']}]({v['url']}) ({v['channel']}) | {v['verdict']} | {v['notes']} |")
A("\n## 주의할 정보\n")
A("인터넷에 흔하지만 틀렸거나 오래된 정보입니다.\n")
for x in static["dropped_claims"]:
    A(f"- {x}")
A("\n## 출처\n")
for s in static["sources"]:
    A(f"- [{s['title']}]({s['url']})")
A(f"\n---\n\n문제 저작권은 각 사이트에 있으며, 이 저장소는 링크만 모아 둡니다. 마지막 수정 {UPDATED}.")
(ROOT / "README.md").write_text("\n".join(L) + "\n")

# ---------- dashboard ----------
page = (ROOT / "src" / "page.html").read_text()
app = (ROOT / "src" / "app.js").read_text()
fragment = page.replace("__WEEKS__", json.dumps(weeks_raw, ensure_ascii=False)).replace("__STATIC__", json.dumps(static, ensure_ascii=False)).replace("__APP__", app)
build = ROOT / "build"
build.mkdir(exist_ok=True)
(build / "artifact.html").write_text(fragment)
split = fragment.index('<header class="top">')
index = ("<!doctype html>\n<html lang=\"ko\">\n<head>\n<meta charset=\"utf-8\">\n"
         "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
         "<meta name=\"description\" content=\"국내 대기업 신입 개발자 코딩테스트를 16주 동안 준비하는 계획과 기록 도구\">\n"
         "<link rel=\"alternate\" type=\"text/markdown\" href=\"README.md\">\n"
         + fragment[:split] + "</head>\n<body>\n" + fragment[split:] + "\n</body>\n</html>\n")
(ROOT / "index.html").write_text(index)

(ROOT / "llms.txt").write_text(f"""# 코딩테스트 로드맵

> 국내 대기업 신입 SW 코딩테스트(삼성·카카오·네이버·현대차그룹·SK·LG·한화 등) 준비 가이드. 기업별 시험 형식, 출제 유형 빈도, 16주 커리큘럼(프로그래머스·코드트리 문제 {total}개, 링크 {CHECKED} 확인, 문제별 예상 시간), 주차별 자주 하는 실수, Python 핵심 템플릿. 백준(BOJ)은 2026-04-28 종료되어 사용하지 않음.

## 문서

- [README.md]({SITE}/README.md): 전체 내용을 Markdown으로 정리 (기업 형식표, 유형 빈도, 16주 요약표, 주차별 문제 표, 템플릿, 출처)
- [curriculum.json]({SITE}/curriculum.json): 같은 내용을 구조화한 JSON. 주요 필드: company_formats, type_frequency, curriculum[].problem_sets[].problems[] (title, platform, level, est_minutes, url), curriculum[].common_mistakes, templates_python, sources
- [index.html]({SITE}/): 사람용 대화형 대시보드 (진행 체크·복습 일정·모의고사 타이머, 기록은 브라우저에 저장)

## 사용 안내

- 학습자의 진도(끝낸 주차)와 지원 회사를 물은 뒤, curriculum[] 순서대로 다음 필수 문제를 고르세요.
- 지원 회사별 우선 주차: 삼성 4~8주, 카카오 3·9~12주, 네이버·SK 등 3·9·10·12주, 현대차그룹 4·5·7·9주.
""")
print(f"built: {total} problems, {len(weeks)} weeks")
