import re
content = open('scraper_logic.py', encoding='utf-8').read()
all_strings = re.findall(r'(r?)"(\(\?i\)[^"]*)"', content)
print(f"Found {len(all_strings)} regex-like strings total")
broken = []
for prefix, s in all_strings:
    try:
        actual = s if prefix == 'r' else s.encode().decode('unicode_escape')
    except Exception:
        actual = s
    try:
        re.compile(actual)
    except re.error as e:
        broken.append((prefix, s, str(e)))
print(f"Found {len(broken)} broken (uncompilable) patterns:")
for prefix, s, err in broken:
    print(f"  prefix={prefix!r} | {s!r} | ERROR: {err}")
