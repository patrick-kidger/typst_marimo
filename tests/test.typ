#import ".typst-marimo/lib.typ": import-image-from-marimo, import-value-from-marimo

#assert.eq(import-value-from-marimo("notebook.py", "x", mode: "code"), 1234)
#import-image-from-marimo("notebook.py", "y", width: 50%)
#import-value-from-marimo("notebook.py", "z", mode: "markup")
