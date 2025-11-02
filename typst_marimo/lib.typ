#import "@preview/digestify:0.1.0": sha1

#let _check_digest(notebook) = {
  assert(notebook.split("/").len() == 1, message: "Traversing the filesystem is not supported.")
  assert(notebook.ends-with(".py"), message: "`notebook-name` must be a `.py` file.")
  let file-digest = sha1(read("../" + notebook, encoding: none))
  assert.eq(file-digest, read(notebook + "/" + "checksum", encoding: none), message: "typst-marimo checksum does not match; re-run your Marimo notebook.")
}

#let import-image-from-marimo(notebook, name, ..args) = {
  _check_digest(notebook)
  image(notebook + "/" + name + ".png", ..args)
}

#let import-value-from-marimo(notebook, name, mode: none) = {
  assert(mode != none, message: "Must pass keyword argument `mode`, as either `\"code\"`, `\"markup\"`, or `\"math\"`.")
  _check_digest(notebook)
  eval(read(notebook + "/" + name), mode: mode)
}
