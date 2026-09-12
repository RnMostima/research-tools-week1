#!/usr/bin/env python3
"""统计英文文本中的词频。

用法：
    python word_freq.py input.txt
    python word_freq.py input.txt --top 10
    Get-Content input.txt | python word_freq.py -

单词按英文字母识别，忽略大小写和标点；支持 don't、state-of-the-art
这类带撇号或连字符的写法。
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

WORD_PATTERN = re.compile(r"[A-Za-z]+(?:['’\-][A-Za-z]+)*")


def count_words(text: str) -> Counter[str]:
    """提取英文单词并返回不区分大小写的词频统计。"""
    normalized_text = text.replace("’", "'")
    words = (match.group(0).lower() for match in WORD_PATTERN.finditer(normalized_text))
    return Counter(words)


def positive_int(value: str) -> int:
    """将命令行参数转换为大于 0 的整数。"""
    try:
        number = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("必须是整数") from exc

    if number <= 0:
        raise argparse.ArgumentTypeError("必须是大于 0 的整数")
    return number


def read_input(input_path: str | None) -> str:
    """从文件或标准输入读取 UTF-8 文本。"""
    if input_path is None or input_path == "-":
        return sys.stdin.read()

    return Path(input_path).read_text(encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="统计英文文本中的词频")
    parser.add_argument(
        "input",
        nargs="?",
        help="UTF-8 文本文件路径；使用 - 或省略参数时从标准输入读取",
    )
    parser.add_argument(
        "-n",
        "--top",
        type=positive_int,
        default=20,
        help="显示词频最高的前 N 个单词，默认 20",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="显示全部单词，不受 --top 限制",
    )
    return parser


def print_report(counts: Counter[str], top: int, show_all: bool) -> None:
    """将词频结果输出到终端。"""
    total_words = sum(counts.values())
    print(f"总词数：{total_words}")
    print(f"不同单词数：{len(counts)}")

    if not counts:
        return

    sorted_items = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    if not show_all:
        sorted_items = sorted_items[:top]

    limit_text = "全部" if show_all else f"前 {top}"
    print(f"\n词频排名（{limit_text}）：")

    word_width = max(len(word) for word, _ in sorted_items)
    for rank, (word, count) in enumerate(sorted_items, start=1):
        print(f"{rank:>3}. {word:<{word_width}}  {count:>5}")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.input is None and sys.stdin.isatty():
        parser.print_help()
        return 2

    try:
        text = read_input(args.input)
    except UnicodeDecodeError:
        parser.error("输入文件不是有效的 UTF-8 文本")
    except OSError as exc:
        parser.error(f"无法读取输入：{exc}")

    counts = count_words(text)
    print_report(counts, top=args.top, show_all=args.all)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())