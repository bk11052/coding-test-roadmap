"""Build README.md, curriculum.json and llms.txt from data/*.json.

Usage: python3 scripts/build.py
"""
import json
import re
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


def lec_tag(u):
    if "blog.encrypted.gg" in u:
        return "바킹독 · 글과 영상 · C++"
    if "PLRx0vPvlEmd" in u:
        return "나동빈 · 영상 · Python"
    if "youtu" in u:
        return "유튜브 영상"
    if "tech.kakao.com" in u:
        return "카카오 공식 해설"
    if "sql_practice_kit" in u:
        return "프로그래머스 문제 모음"
    if "frequent-problems" in u:
        return "코드트리 기출 목록"
    if "hyundai-ngv" in u:
        return "현대차그룹 HSAT"
    return "접수 페이지"


def fmt_h(m):
    h, r = divmod(m, 60)
    return f"{h}시간 {r}분" if h and r else f"{h}시간" if h else f"{r}분"


def problem(x, sql=False):
    p = {"title": x["t"], "platform": SRC[x["s"]], "level": x["lv"], "est_minutes": est(x, sql), "url": url(x)}
    if x.get("sol"):
        p["solution_url"] = x["sol"]
    return p


weeks = []
for w in weeks_raw:
    sets = []
    if w.get("must"):
        sets.append({"name": "필수", "kind": "required", "problems": [problem(x) for x in w["must"]]})
    if w.get("sql"):
        sets.append({"name": "SQL", "kind": "required", "companies": [CO["pg"]], "problems": [problem(x, True) for x in w["sql"]]})
    for g in w.get("groups", []):
        name, items, cos = g[0], g[1], g[2]
        kind = "optional" if len(g) > 3 and g[3] == "more" else "required"
        sets.append({"name": name, "kind": kind, "companies": [CO[c] for c in cos], "problems": [problem(x) for x in items]})
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
    "signals": [{"clue": s, "method": m, "week": n} for s, m, n in static["signals"]], "io_formats": static["io_formats"], "python_pitfalls": [{"case": a, "code": c, "note": n} for a, c, n in static["cheats"]], "myths": static["myths"], "sources": static["sources"],
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
              ("기업별 시험 형식", "기업별-시험-형식"), ("자주 나오는 유형", "자주-나오는-유형"), ("문제 보고 방법 고르기", "문제-보고-방법-고르기"),
              ("사이트별 입출력 형식", "사이트별-입출력-형식"), ("Python에서 자주 틀리는 것", "python에서-자주-틀리는-것"),
              ("외워 둘 코드", "외워-둘-코드"), ("공부 도구", "공부-도구"), ("흔한 오해", "흔한-오해"), ("출처", "출처"),
              ("기여", "기여"), ("라이선스", "라이선스")]:
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
        study = w["week"] <= 12
        A(f"**{'개념 강의' if study else '참고 링크'}**" + (" — 먼저 보고 아래 문제를 푸세요." if study else "") + "\n")
        for l in w["lectures"]:
            A(f"- [{l['title']}]({l['url']}) ({lec_tag(l['url'])})")
        baek = [l for l in w["lectures"] if "blog.encrypted.gg" in l["url"]]
        if study and baek:
            has_py = any(re.search(r"0x([0-9A-Fa-f]{2})", l["title"]) and int(re.search(r"0x([0-9A-Fa-f]{2})", l["title"]).group(1), 16) <= 0x11 for l in baek)
            A("- 바킹독 강의의 예제 코드는 C++입니다."
              + (" Python으로 보려면 같은 예제를 Python으로 푼 [풀이 모음](https://github.com/hanXen/basic-algo-lecture-python)을 참고하세요." if has_py else "")
              + " 강의 끝의 연습 문제는 백준 문제라 지금은 채점이 안 되니 건너뜁니다.")
        A("")
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
        has_sol = any("solution_url" in x for x in s["problems"])
        A("| 문제 | 사이트 | 난이도 | 예상 |" + (" 해설 |" if has_sol else "") + "\n|---|---|:--:|:--:|" + (":--:|" if has_sol else ""))
        for x in s["problems"]:
            sol = (f" [카카오 해설]({x['solution_url']}) |" if "solution_url" in x else " |") if has_sol else ""
            A(f"| [{x['title']}]({x['url']}) | {x['platform']} | {x['level']} | {fmt_h(x['est_minutes'])} |{sol}")
        A("")
    A("</details>\n")
A("## 기업별 시험 형식\n")
A("최근 응시 후기와 기업 공개 자료를 모았습니다. 형식은 해마다 바뀌니 지원 전에 채용 공고를 확인하세요.\n")
A("| 기업 | 시험 환경 | 구성 | 출제 경향 | 참고 | 근거 시점 |\n|---|---|---|---|---|---|")
for c in static["company_formats"]:
    conf = "" if c["confidence"] == "여러 출처 일치" else f" ({c['confidence']})"
    A(f"| {c['company']} | {c['platform']} | {c['format']} | {c['content']} | {c['notes']}{conf} | {c.get('basis', '—')} |")
A("\n## 자주 나오는 유형\n")
A("●●● 매우 자주 · ●● 자주 · ● 가끔 · 빈칸은 거의 안 나옴\n")
dot = {"매우 자주": "●●●", "자주": "●●", "가끔": "●", "드묾": "", "없음": ""}
cols = [c.replace(" (SK·한화·LG 등)", "") for c in static["frequency_columns"]]
A("| " + " | ".join(cols) + " |\n|" + "---|" * len(cols))
for r in static["type_frequency"]:
    A("| " + r[0] + " | " + " | ".join(dot.get(v, v) for v in r[1:]) + " |")
A("\n## 문제 보고 방법 고르기\n")
A("| 지문의 단서 | 떠올릴 방법 | 배우는 주차 |\n|---|---|:--:|")
for sgn, m, n in static["signals"]:
    A(f"| {sgn} | **{m}** | [{n:02d}주](#week-{n}) |")
A("\n## 사이트별 입출력 형식\n")
for f in static["io_formats"]:
    A(f"**{f['site']}** — {f['how']}\n\n```python\n{f['code']}\n```\n")
    if f.get("java"):
        A(f"<details>\n<summary>Java{(' — ' + f['how_java']) if f.get('how_java') else ''}</summary>\n\n```java\n{f['java']}\n```\n\n</details>\n")
A("## Python에서 자주 틀리는 것\n")
A("| 상황 | 코드 | 설명 |\n|---|---|---|")
for a, c, n in static["cheats"]:
    A(f"| {a} | `{c}` | {n} |")
A("\n## 외워 둘 코드\n")
A("Python과 Java로 적었습니다. 16주차에 보지 않고 쓸 수 있는지 확인합니다.\n")
for x in static["templates_python"]:
    A(f"<details>\n<summary>{x['name'].split('. ', 1)[-1]}</summary>\n\n```python\n{x['code']}\n```\n" + (f"\n```java\n{x['java']}\n```\n" if x.get("java") else "") + "\n</details>\n")
A("## 공부 도구\n")
A("| 이름 | 쓰는 곳 |\n|---|---|")
for x in static["tools"]:
    A(f"| [{x['name']}]({x['url']}) | {x['use']} |")
A("\n## 흔한 오해\n")
for x in static["myths"]:
    A(f"- {x}")
A("\n## 출처\n")
for s in static["sources"]:
    A(f"- [{s['title']}]({s['url']})")
A("\n## 기여\n")
A("- 기업 시험 형식이 바뀌었다면 [후기 제보](https://github.com/bk11052/coding-test-roadmap/issues/new?template=company-report.yml)로 알려 주세요.")
A("- 열리지 않는 링크는 [링크 오류 신고](https://github.com/bk11052/coding-test-roadmap/issues/new?template=broken-link.yml)로 알려 주세요. 매주 자동 점검도 돌고 있습니다.")
A("- 내용은 `data/`, 대시보드는 `src/`를 고친 뒤 `python3 scripts/build.py`를 실행하면 README, curriculum.json, llms.txt, index.html이 함께 만들어집니다.")
A("\n## 라이선스\n")
A("코드(`src/`, `scripts/`, 외워 둘 코드)는 [MIT](LICENSE), 글과 데이터는 [CC BY 4.0](LICENSE-CONTENT)입니다. 출처를 밝히면 자유롭게 쓰고 고칠 수 있습니다. 링크한 문제의 저작권은 각 사이트에 있습니다.")
A(f"\n---\n\n마지막 수정 {UPDATED}.")
(ROOT / "README.md").write_text("\n".join(L) + "\n")

# ---------- dashboard ----------
page = (ROOT / "src" / "page.html").read_text()
app = (ROOT / "src" / "app.js").read_text()
fragment = page.replace("__WEEKS__", json.dumps(weeks_raw, ensure_ascii=False)).replace("__STATIC__", json.dumps(static, ensure_ascii=False)).replace("__APP__", app)
build = ROOT / "build"
build.mkdir(exist_ok=True)
(build / "artifact.html").write_text(fragment)
split = fragment.index('<div class="shell">')
index = ("<!doctype html>\n<html lang=\"ko\">\n<head>\n<meta charset=\"utf-8\">\n"
         "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
         "<meta name=\"description\" content=\"국내 대기업 신입 개발자 코딩테스트를 16주 동안 준비하는 계획과 기록 도구\">\n"
         "<link rel=\"alternate\" type=\"text/markdown\" href=\"README.md\">\n"
         "<link rel=\"icon\" href=\"favicon.svg\" type=\"image/svg+xml\">\n"
         f"<meta property=\"og:type\" content=\"website\">\n<meta property=\"og:url\" content=\"{SITE}/\">\n"
         "<meta property=\"og:title\" content=\"코딩테스트 로드맵\">\n"
         "<meta property=\"og:description\" content=\"국내 대기업 신입 개발자 코딩테스트를 16주 동안 준비하는 계획과 기록 도구\">\n"
         f"<meta property=\"og:image\" content=\"{SITE}/og.png\">\n<meta property=\"og:image:width\" content=\"1200\">\n<meta property=\"og:image:height\" content=\"630\">\n"
         "<meta name=\"twitter:card\" content=\"summary_large_image\">\n"
         "<script data-goatcounter=\"https://coding-test-roadmap.goatcounter.com/count\" data-goatcounter-settings='{\"no_onload\": true}' async src=\"https://gc.zgo.at/count.js\"></script>\n"
         + fragment[:split] + "</head>\n<body>\n" + fragment[split:] + "\n</body>\n</html>\n")
(ROOT / "index.html").write_text(index)

(ROOT / "llms.txt").write_text(f"""# 코딩테스트 로드맵

> 국내 대기업 신입 SW 코딩테스트(삼성·카카오·네이버·현대차그룹·SK·LG·한화 등) 준비 가이드. 기업별 시험 형식, 출제 유형 빈도, 16주 커리큘럼(프로그래머스·코드트리 문제 {total}개, 링크 {CHECKED} 확인, 문제별 예상 시간), 주차별 자주 하는 실수, Python 핵심 템플릿. 백준(BOJ)은 2026-04-28 종료되어 사용하지 않음.

## 문서

- [README.md]({SITE}/README.md): 전체 내용을 Markdown으로 정리 (기업 형식표, 유형 빈도, 16주 요약표, 주차별 문제 표, 템플릿, 출처)
- [curriculum.json]({SITE}/curriculum.json): 같은 내용을 구조화한 JSON. 주요 필드: company_formats, type_frequency, curriculum[].problem_sets[].problems[] (title, platform, level, est_minutes, url), curriculum[].common_mistakes, signals (지문 단서 → 알고리즘), io_formats, python_pitfalls, templates_python, sources
- [index.html]({SITE}/): 사람용 대화형 대시보드 (진행 체크·복습 일정·모의고사 타이머, 기록은 브라우저에 저장)

## 사용 안내

- 학습자의 진도(끝낸 주차)와 지원 회사를 물은 뒤, curriculum[] 순서대로 다음 필수 문제를 고르세요.
- 지원 회사별 우선 주차: 삼성 4~8주, 카카오 3·9~12주, 네이버·SK 등 3·9·10·12주, 현대차그룹 4·5·7·9주.
""")
print(f"built: {total} problems, {len(weeks)} weeks")
