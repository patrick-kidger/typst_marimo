import hashlib
import pathlib
import shutil
import sys
from collections.abc import Callable
from typing import cast, TypeVar

import matplotlib.artist
import matplotlib.figure


_here = pathlib.Path(__file__).resolve().parent
_main = sys.modules["__main__"]
if "marimo" not in sys.modules:
    raise ValueError(
        "typst-marimo must be used from within Marimo. However, Marimo has not been "
        "imported."
    )
_notebook_filepath_str = _main.__file__
_notebook_filepath = pathlib.Path(cast(str, _notebook_filepath_str)).resolve()
_base_outdir = _notebook_filepath.parent / ".typst-marimo"
_outdir = _base_outdir / _notebook_filepath.name

_last_modified: None | int = None


def _clear():
    global _last_modified
    # Clean out directory on first call.
    # Note that we can't do this dynamically during saving, as Marimo caches cell
    # results, so we don't know which figures that we want to keep around.
    _outdir.mkdir(parents=True, exist_ok=True)
    if _last_modified is None:
        if _outdir.exists():
            for elem in _outdir.iterdir():
                elem.unlink()
        shutil.copy(_here / "lib.typ", _base_outdir / "lib.typ")
    # Update the checksum if necessary. This is to prevent Typst from allowing
    # compilation without also having up-to-date figures.
    modified = _notebook_filepath.stat().st_mtime_ns
    if modified != _last_modified:
        _last_modified = modified
        (_outdir / "checksum").write_bytes(
            hashlib.sha1(_notebook_filepath.read_bytes()).digest()
        )


def _get_key(obj):
    # We rely on the fact that Marimo itself does not allow multiple global variables
    # with the same name. This ensures that each of our outputs has a unique name.
    keys = []
    for key in dir(_main):
        if getattr(_main, key) is obj and not key.startswith("_"):
            keys.append(key)
    if len(keys) == 0:
        raise ValueError("The provided argument cannot be found in the Marimo globals.")
    if len(keys) > 1:
        raise ValueError(
            f"Multiple arguments with this value are found in the Marimo "
            f"globals: {keys}."
        )
    [key] = keys
    return key


def export_image_to_typst[Artist: matplotlib.artist.Artist](
    fig: matplotlib.figure.Figure | matplotlib.artist.Artist | list[Artist],
) -> None:
    if isinstance(fig, matplotlib.figure.Figure):
        fig2 = fig
    elif isinstance(fig, matplotlib.artist.Artist):
        fig2 = fig.figure
    elif isinstance(fig, list) and all(
        isinstance(f, matplotlib.artist.Artist) for f in fig
    ):
        # Return from e.g. `plt.plot(...)`
        [fig2] = {f.figure for f in fig}
    else:
        raise ValueError(f"Received non-figure {type(fig)}")
    assert isinstance(fig2, matplotlib.figure.Figure)
    _clear()
    # Now save the figure. We do *not* cache the call to `fn`: we let Marimo's
    # cell-level caching handle this. Otherwise we may have the same `fn`, whose
    # dependencies change, and which would not then update.
    key = _get_key(fig)
    fig2.savefig(str(_outdir / key) + ".png", bbox_inches="tight")


_T = TypeVar("_T")


def export_value_to_typst(obj: _T, transform: Callable[[_T], str] = str) -> None:
    _clear()
    key = _get_key(obj)
    obj_str = transform(obj)
    if not isinstance(obj_str, str):
        raise ValueError("The result of `transform(obj)` must be a string.")
    (_outdir / key).write_text(obj_str)
