import click
from pathlib import Path
from ebe.df.merge import Merge
from typing import Optional

from ebe.df.php_array import PhpArray


@click.group()
def cli():
    pass


@cli.command("merge", help="Merges two csv files by matching columns")
@click.argument("left")
@click.argument("right")
@click.option("-l", "--left-columns", multiple=True)
@click.option("-r", '--right-columns', multiple=True)
@click.option("-o", "--output")
def cli_merge(
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
    merge_result = Merge.execute(
        Merge.params(path=left_path, columns=left_columns),
        Merge.params(path=right_path, columns=right_columns)
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


@cli.command("phparray", help="Merges two csv files by matching columns")
@click.argument("csv")
@click.option("-v", "--values", multiple=True)
@click.option("-k", '--key', type=str)
def cli_phparray(
    csv: str,
    values: list[str],
    key: Optional[str] = None,
    output: Optional[str] = None
):
    csv_path = Path(csv)
    assert csv_path.exists()
    _ = PhpArray.execute(
        PhpArray.params(
            path=csv_path,
            values=values,
            key=key
        ),
    )
    # if not output:
    #     output_path = Path(
    #         ".") / f"{left_path.stem}-{right_path.stem}-merge.csv"
    # else:
    #     output_path = Path(output)
    # merge_result.to_csv(
    #     output_path.as_posix(),
    #     index=False
    # )


if __name__ == "__main__":
    cli()
