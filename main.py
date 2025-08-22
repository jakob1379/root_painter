import importlib.util
import typer

app = typer.Typer(invoke_without_command=True)


@app.callback(invoke_without_command=True)
def _default(ctx: typer.Context):
    """
    If invoked without a subcommand, start the GUI (painter).
    """
    if ctx.invoked_subcommand is None:
        # Import and start the painter GUI entrypoint.
        # Expected function: painter.root_painter.main.init_root_painter()
        import painter.root_painter.main as rp_main
        rp_main.init_root_painter()


def run_trainer():
    """
    Start the trainer (server).
    Usage: root-painter trainer
    """
    # Expected function: trainer.root_painter_trainer.start()
    import trainer.root_painter_trainer as trainer_pkg
    trainer_pkg.start()


# Register the 'trainer' command only if the optional server component is installed.
if importlib.util.find_spec("trainer.root_painter_trainer") is not None:
    app.command("trainer")(run_trainer)


def main():
    app()


if __name__ == "__main__":
    main()
