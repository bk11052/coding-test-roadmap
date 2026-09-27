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
    "name": "대기업 코테 로드맵", "site": SITE + "/", "updated": UPDATED, "links_checked": CHECKED, "language": "ko",
    "description": f"국내 대기업 신입 SW 코딩테스트 준비 가이드: 기업별 형식, 출제 유형, 16주 커리큘럼(문제 {total}개)",
    "important_notice": NOTICE, "how_to_use": HOW_TO,
    "est_minutes_rule": "LV1 15분, LV2 30분, LV3 50분, LV4 70분, LV5 90분, 코드트리 삼성 기출 150분, HSAT 기출 60분, SQL LV3 20분·LV4 이상 30분",
    "company_formats": static["company_formats"], "frequency_columns": static["frequency_columns"], "type_frequency": static["type_frequency"],
    "curriculum": weeks, "templates_python": static["templates_python"], "tools": static["tools"],
    "verified_videos": static["verified_videos"], "dropped_claims": static["dropped_claims"], "sources": static["sources"],
}
(ROOT / "curriculum.json").write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")


def badge(label, msg, color):
    enc = lambda s: quote(s.replace("-", "--").replace("_", "__"))
    return f"![{label}](https://img.shields.io/badge/{enc(label)}-{enc(msg)}-{color})"


L = []
A = L.append
A('<div align="center">\n')
A("# 대기업 코테 로드맵\n")
A("**국내 대기업 신입 SW 코딩테스트를 16주 안에 준비하는 커리큘럼과 대시보드**\n")
A(" ".join([badge("문제", f"{total}개", "2f5bea"), badge("기간", "16주", "6a53c9"), badge("기업", "10곳", "1d7f55"),
            badge("링크 확인", CHECKED, "b7730f"), badge("백준", "미사용 (서비스 종료)", "b4323c")]) + "\n")
A(f"[**대시보드 열기**]({SITE}/) · [AI용 요약 (llms.txt)]({SITE}/llms.txt) · [데이터 (curriculum.json)]({SITE}/curriculum.json)\n")
A("</div>\n")
A(f"> [!IMPORTANT]\n> {NOTICE}\n")
A("## 목차\n")
for t, a in [("이 저장소 사용법", "이-저장소-사용법"), ("AI로 활용하기", "ai로-활용하기"), ("핵심 요약", "핵심-요약"), ("기업별 시험 형식", "기업별-시험-형식"),
             ("유형별 출제 빈도", "유형별-출제-빈도"), ("16주 한눈에 보기", "16주-한눈에-보기"), ("주차별 문제", "주차별-문제"),
             ("핵심 템플릿 (Python)", "핵심-템플릿-python"), ("도구", "도구"), ("검증한 유튜브 영상", "검증한-유튜브-영상"),
             ("걸러낸 정보", "걸러낸-정보"), ("출처", "출처")]:
    A(f"- [{t}](#{a})")
A("\n## 이 저장소 사용법\n")
A(f"1. **[대시보드]({SITE}/)를 엽니다.** 지원 회사, 시험 날짜, 하루 공부 시간을 넣으면 오늘 풀 문제와 남은 일정을 계산합니다.")
A("2. **주차 순서대로 공부합니다.** 강의를 보고, 필수 문제를 풀고, 통과 기준을 확인합니다. 문제 옆 **기록** 버튼으로 풀이 상태와 메모를 남기면 해설을 본 문제는 1·3·7·14일 뒤 복습으로 다시 나옵니다.")
A("3. **13주차부터 실전입니다.** 지원 회사 기출을 풀고, 모의고사 타이머로 실제 시험 시간에 맞춰 연습합니다.\n")
A("진행 기록은 브라우저에 저장됩니다. 기기를 바꿀 때는 대시보드의 **기록 내보내기 / 가져오기**를 쓰세요. GitHub에서 직접 볼 때는 아래 주차별 체크박스를 복사해 자기 저장소나 노트에 붙여 쓰면 됩니다.\n")
A("## AI로 활용하기\n")
A("HTML을 해석하지 않아도 되도록 같은 내용을 파일 3개로 따로 올렸습니다. Codex, 다른 계정의 Claude, ChatGPT 같은 AI에게 아래 주소 중 하나를 주면 됩니다.\n")
A("| 파일 | 내용 |\n|---|---|")
A(f"| [`llms.txt`]({SITE}/llms.txt) | 한 문단 요약과 나머지 파일 안내. AI에게 처음 줄 주소로 적당합니다 |")
A(f"| [`README.md`]({SITE}/README.md) | 전체 내용을 Markdown으로 정리한 이 문서. 주차별 문제 링크, 템플릿, 출처까지 들어 있습니다 |")
A(f"| [`curriculum.json`]({SITE}/curriculum.json) | 같은 내용을 구조화한 JSON. 프로그램이나 에이전트가 문제 목록을 다룰 때 씁니다 |\n")
A("이렇게 요청해 보세요.\n")
A("```text")
A(f"{SITE}/llms.txt 읽고 내 진도에 맞춰 이번 주 문제 골라 줘. 나는 5주차까지 끝냈고 삼성 지원 예정이야.")
A(f"{SITE}/curriculum.json 에서 카카오 관련 필수 문제만 뽑아 하루 2시간 기준 4주 계획으로 다시 짜 줘.")
A("README의 7주차 '자주 하는 실수'를 기준으로 내 코드를 검토해 줘. (코드 붙여 넣기)")
A("```\n")
A("`curriculum.json`의 주요 필드: `company_formats`, `type_frequency`, `curriculum[].problem_sets[].problems[]` (`title`, `platform`, `level`, `est_minutes`, `url`), `curriculum[].common_mistakes`, `templates_python`, `sources`.\n")
A("## 핵심 요약\n")
for s in ["구현·시뮬레이션과 BFS/DFS가 모든 회사의 공통 뼈대입니다.", "목표 수준은 백준 기준 골드 4~3입니다.",
          "다 풀 필요는 없습니다. 카카오 1차는 7문제 중 3~4솔로 합격한 후기가 있습니다.",
          "연습은 프로그래머스(카카오·네이버·SK·한화)와 코드트리(삼성·HSAT)로 합니다.",
          "삼성 A형, 현대차 HSAT, PCCP 인증으로 코테를 면제받을 수 있습니다.", "네이버·카카오 등 대부분은 시험 중 AI 사용을 금지합니다."]:
    A(f"- {s}")
A("\n## 기업별 시험 형식\n")
A("| 기업 | 플랫폼 | 구성·시간 | 난이도·유형 | 특이사항 | 신뢰도 |\n|---|---|---|---|---|---|")
for c in static["company_formats"]:
    A(f"| **{c['company']}** | {c['platform']} | {c['format']} | {c['content']} | {c['notes']} | {c['confidence']} |")
A("\n지원 전에 반드시 채용 공고를 확인하세요. 신뢰도가 \"후기 1건\"이나 \"정보 부족\"인 항목은 달라졌을 수 있습니다.\n")
A("## 유형별 출제 빈도\n")
cols = static["frequency_columns"]
A("| " + " | ".join(cols) + " |\n|" + "---|" * len(cols))
for r in static["type_frequency"]:
    A("| **" + r[0] + "** | " + " | ".join(r[1:]) + " |")
A("\n여러 후기와 기출 해설을 종합한 정성 평가입니다.\n")
A("## 16주 한눈에 보기\n")
A("| 주차 | 주제 | 필수·모의고사 | 도전 | 예상 시간 |\n|:--:|---|:--:|:--:|:--:|")
for w in weeks:
    A(f"| [{w['week']:02d}](#week-{w['week']}) | {w['topic']} | {w['required_count']} | {w['optional_count'] or '—'} | {fmt_h(w['est_minutes_required'])} |")
A(f"\n예상 시간 기준: {data['est_minutes_rule']}.\n")
A("## 주차별 문제\n")
A(HOW_TO + "\n")
last = None
for w in weeks:
    if w["phase"] != last:
        A(f"### {w['phase']}\n")
        last = w["phase"]
    A(f'<a id="week-{w["week"]}"></a>')
    A(f"<details>\n<summary><b>{w['week']:02d}주 · {w['topic']}</b> — 필수 {w['required_count']}개 · 약 {fmt_h(w['est_minutes_required'])}</summary>\n")
    if w["lectures"]:
        A("**강의:** " + " · ".join(f"[{l['title']}]({l['url']})" for l in w["lectures"]) + "\n")
    A(f"**익힐 것:** {w['learn']}\n")
    if w["common_mistakes"]:
        A("**자주 하는 실수**\n")
        for p in w["common_mistakes"]:
            A(f"- {p}")
        A("")
    for s in w["problem_sets"]:
        extra = []
        if s.get("time_limit_minutes"):
            extra.append(f"제한 {fmt_h(s['time_limit_minutes'])}")
        if s.get("companies"):
            extra.append(", ".join(s["companies"]))
        A(f"**{s['name']}**" + (f" ({' · '.join(extra)})" if extra else "") + "\n")
        A("| | 문제 | 플랫폼 | 난이도 | 예상 |\n|:--:|---|---|:--:|:--:|")
        for p in s["problems"]:
            A(f"| ☐ | [{p['title']}]({p['url']}) | {p['platform']} | {p['level']} | {fmt_h(p['est_minutes'])} |")
        A("")
    A(f"**통과 기준:** {w['pass_criterion']}\n\n</details>\n")
A("## 핵심 템플릿 (Python)\n")
A("16주차 점검 대상입니다. 보지 않고 5분 안에 쓸 수 있을 때까지 반복하세요.\n")
for t in static["templates_python"]:
    A(f"<details>\n<summary><b>{t['name']}</b></summary>\n\n```python\n{t['code']}\n```\n\n</details>\n")
A("## 도구\n")
A("| 도구 | 용도 |\n|---|---|")
for t in static["tools"]:
    A(f"| [{t['name']}]({t['url']}) | {t['use']} |")
A("\n## 검증한 유튜브 영상\n")
A("자막 전체를 읽고 확인했습니다.\n")
A("| 영상 | 채널 | 판정 | 메모 |\n|---|---|---|---|")
for v in static["verified_videos"]:
    A(f"| [{v['title']}]({v['url']}) | {v['channel']} | **{v['verdict']}** | {v['notes']} |")
A("\n## 걸러낸 정보\n")
A("조사하면서 틀렸거나, 오래됐거나, 근거가 약하다고 판단해 넣지 않았거나 고친 내용입니다.\n")
for x in static["dropped_claims"]:
    A(f"- {x}")
A("\n## 출처\n")
for s in static["sources"]:
    A(f"- [{s['title']}]({s['url']})")
A(f"\n---\n\n문제 저작권은 각 플랫폼(프로그래머스, 코드트리)에 있으며 이 저장소는 링크만 제공합니다. 채용 형식은 해마다 바뀌므로 지원 전 채용 공고를 최종 기준으로 삼으세요. 최종 업데이트 {UPDATED}.")
(ROOT / "README.md").write_text("\n".join(L) + "\n")

(ROOT / "llms.txt").write_text(f"""# 대기업 코테 로드맵

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
