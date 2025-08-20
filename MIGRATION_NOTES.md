Summary of changes:
- Added a CLI entrypoint "root-painter" via pyproject.toml (PEP 621 [project.scripts]).
- Added main.py which exposes two behaviors:
  - Running "root-painter" with no subcommand launches the painter GUI by calling painter.root_painter.main.init_root_painter().
  - Running "root-painter trainer" calls trainer.root_painter_trainer.start().

Install & test (from repo root):
```bash
pip install -e .
```

Run:
```bash
root-painter
```
```bash
root-painter trainer
```

Package & publish with uv:
- Ensure you have uv (and an up-to-date build tool) installed and credentials/configured for PyPI.
```bash
python -m pip install --upgrade build uv
```
```bash
uv build
```
```bash
uv publish
```

Notes:
- If the actual entrypoint function names differ, update main.py to call the correct functions.
- Qt GUIs must usually run on the main thread; this implementation calls the GUI directly when no subcommand is given.
- If you prefer a different build backend (hatchling, flit, etc.) we can adapt the [build-system] and setuptools sections accordingly.
