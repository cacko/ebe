import io
from pandas import DataFrame


def info(
    df: DataFrame,
    verbose: bool | None = False,
    max_cols: int | None = True,
    memory_usage: bool | str | None = True,
    show_counts: bool | None = True,
) -> str:
    buff = io.StringIO()
    df.info(
        verbose,
        buff,
        max_cols,
        memory_usage,
        show_counts,
    )
    return buff.getvalue()
