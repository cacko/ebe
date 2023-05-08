from typing import Any, Optional
from typing import TypeVar
from click import Command
from prompt_toolkit.styles.pygments import style_from_pygments_cls
from pygments.styles import get_style_by_name
from questionary import Separator
from pydantic import BaseModel
from emoji import emojize
from pathlib import Path
from ebe.core.csv import get_columns

from prompt_toolkit.formatted_text import (
    FormattedText as PT_FormattedText,
    PygmentsTokens,
    to_formatted_text,
    merge_formatted_text,
    AnyFormattedText,
)
from pygments.token import Token
import questionary

from ebe.df import Operation
from ebe.ui.models import TaskIcon


style = style_from_pygments_cls(get_style_by_name("monokai"))  # type: ignore


def keyword(s: str) -> PT_FormattedText:
    return to_formatted_text(PygmentsTokens([(Token.Keyword, s)]))


def punctuation(s: str) -> PT_FormattedText:
    return to_formatted_text(PygmentsTokens([(Token.Punctuation, s)]))


def comment(s: str) -> PT_FormattedText:
    return to_formatted_text(PygmentsTokens([(Token.Comment, s)]))


def text(s: str) -> PT_FormattedText:
    return to_formatted_text(PygmentsTokens([(Token.Text, s)]))


class MenuItem(BaseModel):
    text: str
    cmd: Command
    obj: Optional[Any] = None
    disabled: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True

    @property
    def display(self) -> AnyFormattedText:
        return to_formatted_text(
            merge_formatted_text(
                [
                    punctuation(f"{emojize(self.task_icon.value)} "),
                    keyword(self.text),
                ]
            )
        )

    @property
    def value(self):
        if self.obj:
            return self.obj.name
        return self.text

    @property
    def task_icon(self) -> TaskIcon:
        if self.obj:
            return self.obj.task_icon
        return TaskIcon.OFF


class TaskItem(MenuItem):
    obj: Operation

    class Config:
        arbitrary_types_allowed = True

    def get_input(self):
        raise NotImplementedError


class DisabledItem(MenuItem):
    @property
    def display(self):
        return comment(self.text)


# @click.argument("left")
# @click.argument("right")
# @click.option("-l", "--left-columns", multiple=True)
# @click.option("-r", '--right-columns', multiple=True)
# @click.option("-o", "--output")


class MergeOperationItem(TaskItem):

    def get_input(self) -> dict:
        answers = {}

        answers["left"] = questionary.path(
            message="Left file",
            validate=lambda x: Path(x).suffix == '.csv',
        ).ask()

        answers["right"] = questionary.path(
            message="right file",
            validate=lambda x: Path(x).suffix == '.csv',
        ).ask()

        answers["left_columns"] = questionary.checkbox(
            message="left cols",
            choices=get_columns(Path(answers["left"])),
            validate=lambda x: len(x) > 0

        ).ask()

        answers["right_columns"] = questionary.checkbox(
            message="right columns",
            choices=get_columns(Path(answers["right"])),
            validate=lambda x: len(x) > 0
        ).ask()

        return answers


MT = TypeVar("MT", MenuItem, TaskItem, DisabledItem, Separator)
