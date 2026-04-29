from __future__ import annotations

from rich.console import Console
from rich.markdown import Markdown

console = Console()


def print_markdown(text: str) -> None:
    console.print(Markdown(text))


def info(text: str) -> None:
    console.print(f"[bold cyan]{text}[/bold cyan]")


def warn(text: str) -> None:
    console.print(f"[bold yellow]{text}[/bold yellow]")
