"""Check every problem and link in curriculum.json.

- Programmers problems: compare title and level with the public catalog API.
- Codetree problems: compare the page title.
- Other links: expect HTTP 200. HTTP errors and DNS failures are broken;
  403/429, resets and timeouts are warnings (bot or overseas blocking).

Prints a Markdown report. Exit code 1 when anything is broken.
Usage: python3 scripts/check_links.py
"""
import concurrent.futures as cf
import json
import pathlib
import re
import socket
import sys
import time
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) coding-test-roadmap link check"}
data = json.loads((ROOT / "curriculum.json").read_text())


def fetch(url, retries=2):
    for i in range(retries + 1):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return r.status, r.read().decode("utf-8", "ignore")
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and i < retries:
                time.sleep(3 * (i + 1))
                continue
            return e.code, ""
        except Exception as e:  # DNS, reset, timeout
            if isinstance(getattr(e, "reason", None), socket.gaierror):
                return "DNS", ""  # 도메인이 사라짐: 확실히 깨진 링크
            if i < retries:
                time.sleep(3 * (i + 1))
                continue
            return type(e).__name__, ""


problems = []
for w in data["curriculum"]:
    for s in w["problem_sets"]:
        for p in s["problems"]:
            problems.append((w["week"], s["name"], p))

broken, warnings = [], []

# Programmers catalog
catalog, page = {}, 1
while True:
    status, body = fetch(f"https://school.programmers.co.kr/api/v2/school/challenges/?perPage=100&page={page}")
    if status != 200:
        broken.append(f"프로그래머스 문제 목록 API를 읽지 못했습니다 ({status})")
        break
    d = json.loads(body)
    for x in d["result"]:
        catalog[x["id"]] = x
    if page >= d["totalPages"]:
        break
    page += 1

for week, set_name, p in problems:
    if p["platform"] != "프로그래머스" or not catalog:
        continue
    x = catalog.get(int(p["url"].rsplit("/", 1)[1]))
    where = f"{week:02d}주 · {set_name} · {p['title']}"
    if not x:
        broken.append(f"{where}: 프로그래머스에서 사라짐 ({p['url']})")
    elif x["title"].strip() != p["title"] or f"LV{x['level']}" != p["level"]:
        broken.append(f"{where}: 제목·난이도가 바뀜 → {x['title'].strip()} LV{x['level']}")


def check_codetree(item):
    week, set_name, p = item
    status, body = fetch(p["url"])
    m = re.search(r"<title>코딩테스트 기출 문제 설명: ([^|<]*)", body)
    got = m.group(1).strip() if m else None
    if got != p["title"]:
        return f"{week:02d}주 · {set_name} · {p['title']}: 코드트리 페이지가 다름 ({status}, {got}) {p['url']}"


links = set()
for w in data["curriculum"]:
    links.update(l["url"] for l in w["lectures"])
    for s in w["problem_sets"]:
        links.update(p["solution_url"] for p in s["problems"] if "solution_url" in p)
links.update(t["url"] for t in data["tools"])
links.update(s["url"] for s in data["sources"])


def check_link(u):
    status, _ = fetch(u)
    if status == 200:
        return None
    # 404·410 같은 HTTP 오류와 DNS 실패만 깨진 것으로 봅니다.
    # 403·429와 연결 끊김·시간 초과는 해외 접속 차단일 수 있어 경고로 둡니다.
    real = status == "DNS" or (isinstance(status, int) and status not in (401, 403, 429))
    return ("broken" if real else "warn", f"{u} ({status})")


with cf.ThreadPoolExecutor(8) as ex:
    broken += [r for r in ex.map(check_codetree, [x for x in problems if x[2]["platform"] != "프로그래머스"]) if r]
    for r in ex.map(check_link, sorted(links)):
        if r:
            (warnings if r[0] == "warn" else broken).append(r[1])

print(f"문제 {len(problems)}개, 링크 {len(links)}개를 확인했습니다.\n")
if broken:
    print("### 깨진 항목\n")
    print("\n".join(f"- {b}" for b in broken))
if warnings:
    print("\n### 접근이 막힌 링크 (봇 차단일 수 있음)\n")
    print("\n".join(f"- {w}" for w in warnings))
if not broken and not warnings:
    print("모두 정상입니다.")
sys.exit(1 if broken else 0)
