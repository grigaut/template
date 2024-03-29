"""Generate the code reference pages and navigation."""

from pathlib import Path

import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()

for path in sorted(Path("src/{{cookiecutter.module_name}}").rglob("*.py")):
    module_path = path.relative_to(".").with_suffix("")
    doc_path = path.relative_to(
        "src/{{cookiecutter.module_name}}"
    ).with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    parts = list(module_path.parts)

    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
        ident = ".".join(parts)
        nav[parts] = doc_path
        with mkdocs_gen_files.open(full_doc_path, "w") as fd:
            print(f"# `{ident}`\n", file=fd)
            print("::: " + ident, file=fd)
            print("    options:", file=fd)
            print("      members:", file=fd)
            print("        - __all__", file=fd)
            mkdocs_gen_files.set_edit_path(full_doc_path, path)
            continue
    elif parts[-1] == "__main__":
        continue

    ident = ".".join(parts)

    nav[parts] = doc_path

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        print(f"# `{ident}`\n", file=fd)
        print("::: " + ident, file=fd)

    mkdocs_gen_files.set_edit_path(full_doc_path, path)

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
