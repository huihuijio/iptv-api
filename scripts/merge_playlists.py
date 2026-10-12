import re


def merge(files, out_m3u, out_txt):
    """合并多个 m3u（按传入顺序，同频道多源全部保留），输出 result.m3u 与 result.txt。"""
    merged = []
    for fn in files:
        with open(fn, encoding="utf-8") as f:
            merged.extend(f.read().splitlines())

    body = []
    for ln in merged:
        if ln.startswith("#EXTM3U"):
            body.append('#EXTM3U x-tvg-url="https://live.fanmingming.cn/e.xml"')
        else:
            body.append(ln)

    with open(out_m3u, "w", encoding="utf-8") as f:
        f.write("\n".join(body) + "\n")

    txt = []
    cur_cat = None
    prev_name = None
    for ln in body:
        if ln.startswith("#EXTINF"):
            m = re.search(r'group-title="([^"]*)"', ln)
            cat = m.group(1) if m else "其他频道"
            if cat != cur_cat:
                cur_cat = cat
                txt.append(f"{cat},#genre#")
            nm = re.search(r",([^,]+)$", ln)
            prev_name = nm.group(1).strip() if nm else None
        elif ln.startswith("http"):
            name = prev_name or "未知频道"
            txt.append(f"{name},{ln}")

    with open(out_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(txt) + "\n")


if __name__ == "__main__":
    merge(["index.m3u", "ipv6.m3u"], "result.m3u", "result.txt")
