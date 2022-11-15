from pathlib import Path
from bottle import route, static_file, run
from htmltags import *

bulma_css_path = "/static/css/bulma.min.css"
htmx_path = "/static/js/htmx.min.js"

bulma_css = link(
    rel="stylesheet", href=bulma_css_path
)

htmx_src = script(src=htmx_path)

def replaceable_button(url="/removed", content="Click me to remove"):
    return button(content, hx_trigger="click", hx_swap="outerHTML", hx_get=url, class_="button is-primary")

def home_page(greeting):
    return html(
        head(title("A Test of HTML generation"), bulma_css),
        body(
            main(
                h1("A Test of HTML generation", class_="title"),
                details(
                    summary("What could be down below?"),
                    p("It's just leeeeeeeeeeeeeeeeeeeeeeeengthy text"),
                    class_="box"
                ),
                p(greeting, class_="box"),
                replaceable_button(),
                div('<script>alert("evil!")</script>', id="mydiv", class_="box"),
                htmx_src,
                class_="container"
            )
        ),
    )

@route(bulma_css_path)
def bulmacss():
    return static_file("bulma.min.css", root=Path(__file__).parent / "assets/css")

@route(htmx_path)
def htmx():
    return static_file("htmx.min.js", root=Path(__file__).parent / "assets/js")

@route('/hello/<name>')
def hello(name):
    return str(home_page(f"hi {name}!"))

@route('/removed')
def hello():
    return str(p("You got replaced!", class_="notification"))

run(host='localhost', port=8080, debug=True, reloader=True)