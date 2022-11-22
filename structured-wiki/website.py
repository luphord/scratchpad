from pathlib import Path
from bottle import route, static_file, run
from htmltags import *

bulma_css_path = "/static/css/bulma.min.css"
htmx_path = "/static/js/htmx.min.js"

bulma_css = link(rel="stylesheet", href=bulma_css_path)

htmx_src = script(src=htmx_path)


def navbar(brand_content, items):
    brand = div(a(brand_content, href="/", class_="navbar-item"), _class="navbar-brand")
    links = div(
        div(*[a(item, class_="navbar-item") for item in items], class_="navbar-start"),
        div(a("Login", class_="navbar-item"), class_="navbar-end"),
        _class="navbar-menu",
    )
    return nav(brand, links, class_="navbar is-fixed-top is-info")


def replaceable_button(url, content="Click me to remove"):
    return button(
        content,
        hx_trigger="click",
        hx_swap="outerHTML",
        hx_get=url,
        class_="button is-info",
    )


def home_page(greeting):
    return html(
        head(title("A Test of HTML generation"), bulma_css),
        body(
            navbar("My Page", ["First", "Second", "Third"]),
            main(
                h1("A Test of HTML generation", class_="title"),
                details(
                    summary("What could be down below?"),
                    p("It's just leeeeeeeeeeeeeeeeeeeeeeeengthy text"),
                    class_="box",
                ),
                p(greeting, class_="box"),
                replaceable_button(f"/removed/myid"),
                div('<script>alert("evil!")</script>', id="mydiv", class_="box"),
                htmx_src,
                class_="container",
            ),
        ),
    )


@route(bulma_css_path)
def bulmacss():
    return static_file("bulma.min.css", root=Path(__file__).parent / "assets/css")


@route(htmx_path)
def htmx():
    return static_file("htmx.min.js", root=Path(__file__).parent / "assets/js")


@route("/hello/<name>")
def hello(name):
    return str(home_page(f"hi {name}!"))


remove_count = 0


@route("/removed/<id>")
def hello(id):
    global remove_count
    remove_count += 1
    return str(
        article(
            div(
                p("You got replaced!"),
                button(
                    class_="delete",
                    hx_target=f"#{id}",
                    hx_trigger="click",
                    hx_get=f"/removed/{id}",
                ),
                class_="message-header",
            ),
            div(
                "This replacement was triggered by a button click "
                f"and executed via htmx {remove_count} times. The content was sent by the server.",
                class_="message-body",
            ),
            class_="message",
            id=id,
        )
    )


run(host="localhost", port=8080, debug=True, reloader=True)
