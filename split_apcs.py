#!/usr/bin/env python3
import os, re, sys, shutil, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "apcs" / "notes.md"
PROB_DIR = ROOT / "apcs" / "problems"
TOPIC_DIR = ROOT / "apcs" / "topics"

if not SRC.exists():
    print(f"[ERR] 找不到 {SRC}，請確認你在 repo 根目錄執行。")
    sys.exit(1)

# 題名 → 主題 的對應（可自行增修）
TITLE2TOPIC = {
    "互補 CP": "bit-hash",
    "置物櫃分配": "dp",
    "飛黃騰達": "greedy-lis",
    "幸運數字": "range-ds",
    "搬家": "graph",
    "美食博覽會": "misc",  # 進階可再拆到 DP
    "內積": "dp",
    "低地距離": "range-ds",
    "投資遊戲": "dp",
    "切割費用": "range-ds",
    "階梯數字": "dp",
    "Tree Distance I (CSES 1132)": "graph",
    "真假子圖": "graph",
    "邏輯電路": "graph",
    "病毒演化": "graph",
}

# 題名 → 檔名 slug（避免中文被清掉）
TITLE2SLUG = {
    "互補 CP": "complementary-pairs",
    "置物櫃分配": "locker",
    "飛黃騰達": "rising",
    "幸運數字": "lucky-number",
    "搬家": "moving",
    "美食博覽會": "food-expo",
    "內積": "dot-product",
    "低地距離": "lowland-distance",
    "投資遊戲": "investment-skip-k",
    "切割費用": "cut-cost",
    "階梯數字": "digit-dp",
    "Tree Distance I (CSES 1132)": "tree-distance-i",
    "真假子圖": "fake-subgraph-2sat-dsu",
    "邏輯電路": "logic-circuit-dag",
    "病毒演化": "virus-evolution-tree-dp",
}

def slugify(title:str)->str:
    # 預設用對應表；沒有就 fallback
    if title in TITLE2SLUG: return TITLE2SLUG[title]
    s = unicodedata.normalize("NFKD", title)
    s = re.sub(r"[^\w\s-]", "", s).strip().lower()
    s = re.sub(r"[\s_-]+", "-", s)
    return s or "section"

text = SRC.read_text(encoding="utf-8")

# 以第二級標題 "## " 切段：[(title, content)]
parts = []
cur_title = None
cur_lines = []

for line in text.splitlines():
    m = re.match(r"^##\s+(.+?)\s*$", line)
    if m:
        if cur_title is not None:
            parts.append((cur_title, "\n".join(cur_lines).rstrip()+"\n"))
        cur_title = m.group(1).strip()
        cur_lines = []
    else:
        if cur_title is not None:
            cur_lines.append(line)

if cur_title is not None:
    parts.append((cur_title, "\n".join(cur_lines).rstrip()+"\n"))

if not parts:
    print("[ERR] 沒有找到任何 '## 題目' 區塊；請確認 notes.md 的標題層級。")
    sys.exit(1)

# 備份原筆記一次
bak = SRC.with_suffix(".backup.md")
if not bak.exists():
    shutil.copy2(SRC, bak)

PROB_DIR.mkdir(parents=True, exist_ok=True)

# 將每一段輸出為獨立題解頁，並寫入對應主題頁清單
created = []
for title, body in parts:
    topic = TITLE2TOPIC.get(title, "misc")
    slug = slugify(title)
    out = PROB_DIR / f"{slug}.md"

    # 生成題解頁內容：轉為 H1，補麵包屑與標籤
    content = []
    content.append(f"[← 回 APCS 索引](../index.md) · [主題：{topic}](../topics/{topic}.md)\n")
    content.append(f"# {title}\n\n")
    # 如果原段落以 "```cpp" 等程式碼開頭，前面留一個空行避免黏連
    content.append(body.lstrip() + ("\n" if not body.endswith("\n") else ""))
    out.write_text("\n".join(content), encoding="utf-8")

    # 把連結追加到對應主題頁（若尚未存在同一行）
    topic_md = TOPIC_DIR / f"{topic}.md"
    topic_md.touch()
    topic_text = topic_md.read_text(encoding="utf-8")
    link_line = f"- [{title}](../problems/{slug}.md)"
    if link_line not in topic_text:
        if not topic_text.endswith("\n"): topic_text += "\n"
        topic_text += link_line + "\n"
        topic_md.write_text(topic_text, encoding="utf-8")

    created.append((title, topic, out.relative_to(ROOT).as_posix()))

# 輸出 summary
print("\n[OK] 已拆出以下題解頁：")
for t, tp, p in created:
    print(f"  - {t}  →  {p}  （主題：{tp}）")

print(f"\n[INFO] 已保留原檔：{SRC.name}（備份：{bak.name}）")
print("[NEXT] 請在側欄點『APCS → 索引（主題導覽）』查看效果；或用 `mkdocs serve` 預覽。")
