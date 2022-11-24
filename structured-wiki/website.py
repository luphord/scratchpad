from pathlib import Path
from collections import Counter
import random
from datetime import datetime
from uuid import uuid4
from bottle import Bottle, request, static_file
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


def random_client_id():
    return f"dom-{random.getrandbits(8*8):0x}"


counts = Counter()


def counter(prefix, server_id, do_increment):
    global counts
    if do_increment:
        counts[server_id] += 1
    return div(
        div(
            div(f"Count of '{server_id}' is {counts[server_id]}", class_="box"),
            class_="column is-three-quarters",
        ),
        div(
            button(
                "Increment",
                hx_trigger="click",
                hx_swap="outerHTML",
                hx_put=f"{prefix}/{server_id}",
                class_="button is-info",
            ),
            class_="column is-one-quarter",
        ),
        class_="columns",
        hx_target="this",
    )


def console_window(url):
    return div(
        div(id="lines", class_="box"),
        div(
            input(
                name="line",
                type="text",
                placeholder="Type some text and press enter...",
                hx_trigger="keydown[key=='Enter']",
                hx_post=url,
                hx_target="#lines",
                hx_swap="beforeend",
                class_="input",
            ),
        ),
        class_="box",
    )


def home_page(greeting):
    return html(
        head(title("A Test of HTML generation"), bulma_css),
        body(
            navbar("My Page", ["First", "Second", "Third"]),
            main(
                h1("A Test of HTML generation", class_="title"),
                div(hx_trigger="load", hx_swap="outerHTML", hx_get="/counter/first"),
                div(hx_trigger="load", hx_swap="outerHTML", hx_get="/counter/second"),
                div(hx_trigger="load", hx_swap="outerHTML", hx_get="/counter/first"),
                console_window("/line"),
                details(
                    summary("What could be down below?"),
                    p("It's just leeeeeeeeeeeeeeeeeeeeeeeengthy text"),
                    class_="box",
                ),
                p(greeting, class_="box"),
                replaceable_button(f"/removed/{uuid4()}"),
                div('<script>alert("evil!")</script>', id="mydiv", class_="box"),
                htmx_src,
                class_="container",
            ),
        ),
    )


myapp = Bottle()


@myapp.route("/static/<path:path>")
def static_files(path):
    return static_file(path, root=Path(__file__).parent / "assets")


@myapp.route("/")
@myapp.route("/hello/<name>")
def hello(name="anonymous"):
    return home_page(f"hi {name}!")


@myapp.get("/counter/<id>")
def get_counter(id):
    return counter("/counter", id, False)


@myapp.put("/counter/<id>")
def increment_counter(id):
    return counter("/counter", id, True)


@myapp.post("/line")
def line():
    return p(f"{datetime.now()} >>> {request.forms.get('line')}")


remove_count = 0


@myapp.route("/removed/<id>")
def hello(id):
    global remove_count
    remove_count += 1
    return article(
        div(
            p("You got replaced!"),
            button(
                class_="delete",
                hx_target=f"#my{id}",
                hx_trigger="click",
                hx_get=f"/removed/{id}",
            ),
            class_="message-header",
        ),
        div(
            "This replacement was triggered by a button click "
            f"and executed via htmx {remove_count} times. The content was sent by the server."
            f" Route is {vars(request['bottle.route'])}",
            class_="message-body",
        ),
        class_="message",
        id=f"my{id}",
    )


print(f"{id(myapp):0x}")
myapp.run(host="localhost", port=8080, debug=True, reloader=True)
