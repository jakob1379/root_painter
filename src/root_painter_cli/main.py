import importlib.util
import importlib.metadata
import typer
from typing import Optional

app = typer.Typer(invoke_without_command=True)


def _find_first_dist_version(*names: str) -> Optional[str]:
    """Return the first found installed distribution version for the given names."""
    for name in names:
        try:
            return importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            continue
    return None


def _version_callback(ctx: typer.Context, param, value: bool):
    """Print component versions and exit when --version is passed.

    This uses a Typer/Click option callback so the option is eager and
    shown/handled before normal command execution.
    """
    if not value or ctx.resilient_parsing:
        return

    painter_version = _find_first_dist_version("root-painter-painter", "root-painter", "root_painter")
    trainer_version = _find_first_dist_version("root-painter-trainer-jakob1397", "root-painter-trainer")

    # Compose and print a friendly, multi-line version summary.
    typer.echo(f"Painter: {painter_version if painter_version is not None else 'not installed'}")
    typer.echo(f"Trainer: {trainer_version if trainer_version is not None else 'not installed'}")
    ctx.exit()


trainer_installed = importlib.util.find_spec("root_painter_trainer") is not None

if trainer_installed:
    help_text = """
    Launch the Painter graphical application (default).

    By default, running `root-painter` with no subcommand starts the GUI (Painter).

    The optional `trainer` subcommand is installed and available:

      root-painter trainer --help
    """
else:
    help_text = """
    Launch the Painter graphical application (default).

    By default, running `root-painter` with no subcommand starts the GUI (Painter).

    To expose the optional `trainer` subcommand (a server component for training),
    install the trainer extra in this workspace and re-sync the environment:

      uv sync --extra trainer

    Alternatively, when installing from source or from a wheel you can enable
    the trainer extra using the PEP 508 extras syntax:

      pip install 'root-painter[trainer]'

    After installing the extra, the `trainer` subcommand will be available:

      root-painter trainer --help
    """

@app.callback(invoke_without_command=True, help=help_text)
def _default(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", "-V", callback=_version_callback, is_eager=True, help="Show component versions and exit."),
):
    """Launch the Painter graphical application (default)."""
    if ctx.invoked_subcommand is None:
        # Import and start the painter GUI entrypoint from the painter package
        # Expected function: root_painter.main.init_root_painter()
        import root_painter.main as rp_main
        rp_main.init_root_painter()


def run_trainer():
    """
    Start the trainer (server).
    Usage: root-painter trainer
    """
    # If the trainer package isn't installed, show a helpful message and exit.
    if importlib.util.find_spec("root_painter_trainer") is None:
        typer.echo(
            "The 'trainer' optional component is not installed.\n\n"
            "Enable it using one of the following commands:\n\n"
            "  uv sync --extra trainer\n\n"
            "or\n\n"
            "  pip install 'root-painter[trainer]'\n",
            err=True,
        )
        raise typer.Exit(code=2)

    # Expected function: root_painter_trainer.start()
    import root_painter_trainer as trainer_pkg
    trainer_pkg.start()


# Ensure the 'trainer' command is always visible, but mark it as not installed when missing.
trainer_help = "Start the trainer (server)."
if importlib.util.find_spec("root_painter_trainer") is None:
    trainer_help += " [not installed — install optional extra to enable]"
# Set the function docstring so Typer/Click shows the status in help.
run_trainer.__doc__ = trainer_help

app.command("trainer")(run_trainer)


def main():
    app()


if __name__ == "__main__":
    main()
