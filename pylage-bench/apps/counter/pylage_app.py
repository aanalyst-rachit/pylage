import pylage as pl

count = pl.state(0)

def increment():
    count.set(count.value + 1)

app = pl.column(
    pl.heading("Counter"),
    pl.text(count),
    pl.button("Increment", on_click=increment),
)

if __name__ == "__main__":
    pl.run(app, title="PyLage Counter", host="127.0.0.1", port=3001, serve=True)
