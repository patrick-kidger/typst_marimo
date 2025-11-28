import marimo


__generated_with = "0.17.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import matplotlib.pyplot as plt
    import typst_marimo

    x = plt.plot([0, 1, 2], [3, 4, 5])
    y = x
    typst_marimo.export_image_to_typst(y)
    return


if __name__ == "__main__":
    app.run()
