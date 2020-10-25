import itertools as it
import pathlib
from typing import Iterator

import bs4
import markdown

MARKDOWN_EXTENSIONS = ["fenced_code"]


def convert(fname: pathlib.Path) -> str:
    return format(split(read_markdown(fname)))


def read_markdown(fname: pathlib.Path) -> bs4.BeautifulSoup:
    with open(fname) as f:
        html = markdown.markdown(f.read(), extensions=MARKDOWN_EXTENSIONS)
    return bs4.BeautifulSoup(html, "html.parser")


class H2Grouper:
    def __init__(self) -> None:
        self._g = 0

    def __call__(self, elem: bs4.BeautifulSoup) -> int:
        if elem.name == "h2":
            self._g += 1
        return self._g


def split(bs: bs4.BeautifulSoup) -> Iterator[Iterator[bs4.BeautifulSoup]]:
    gs = it.groupby(bs.children, H2Grouper())
    return (v for _, v in gs)


def escape(s: str) -> str:
    return s.replace('"', '""')


def format_group(g: Iterator[bs4.BeautifulSoup]) -> str:
    hl = next(g).text
    block = "\n".join(escape(f"{x}") for x in g)
    return f'"{hl}"; "{block}"'


def format(gs: Iterator[Iterator[bs4.BeautifulSoup]]) -> str:
    return "\n".join(format_group(g) for g in gs)
