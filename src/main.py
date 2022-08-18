#
# TODO - if semver already exists, append, dont overwrite
# TODO - add logger
#
import argparse
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


ALLOWED_CHANGELOG_ACTIONS = (
    "added",
    "changed",
    "fixed",
    "removed",
)
TEMPLATE_DIR = Path(__file__).parent / "templates"

environment = Environment(loader=FileSystemLoader(TEMPLATE_DIR), trim_blocks=True)


def parse_args() -> argparse.Namespace:
    """ """
    parser = argparse.ArgumentParser(prog="A changelog.md helper")
    parser.add_argument(
        "--semver",
        type=str,
        help="The new semantic version number such as 0.1.2",
    )
    parser.add_argument(
        "--added",
        action="extend",
        nargs="+",
        help="A space delimited list of items that have been *added* during this release such as --added 'first item' 'second item'.",
    )
    parser.add_argument(
        "--changed",
        action="extend",
        nargs="+",
        help="A space delimited list of items that have been *changed* during this release such as --changed 'first item' 'second item'.",
    )
    parser.add_argument(
        "--fixed",
        action="extend",
        nargs="+",
        help="A space delimited list of items that have been *fixed* during this release such as --fixed 'first item' 'second item'.",
    )
    parser.add_argument(
        "--removed",
        action="extend",
        nargs="+",
        help="A space delimited list of items that have been *removed* during this release such as --removed 'first item' 'second item'.",
    )
    parser.add_argument(
        "--github-snippet",
        action="store_true",
        # nargs="?",
        help="todo",
    )
    return parser.parse_args()


def render_template(
    semantic_version: str,
    action: str,
    items: list[str],
    template_file: str = "changelog.j2",
    date: str = datetime.now().date().isoformat(),
) -> str:
    """ """
    template = environment.get_template(name=template_file)
    return template.render(
        semantic_version=semantic_version, action=action, items=items, date=date
    )


def changelog_file_manager(content: str, file: str = 'CHANGELOG.md') -> None:
    with open(file=file, mode='a') as f:
        f.write(content)



def main() -> None:
    args = parse_args()
    print(args)
    template = environment.get_template(name="changelog.j2")
    rendered = template.render(
        semantic_version=args.semver,
        allowed_changelog_actions=ALLOWED_CHANGELOG_ACTIONS,
        date=datetime.now().date().isoformat(),
        args=args,
    )
    print(f"Writing the following changelog actions to CHANGELOG.md...\n{rendered}")
    changelog_file_manager(file='/tmp/CHANGELOG.md', content=rendered)
    if args.github_snippet:
        print(

        f"""git tag {args.semver}, --message '{args.semver}' --message '{rendered.strip()}' && \\
git push --tags"""
        )

if __name__ == "__main__":
    main()
