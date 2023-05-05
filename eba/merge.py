import pandas as pd
from pathlib import Path
from pydantic import BaseModel, PrivateAttr
from progressor import Spinner
from eba.core.df import info
from eba.core.term import ccze

class MergeParams(BaseModel):
    path: Path
    columns: list[str]
    
    def df(self) -> pd.DataFrame:
        with Spinner(f"Loading {self.path.name}") as progress:
            frame =  pd.read_csv(self.path.as_posix(), low_memory=False)
            progress.console.print(ccze(info(frame)))
            return frame
        

def merge(
    left: MergeParams,
    right: MergeParams
) -> pd.DataFrame:
    dfp = left.df()
    dfb = right.df()
    with Spinner(f"Merging by {','.join(left.columns)}"
        f" / {','.join(right.columns)}"
    ) as progress:
        res = dfp.merge(dfb, left_on=left.columns, right_on=right.columns)
        progress.console.print(ccze(info(res)))
        return res
