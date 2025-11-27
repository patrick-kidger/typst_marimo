import marimo

__generated_with = "0.17.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import matplotlib.pyplot as plt
    import typst_marimo

    x = "1234"
    y = plt.plot([0, 1, 2], [3, 4, 5])
    z = "37 #sym.degree;C"
    typst_marimo.export_value_to_typst(x)
    typst_marimo.export_image_to_typst(y)
    typst_marimo.export_value_to_typst(z)
    return


if __name__ == "__main__":
    app.run()
