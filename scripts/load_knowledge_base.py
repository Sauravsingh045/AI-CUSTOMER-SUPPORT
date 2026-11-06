from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_BASE_DIR = PROJECT_ROOT / "knowledge_base"


def parse(path: Path) -> list[tuple[str, str, str]]:
    entries = []
    for block in path.read_text(encoding="utf-8").split("\n## ")[1:]:
        title, separator, content = block.partition("\n")
        if not separator or not title.strip() or not content.strip():
            raise ValueError(f"{path.name}: each ## heading must have a title and content")
        if "TODO:" in content:
            raise ValueError(f"{path.name}: {title.strip()} still contains a TODO")
        entries.append((path.stem, title.strip(), content.strip()))
    if not entries:
        raise ValueError(f"{path.name}: no ## entries found")
    return entries


def main() -> None:
    paths = sorted(KNOWLEDGE_BASE_DIR.glob("*.md"))
    if not paths:
        raise FileNotFoundError(f"No Markdown files found in {KNOWLEDGE_BASE_DIR}")

    seen: set[tuple[str, str]] = set()
    total = 0
    for path in paths:
        rows = parse(path)
        for section, title, _ in rows:
            key = (section, title)
            if key in seen:
                raise ValueError(f"Duplicate knowledge-base entry: {section}/{title}")
            seen.add(key)
        total += len(rows)
        print(f"{path.stem}: {len(rows)} entries")
    print(f"Validated {total} entries across {len(paths)} files.")


if __name__ == "__main__":
    main()
