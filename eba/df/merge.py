from typing import Any
import pandas as pd
from pathlib import Path
from pydantic import BaseModel
from progressor import Spinner
from eba.df import Info, OperationMeta
from eba.core.term import ccze
from rich.markdown import Markdown


class Merge(object, metaclass=OperationMeta):

    class CustomParams(BaseModel):
        path: Path
        columns: list[str]

        def df(self) -> pd.DataFrame:
            with Spinner(f"Loading {self.path.name}") as progress:
                frame = pd.read_csv(self.path.as_posix(), low_memory=False)
                progress.console.print(Info(
                    title=self.path.name,
                    df=frame
                ))
                return frame

    def exec(self, *params: list[CustomParams], **options) -> pd.DataFrame:
        left, right = params
        dfp = left.df()
        dfb = right.df()
        with Spinner(f"Merging by {','.join(left.columns)}"
                     f" / {','.join(right.columns)}"
                     ) as progress:
            res = dfp.merge(
                dfb,
                left_on=left.columns,
                right_on=right.columns
            )
            progress.console.print(Info(
                title="merged result",
                df=res
            ))
            return res
