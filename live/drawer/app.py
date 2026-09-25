import pylage as pl


if __name__ == "__main__":
    pl.run(
        pages_dir="live/drawer/pages",
        title="PyLage Drawer Live Test",
        serve=True,
        host="0.0.0.0",
        port=3010,
    )
