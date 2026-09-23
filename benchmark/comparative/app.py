import pylage as pl

count = pl.state(0)

def increment():
    count.set(count.value + 1)
    return count.value

button = pl.button("Increment", on_click=increment)

app = pl.column(
    pl.heading(count),
    button,
)
