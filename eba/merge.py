import pandas as pd
from pathlib import Path
from pydantic import BaseModel
from progressor import UndeterminedProgress, WithTask


class MergeParams(BaseModel):
    path: Path
    columns: list[str]

    def df(self, progress: UndeterminedProgress) -> pd.DataFrame:
        task_id = progress.add_task(f"Loading {self.path.name}", total=None)
        with WithTask(progress, task_id=task_id):
            return pd.read_csv(self.path.as_posix(), low_memory=False)


def merge(
    left: MergeParams,
    right: MergeParams
) -> pd.DataFrame:
    with UndeterminedProgress(title="Merging") as progress:
        dfp = left.df(progress)
        # dfp.info(verbose=False, show_counts=True)
        dfb = right.df(progress)
        # dfb.info(verbose=False, show_counts=True)
        with WithTask(progress, task_id=progress.add_task(
            f"Merging by {','.join(left.columns)}"
            f" / {','.join(right.columns)}"
        )):
            res = dfp.merge(dfb, left_on=left.columns, right_on=right.columns)
            res.info(verbose=False, show_counts=True)
            return res
