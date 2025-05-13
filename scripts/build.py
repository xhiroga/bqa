import json
from pathlib import Path

META_PATH = Path(__file__).resolve().parent.parent / "as" / "metadata.jsonl"

OUTPUTS = {
    "en": Path(__file__).resolve().parent.parent / "README.md",
    "ja": Path(__file__).resolve().parent.parent / "README.ja.md",
}

HEADER = "# Blender Q&A\n"


def format_version(version_dict: dict | None):
    """Return formatted version string like " (v4.0~)" or " (v4.0-4.1)".

    If version_dict is None or empty, return empty string.
    Accepted keys:
        min: minimum supported version (string)
        max: maximum supported version (string)
    """
    if not version_dict:
        return ""

    min_v: str | None = version_dict.get("min")
    max_v: str | None = version_dict.get("max")

    if not min_v and not max_v:
        return ""

    if min_v and max_v:
        return f" (v{min_v}-{max_v})"
    if min_v:
        return f" (v{min_v}~)"
    return f" (~v{max_v})"


def load_metadata(path: Path):
    """metadata.jsonl をパースして list[dict] を返す"""
    items: list[dict] = []
    with path.open(encoding="utf-8") as fp:
        for line in fp:
            line = line.strip()
            if not line:
                continue
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError as err:
                print(f"Skip invalid JSON line: {err}")
    return items


def find_entry(qa_list: list[dict], lang: str):
    for qa in qa_list:
        if qa.get("lang") == lang:
            return qa
    return None


def build_readme(items: list[dict], lang: str) -> str:
    md_lines: list[str] = [HEADER]
    for item in items:
        qa_list = item.get("qa", [])
        qa = find_entry(qa_list, lang)
        if not qa:
            continue
        q = qa.get("q", "")
        a = qa.get("a", "")
        image_url = item.get("url") or f"as/{item['file_name']}"

        version_info = format_version(item.get("blender_version"))

        md_lines.append(f"## {q.rstrip('。')}{version_info}\n")
        md_lines.append(f"{a}\n")
        md_lines.append(f"![{Path(image_url).stem.replace('-', ' ')}]({image_url})\n")
        
    return "\n".join(md_lines)


def main():
    items = load_metadata(META_PATH)
    for lang, out_path in OUTPUTS.items():
        markdown = build_readme(items, lang)
        out_path.write_text(markdown, encoding="utf-8")
        print(f"Generated {out_path}")


if __name__ == "__main__":
    main()
