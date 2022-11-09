from htmltags import *

water_css = link(
    rel="stylesheet", href="https://cdn.jsdelivr.net/npm/water.css@2/out/dark.css"
)

# Some test elements adapted from https://watercss.kognise.dev/
print(
    html(
        head(title("A Test of HTML generation"), water_css),
        body(
            h1("A Test of HTML generation"),
            details(
                summary("What could be down below?"),
                p("It's just leeeeeeeeeeeeeeeeeeeeeeeengthy text"),
            ),
            div('Hello World <script>alert("evil!")</script>', id="mydiv"),
            div(
                button("Open dialog", id="dialog-trigger", type="button"),
                span(id="dialog-result"),
            ),
            dialog(
                header("My Dialog"),
                form(
                    p("some content"),
                    menu(button("Alright", value="ok"), button("Nope", value="not ok")),
                ),
                id="dialog",
            ),
            script(
                """document.getElementById("dialog-trigger").addEventListener("click", (function () { document.getElementById("dialog-result").innerText = "", document.getElementById("dialog").showModal() })), document.getElementById("dialog").addEventListener("close", (function (e) { document.getElementById("dialog-result").innerText = "Your answer: ".concat(e.target.returnValue) }))"""
            ),
        ),
    )
)
