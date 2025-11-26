# typst-marimo

Generate images and values in a Marimo notebook; load them in Typst.

This is essentially a thin wrapper around matplotlib's `savefig` and Typst's `image`, with some guards:

- a checksum to be sure that the images are up-to-date;
- impossible to save two different images under the same name.

## Installation

```bash
pip install typst-marimo
```

## Usage

In Marimo:
```python
import matplotlib.pyplot as plt
from typst_marimo import export_image_to_typst, export_value_to_typst

x = plt.plot(...)

# Usage is `export_image_to_typst(x)`, called from within a Marimo cell (not within a
# function) on a matplotlib object.
#
# This will save the image under `x.png`, using the name of the variable. Marimo
# requires all global variables to have unique names, so this safely avoids the
# possibility of accidentally using the same name twice.
#
# This command will also save `.typst-marimo/lib.typ` for loading from Typst.
export_image_to_typst(x)

y = "37 #sym.degree;C"

# Usage is `export_value_to_typst(y)`. Same as the above, but instead of saving a image
# then we save `str(y)`, and evaluate this as Typst code when imported.
export_value_to_typst(y)
```

Then run your marimo notebook, either via `marimo ... your-notebook.py` or via `python your-notebook.py`. This will save and generate your images, along with a checksum that they are up-to-date.

In Typst:
```typst
#import ".typst-marimo/lib.typ": import-image-from-marimo, import-value-from-marimo

// Usage is `import-image-from-marimo(notebook, variable, ..args)`, with
// remaining arguments passed on to `image`.
//
// Importantly (the whole point of this package), it will error out if the
// image is not up-to-date.
#let my-image = import-image-from-marimo("your-notebook.py", "x", width: 50%)

// Usage is `import-value-from-marimo(notebook, variable, mode)`.
//
// `mode` is the same as in `eval(..., mode: ...)`, and must be one of `"markup"`,
// `"math"` or `"code"`.
#let my-value = import-value-from-marimo("your-notebook.py", "y", mode: "markup")
```

## FAQ

**Typst incorrectly states that the Marimo notebook is out of date?**

Marimo is happy to ignore some whitespace changes and in this case will avoid recompiling; Typst is not so lenient about detecting this. The easiest way to resolve this is to force a re-run of the whole notebook, via the 'Restart kernel' command in Marimo.
