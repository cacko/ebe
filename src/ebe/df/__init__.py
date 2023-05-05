import io
from pandas import DataFrame
from typing import Any, Optional
from rich.console import Console, ConsoleOptions, RenderResult
from pydantic import BaseModel, Field


class Info(BaseModel):
    df: DataFrame
    verbose: bool | None = Field(default=False)
    max_cols: int | None = Field(default=False)
    memory_usage: bool | str | None = Field(default=False)
    show_counts: bool | None = Field(default=True)
    icon: Optional[str] = Field(default=None)
    title: Optional[str] = Field(default=None)

    class Config:
        arbitrary_types_allowed = True

    def __rich_console__(
        self,
        console: Console,
        options: ConsoleOptions
    ) -> RenderResult:
        txt = []
        if self.icon:
            txt.append(self.icon)
        if self.title:
            txt.append(f"[b]{self.title}[/b]")
        if len(txt):
            yield " ".join(txt)
        yield self.info
        yield "\n"

    @ property
    def info(self) -> str:
        buff = io.StringIO()
        self.df.info(
            self.verbose,
            buff,
            self.max_cols,
            self.memory_usage,
            self.show_counts,
        )
        return buff.getvalue()


class OperationMeta(type):

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return super().__call__(*args, **kwds)

    @ property
    def params(cls):
        return cls.CustomParams

    def execute(cls, *args, **kwds):
        return cls().exec(*args, **kwds)
