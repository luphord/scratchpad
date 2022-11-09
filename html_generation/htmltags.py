from typing import Iterable, Union

HTMLContent = Union["HTMLElement", str]

_escaped_attrs = ("id", "class", "type")


class HTMLElement(object):
    tag = "div"  # type: str
    render_compact = False  # type: bool

    def __init__(self, *content: HTMLContent, **attributes: str) -> None:
        self.content = list(content)
        self.attributes = attributes
        for a in _escaped_attrs:
            if "_" + a in self.attributes:
                self.attributes[a] = self.attributes.pop("_" + a)

    def append(self, *items: HTMLContent) -> "HTMLElement":
        self.content += items
        return self

    def __call__(self, *items: HTMLContent) -> "HTMLElement":
        return self.append(*items)

    def subelement(self, item: "HTMLElement") -> "HTMLElement":
        self.content.append(item)
        return item

    def lazy_render_attributes(self) -> Iterable[str]:
        if self.attributes:
            for k, v in self.attributes.items():
                yield " "
                yield str(k)
                yield '="'
                yield str(v)
                yield '"'

    def lazy_render(self, indent: str = "", add_indent: str = "") -> Iterable[str]:
        is_doc_root = self.tag.lower() == "html"
        if is_doc_root:
            yield "<!DOCTYPE HTML>\n"
        do_linebreak = not self.render_compact and self.content
        yield indent
        yield "<"
        yield self.tag
        yield from self.lazy_render_attributes()
        yield ">"
        if do_linebreak:
            yield "\n"
        child_indent = indent + add_indent if do_linebreak else ""
        if not do_linebreak:
            add_indent = ""
        for child in self.content:
            if isinstance(child, HTMLElement):
                yield from child.lazy_render(child_indent, add_indent)
            else:
                yield "{}{}".format(child_indent, child)
            if do_linebreak:
                yield "\n"
        if do_linebreak:
            yield indent
        yield "</"
        yield self.tag
        yield ">"
        if is_doc_root:
            yield "\n"

    def __str__(self) -> str:
        """Render element to string.
        >>> str(a('Somewhere', href="#"))
        '<a href="#">Somewhere</a>'
        >>> str(p())
        '<p></p>'
        >>> str(div('Hello World'))
        '<div>\\n  Hello World\\n</div>'
        >>> str(table())
        '<table></table>'
        """
        return "".join(self.lazy_render(add_indent="  "))

    def write(self, fname: str) -> None:
        with open(fname, "w") as f:
            for s in self.lazy_render(add_indent="  "):
                f.write(s)


# TAGS


class a(HTMLElement):
    tag = "a"
    render_compact = True


class article(HTMLElement):
    tag = "article"
    render_compact = False


class body(HTMLElement):
    tag = "body"
    render_compact = False


class button(HTMLElement):
    tag = "button"
    render_compact = True


class div(HTMLElement):
    tag = "div"
    render_compact = False


class footer(HTMLElement):
    tag = "footer"
    render_compact = False


class form(HTMLElement):
    tag = "form"
    render_compact = False


class h1(HTMLElement):
    tag = "h1"
    render_compact = True


class h2(HTMLElement):
    tag = "h2"
    render_compact = True


class h3(HTMLElement):
    tag = "h3"
    render_compact = True


class h4(HTMLElement):
    tag = "h4"
    render_compact = True


class head(HTMLElement):
    tag = "head"
    render_compact = False


class header(HTMLElement):
    tag = "header"
    render_compact = False


class hr(HTMLElement):
    tag = "hr"
    render_compact = False


class html(HTMLElement):
    tag = "html"
    render_compact = False


class img(HTMLElement):
    tag = "img"
    render_compact = False


class li(HTMLElement):
    tag = "li"
    render_compact = True


class link(HTMLElement):
    tag = "link"
    render_compact = False


class meta(HTMLElement):
    tag = "meta"
    render_compact = False


class nav(HTMLElement):
    tag = "nav"
    render_compact = False


class ol(HTMLElement):
    tag = "ol"
    render_compact = False


class p(HTMLElement):
    tag = "p"
    render_compact = True


class small(HTMLElement):
    tag = "small"
    render_compact = True


class span(HTMLElement):
    tag = "span"
    render_compact = True


class style(HTMLElement):
    tag = "style"
    render_compact = False


class table(HTMLElement):
    tag = "table"
    render_compact = False


class tbody(HTMLElement):
    tag = "tbody"
    render_compact = False


class td(HTMLElement):
    tag = "td"
    render_compact = True


class th(HTMLElement):
    tag = "th"
    render_compact = False


class thead(HTMLElement):
    tag = "thead"
    render_compact = False


class title(HTMLElement):
    tag = "title"
    render_compact = True


class tr(HTMLElement):
    tag = "tr"
    render_compact = False


class ul(HTMLElement):
    tag = "ul"
    render_compact = False
