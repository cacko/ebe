import pandas as pd
from pathlib import Path
from pydantic import BaseModel
from progressor import Spinner
from build.lib.ebe.df import php_array
from ebe.df import Info, OperationMeta
from typing import Optional


class PhpArray(object, metaclass=OperationMeta):

    class CustomParams(BaseModel):
        path: Path
        values: list[str]
        key: Optional[str]

        def df(self) -> pd.DataFrame:
            with Spinner(f"Loading {self.path.name}") as progress:
                frame = pd.read_csv(self.path.as_posix(), low_memory=False)
                progress.console.print(Info(
                    title=self.path.name,
                    df=frame
                ))
                return frame

    def exec(self, *params: CustomParams, **options) -> pd.DataFrame:
        param = params[0]
        df = param.df()
        dff = df[[param.key, *param.values]]
        print(dff.head())
        # dfp = left.df()
        # dfb = right.df()
        # with Spinner(f"Merging by {','.join(left.columns)}"
        #              f" / {','.join(right.columns)}"
        #              ) as progress:
        #     res = dfp.merge(
        #         dfb,
        #         left_on=left.columns,
        #         right_on=right.columns
        #     )
        #     progress.console.print(Info(
        #         title="merged result",
        #         df=res
        #     ))
        #     return res
