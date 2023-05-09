import sys
import click
from pathlib import Path
from ebe.df.merge import Merge
from typing import Optional
import logging
from pyfiglet import Figlet
from ebe.df.php_array import PhpArray
from ebe.ui.items import MenuItem, MergeOperationItem, TaskItem
from ebe.ui.menu import Menu
from ebe.version import __version__


def banner(txt: str, color: str = "bright_green"):
    logo = Figlet(font="poison", width=120).renderText(text=txt)
    click.secho(logo, fg=color)


def echo(txt: str, color="bright_blue"):
    click.secho(txt, fg=color)


def error(e: Exception, txt: Optional[str] = None):
    if not txt:
        txt = f"{e}"
    click.secho(txt, fg="bright_red", err=True)
    if e:
        logging.debug(txt, exc_info=e)


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx: click.Context):
    if ctx.invoked_subcommand is None:
        ctx.invoke(main_menu)


@cli.command("quit")
def quit():
    """Quit."""
    echo("Bye!", color="blue")
    sys.exit(0)


@cli.command("menu", short_help="My Tasks")
@click.pass_context
def main_menu(ctx: click.Context):
    try:
        click.clear()
        banner(txt=f"eBe {__version__}", color="bright_blue")
        menu_items = [
            MergeOperationItem(text="Merge", obj=Merge, cmd=cli_merge),
            MenuItem(text="PhpArray", obj=PhpArray, cmd=cli_phparray),
        ] + [MenuItem(text="Exit", cmd=quit)]
        with Menu(menu_items, title="Select task") as item:  # type: ignore
            if isinstance(item, TaskItem):
                args = item.get_input()
                ctx.forward(item.cmd, **args)
            match item.cmd:
                case click.Command():
                    ctx.invoke(item.cmd)
    except Exception as e:
        error(e)


@cli.command("merge", help="Merges two csv files by matching columns")
@click.pass_context
@click.argument("left")
@click.argument("right")
@click.option("-l", "--left-columns", multiple=True)
@click.option("-r", '--right-columns', multiple=True)
@click.option("-o", "--output")
def cli_merge(
    ctx: click.Context,
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
    click.pause()
    if parent := ctx.parent:
        if parent != ctx.find_root():
            click.clear()
            ctx.invoke(parent.command)


@cli.command("phparray", help="Merges two csv files by matching columns")
@click.pass_context
@click.argument("csv")
@click.option("-v", "--values", multiple=True)
@click.option("-k", '--key', type=str)
@click.option("-c", '--comment', type=str)
@click.option("-o", "--output")
def cli_phparray(
    ctx: click.Context,
    csv: str,
    values: list[str],
    key: Optional[str] = None,
    comment: Optional[str] = None,
    output: Optional[str] = None
):
    csv_path = Path(csv)
    assert csv_path.exists()
    php_array = PhpArray.execute(
        PhpArray.params(
            path=csv_path,
            values=values,
            key=key,
            comment=comment
        ),
    )
    if not output:
        output_path = Path(
            ".") / f"{csv_path.stem}-phparray.php"
    else:
        output_path = Path(output)
    output_path.write_text(php_array)
    echo(f"Generated array is stored into {output_path}")
    if parent := ctx.parent:
        if parent != ctx.find_root():
            click.pause()
            click.clear()
            ctx.invoke(parent.command)


if __name__ == "__main__":
    cli()
