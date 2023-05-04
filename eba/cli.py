import click
from pathlib import Path
from eba.merge import merge, MergeParams
from typing import Optional


@click.group()
def cli():
    pass


@cli.command("merge", help="Merges two csv files by matching columns")
@click.argument("left")
@click.argument("right")
@click.option("-l", "--left-columns", multiple=True)
@click.option("-r", '--right-columns', multiple=True)
@click.option("-o", "--output")
def cli_params(
    left: str,
    right: str,
    left_columns: list[str],
    right_columns: list[str],
    output: Optional[str] = None
):
    left_path = Path(left)
    right_path = Path(right)
    assert left_path.exists()
    assert right_path.exists()
    merge_result = merge(
        MergeParams(path=left_path, columns=left_columns),
        MergeParams(path=right_path, columns=right_columns)
    )
    if not output:
        output_path = Path(
            ".") / f"{left_path.stem}-{right_path.stem}-merge.csv"
    else:
        output_path = Path(output)
    merge_result.to_csv(
        output_path.as_posix(),
        index=False
    )


if __name__ == "__main__":
    cli()
