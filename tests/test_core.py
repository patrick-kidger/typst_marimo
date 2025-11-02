import pathlib
import shutil
import subprocess

import pytest


_here = pathlib.Path(__file__).resolve().parent


@pytest.mark.parametrize("call_directly", (False, True))
def test_core(call_directly: bool, tmp_path: pathlib.Path):
    assert not (_here / ".typst-marimo").exists()
    shutil.copy(_here / "test.typ", tmp_path / "test.typ")
    shutil.copy(_here / "notebook.py", tmp_path / "notebook.py")
    assert not (tmp_path / ".typst-marimo").exists()

    assert (
        subprocess.run(
            ["typst", "compile", "test.typ"], cwd=tmp_path, check=False
        ).returncode
        != 0
    )

    if call_directly:
        subprocess.run(["python", "notebook.py"], cwd=tmp_path, check=True)
    else:
        subprocess.run(
            ["marimo", "export", "html", "notebook.py"], cwd=tmp_path, check=True
        )
    assert (tmp_path / ".typst-marimo").exists()

    subprocess.run(["typst", "compile", "test.typ"], cwd=tmp_path, check=True)
    assert not (_here / ".typst-marimo").exists()

    # Cache bust
    notebook = tmp_path / "notebook.py"
    notebook.write_text(notebook.read_text() + "\n")
    assert (
        subprocess.run(
            ["typst", "compile", "test.typ"], cwd=tmp_path, check=False
        ).returncode
        != 0
    )


@pytest.mark.parametrize("call_directly", (False, True))
def test_broken(call_directly, tmp_path):
    for broken in ("broken1.py", "broken2.py"):
        shutil.copy(_here / broken, tmp_path / broken)
        if call_directly:
            p = subprocess.run(["python", broken], cwd=tmp_path, check=False, capture_output=True)
        else:
            p = subprocess.run(
                ["marimo", "export", "html", broken], cwd=tmp_path, check=False, capture_output=True
            )
        assert p.returncode != 0
        assert "The provided argument cannot be found in the Marimo globals." in p.stderr.decode()
