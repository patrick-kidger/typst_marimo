import marimo


__generated_with = "0.17.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import matplotlib.pyplot as plt
    import typst_marimo

    _x = plt.plot([0, 1, 2], [3, 4, 5])
    typst_marimo.export_image_to_typst(_x)
    return


if __name__ == "__main__":
    app.run()
