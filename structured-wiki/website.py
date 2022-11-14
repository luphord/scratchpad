from pathlib import Path
from bottle import route, static_file, run
from htmltags import *

water_css_path = "/static/css/water.css"
htmx_path = "/static/js/htmx.min.js"

water_css = link(
    rel="stylesheet", href=water_css_path
)

htmx_src = script(src=htmx_path)

def home_page(greeting):
    return html(
        head(title("A Test of HTML generation"), water_css),
        body(
            h1("A Test of HTML generation"),
            details(
                summary("What could be down below?"),
                p("It's just leeeeeeeeeeeeeeeeeeeeeeeengthy text"),
            ),
            p(greeting),
            div('<script>alert("evil!")</script>', id="mydiv"),
            htmx_src
        ),
    )

@route(water_css_path)
def watercss():
    return static_file("water.css", root=Path(__file__).parent / "assets/css")

@route(htmx_path)
def htmx():
    return static_file("htmx.min.js", root=Path(__file__).parent / "assets/js")

@route('/hello/<name>')
def hello(name):
    return str(home_page(f"hi {name}!"))

run(host='localhost', port=8080, debug=True, reloader=True)