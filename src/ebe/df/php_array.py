import pandas as pd
from pathlib import Path
from pydantic import BaseModel
from progressor import Spinner
from ebe.df import Info, Operation
from typing import Optional
from ebe.core.php import to_php
from ebe.ui.models import TaskIcon


class PhpArray(object, metaclass=Operation):

    summary = "Create PHP Array from csv"
    task_icon = TaskIcon.PHPARRAY

    class CustomParams(BaseModel):
        path: Path
        values: list[str]
        key: Optional[str]
        comment: Optional[str]

        def df(self) -> pd.DataFrame:
            with Spinner(f"Loading {self.path.name}") as progress:
                frame = pd.read_csv(self.path.as_posix(), low_memory=False)
                progress.console.print(Info(
                    title=self.path.name,
                    df=frame
                ))
                return frame

        @property
        def source_values(self) -> list[str]:
            return [
                x.split(":")[0] for x in self.values
            ]

        @property
        def is_assoc(self) -> bool:
            return any([":" in x for x in self.values])

        @property
        def dest_values(self) -> list[str]:
            return [
                x.split(":")[-1] for x in self.values
            ]

    @staticmethod
    def to_assoc(df, param: CustomParams) -> str:
        res = {}
        comments = {}
        for ind in df.index:
            key = df[param.key][ind]
            res[key] = {
                k: df[v][ind]
                for v, k in
                zip(param.source_values, param.dest_values)
            }
            if param.comment:
                comments[key] = df[param.comment][ind]
        return to_php(res, comments=comments)

    @staticmethod
    def to_map(df, param) -> str:
        res = {}
        comments = {}
        for ind in df.index:
            key = df[param.key][ind]
            res[key] = [df[k][ind] for k in param.source_values]
            if param.comment:
                comments[key] = df[param.comment][ind]
        return to_php(res, comments=comments)

    def exec(self, *params: CustomParams, **options) -> str:
        param = params[0]
        df = param.df()
        dff = df[filter(
            None, [param.key, *param.source_values, param.comment])]
        print(dff.head())
        if param.is_assoc:
            return PhpArray.to_assoc(dff, param)
        return PhpArray.to_map(dff, param)
