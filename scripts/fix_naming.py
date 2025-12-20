#!/usr/bin/env python3
"""
Fix naming convention violations: files with ___ in name but wikilink object.

The ___ placeholder should only be used for literal objects.
For wikilink objects, the object anchor should be in the filename.
"""

import os
import re
from pathlib import Path


def extract_object_anchor(content: str) -> str | None:
    """Extract anchor from rdf__object if it's a pure wikilink."""
    match = re.search(r'rdf__object:\s*"\[\[([^\]]+)\]\]"', content)
    if match:
        return match.group(1)
    return None


def fix_filename(filepath: Path) -> tuple[Path, Path] | None:
    """
    Check if file needs renaming and return (old_path, new_path).
    Returns None if no rename needed.
    """
    filename = filepath.name

    # Only process files with ___ pattern
    if '___' not in filename:
        return None

    # Read content
    content = filepath.read_text(encoding='utf-8')

    # Check if object is a pure wikilink
    anchor = extract_object_anchor(content)
    if not anchor:
        return None  # Object is a literal, ___ is correct

    # Build new filename by replacing ___N with anchor
    # Pattern: "subject predicate ___N.md" -> "subject predicate anchor.md"
    new_filename = re.sub(r'___\d*\.md$', f'{anchor}.md', filename)

    if new_filename == filename:
        return None  # No change needed

    new_path = filepath.parent / new_filename
    return (filepath, new_path)


def main():
    root = Path('.')
    renames = []

    # Collect all renames first
    for dirpath, _, filenames in os.walk(root):
        dir_path = Path(dirpath)
        if dir_path.name.startswith('.'):
            continue  # Skip hidden dirs

        for filename in filenames:
            if '___' not in filename or not filename.endswith('.md'):
                continue

            filepath = dir_path / filename
            result = fix_filename(filepath)
            if result:
                renames.append(result)

    print(f"Found {len(renames)} files to rename")

    # Check for conflicts
    new_names = {}
    conflicts = []
    for old_path, new_path in renames:
        if new_path in new_names:
            conflicts.append((old_path, new_path, new_names[new_path]))
        else:
            new_names[new_path] = old_path

    if conflicts:
        print(f"\n{len(conflicts)} conflicts detected:")
        for old1, new, old2 in conflicts[:10]:
            print(f"  {old1.name} and {old2.name} -> {new.name}")
        if len(conflicts) > 10:
            print(f"  ... and {len(conflicts) - 10} more")
        return

    # Perform renames
    for old_path, new_path in renames:
        if new_path.exists():
            print(f"SKIP (exists): {old_path.name} -> {new_path.name}")
            continue
        os.rename(old_path, new_path)
        print(f"RENAMED: {old_path.name} -> {new_path.name}")

    print(f"\nDone! Renamed {len(renames)} files.")


if __name__ == '__main__':
    main()
