from typing import Mapping, Iterable, TypeVar, Dict, Set, Union, Callable
from collections import defaultdict
from functools import reduce
import operator
from abc import ABC, abstractmethod


T = TypeVar("T")


def invert_dag(dag: Mapping[T, Iterable[T]]) -> Dict[T, Set[T]]:
    """Invert DAG representation from precedents to dependents
    or vice versa.

    >>> invert_dag({1: [2, 3], 2: [3]})
    {2: {1}, 3: {1, 2}}
    >>> invert_dag({"a": ["b", "c"], "b": ["c", "d"], "c": ["d"]}) \
        == {"d": {"b", "c"}, "c": {"b", "a"}, "b": {"a"}}
    True
    >>> invert_dag({1: []})
    {1: set()}
    >>> invert_dag({})
    {}
    """
    inv = defaultdict(set)
    for k, v in dag.items():
        if v:
            for node in v:
                inv[node].add(k)
        else:
            # k has not precedents (or dependents)
            # we have to ensure it does not get lost
            inv[k]
    return dict(inv)


def topological_sort(dag: Mapping[T, Iterable[T]]) -> Iterable[T]:
    """Perform topological sorting by Kahn's algorithm (see
    https://en.wikipedia.org/wiki/Topological_sorting#Kahn.27s_algorithm).
    `dag` is a mapping from a node to its precedents,
    i.e. the nodes it depends on. E.g. dag={1: [2, 3]} means
    that node 1 depends on nodes 2 and 3. Hence [2, 3, 1] or
    [3, 2, 1] would be the valid topological sortings here.

    >>> d1 = {1: [2, 3], 2: [3]}
    >>> list(topological_sort(d1))
    [3, 2, 1]
    >>> d2 = {"a": ["b", "c"], "b": ["c", "d"], "c": ["d"]}
    >>> list(topological_sort(d2)) == list("dcba")
    True
    >>> list(topological_sort({1: []}))
    [1]
    >>> list(topological_sort({}))
    []
    """
    dag = invert_dag(dag)
    s = dag.keys() - set.union(*(dag.values() or [set()]))
    s.update({k for k, v in dag.items() if not v})
    while s:
        node = s.pop()
        yield node
        node_dependents = dag.pop(node, set())
        remaining = set.union(*(dag.values() or [set()]))
        s.update(node_dependents - remaining)
    if dag:
        raise ValueError(f"DAG contains a cycle related to {dag}")


ExpressionLike = Union[int, float, "Expression"]


class Expression(ABC):
    """Abstract base class for all types of expressions including nodes."""

    @staticmethod
    def wrap(o: ExpressionLike) -> "Expression":
        """Wrap a numeric value as a constant expression.
        Return the expression itself if it is already an instance of Expression

        >>> Expression.wrap(1)
        Constant(1)
        >>> Expression.wrap(1.23)
        Constant(1.23)
        >>> Expression.wrap(Constant(5))
        Constant(5)
        """
        if isinstance(o, Expression):
            return o
        elif isinstance(o, int) or isinstance(o, float):
            return Constant(o)
        else:
            raise TypeError(f"Cannot wrap '{o}' of type {type(o)} as expression")

    @property
    @abstractmethod
    def dependencies(self) -> Iterable["Expression"]:
        """Nodes that this expression depends on.

        >>> list((1 + Constant(2) - 3).dependencies)
        []
        >>> list((1 + Constant(2) - Stock()).dependencies)
        [Stock()]
        """
        pass

    @property
    @abstractmethod
    def dependencies_resolving_self(self) -> Iterable["Expression"]:
        pass

    @abstractmethod
    def evaluate(self, context: Mapping["Node", float]) -> float:
        """Evaluate expression in context.

        >>> float((1 + Constant(2) - 3).evaluate({}))
        0.0
        >>> s1, s2 = Stock(), Stock()
        >>> float((s1 + 2 - s2).evaluate({s1: -1, s2: 1}))
        0.0
        """
        pass

    def __add__(self, other: ExpressionLike) -> "Expression":
        """Add other expression-like to self.

        >>> Constant(1) + 2
        Sum(Constant(1), Constant(2))
        >>> Constant(1) + 2 + 3
        Sum(Constant(1), Constant(2), Constant(3))
        """
        return Sum(self, other)

    def __radd__(self, other: ExpressionLike) -> "Expression":
        """Add other expression-like to self.

        >>> 1 + Constant(2)
        Sum(Constant(1), Constant(2))
        >>> 1 + Constant(2) + 3
        Sum(Constant(1), Constant(2), Constant(3))
        """
        return Sum(other, self)

    def __neg__(self) -> "Expression":
        """Negative value of the given expression.

        >>> -Constant(1)
        NegativeOf(Constant(1))
        """
        return NegativeOf(self)

    def __sub__(self, other: ExpressionLike) -> "Expression":
        """Subtract other expression-like from self.

        >>> Constant(1) - 2
        Sum(Constant(1), NegativeOf(Constant(2)))
        >>> Constant(1) - 2 - 3
        Sum(Constant(1), NegativeOf(Constant(2)), NegativeOf(Constant(3)))
        """
        return Sum(self, NegativeOf(other))

    def __rsub__(self, other: ExpressionLike) -> "Expression":
        """Subtract self from other expression-like.

        >>> 1 - Constant(2)
        Sum(Constant(1), NegativeOf(Constant(2)))
        >>> 1 - Constant(2) - 3
        Sum(Constant(1), NegativeOf(Constant(2)), NegativeOf(Constant(3)))
        """
        return Sum(other, NegativeOf(self))

    def __mul__(self, other: ExpressionLike) -> "Expression":
        """Multiply other expression-like with self.

        >>> Constant(1) * 2
        Product(Constant(1), Constant(2))
        >>> Constant(1) * 2 * 3
        Product(Constant(1), Constant(2), Constant(3))
        """
        return Product(self, other)

    def __rmul__(self, other: ExpressionLike) -> "Expression":
        """Multiply other expression-like with self.

        >>> 1 * Constant(2)
        Product(Constant(1), Constant(2))
        >>> 1 * Constant(2) * 3
        Product(Constant(1), Constant(2), Constant(3))
        """
        return Product(other, self)


class Node(Expression):
    """Abstract base class for all nodes."""

    @property
    def dependencies(self) -> Iterable["Expression"]:
        yield self


class Stock(Node):
    """A node representing a state to be observerd. Grows (or diminishes) with the flows
    leading to it (or coming from it).

    >>> Stock()
    Stock()
    >>> Stock("test")
    Stock('test')
    >>> Stock(label="test")
    Stock('test')
    """

    def __init__(self, label: str = None):
        self.label = label

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.label) if self.label else ''})"

    @property
    def dependencies_resolving_self(self) -> Iterable["Expression"]:
        return self.dependencies

    def evaluate(self, context: Mapping["Node", float]) -> float:
        # Stocks cannot be computed explicitly, their value is obtained by
        # solving the system of ordinary differential equations defined by the model
        return context[self]


class Flow(Node):
    """Flow from one Stock to another. Adds up to first derivative of Stock.

    >>> Flow()
    Flow(None, None, None, Constant(0))
    >>> Flow("flow", Stock("one"), Stock("two"), Constant(1) + 2)
    Flow('flow', Stock('one'), Stock('two'), Sum(Constant(1), Constant(2)))
    """

    def __init__(
        self,
        label: str = None,
        source: Node = None,
        sink: Node = None,
        value: ExpressionLike = 0,
    ):
        self.label = label
        self.source = source
        self.sink = sink
        self.value = Expression.wrap(value)

    def __repr__(self):
        args = [repr(self.label), repr(self.source), repr(self.sink), repr(self.value)]
        return f"{self.__class__.__name__}({', '.join(args)})"

    @property
    def dependencies_resolving_self(self) -> Iterable["Expression"]:
        return self.value.dependencies

    def evaluate(self, context: Mapping["Node", float]) -> float:
        return self.value.evaluate(context)


class NonNode(Expression):
    """Abstract base class for all non-node expressions."""

    @property
    def dependencies_resolving_self(self) -> Iterable["Expression"]:
        return self.dependencies


class Constant(NonNode):
    """Constant value over time."""

    def __init__(self, constant: float):
        self.constant = constant

    def __repr__(self):
        return f"{self.__class__.__name__}({self.constant})"

    @property
    def dependencies(self) -> Iterable["Expression"]:
        yield from ()

    def evaluate(self, context: Mapping["Node", float]) -> float:
        return self.constant


class Sum(NonNode):
    """Sum of multiple expressions."""

    def __init__(self, *summands):
        summands = [Expression.wrap(summand) for summand in summands]
        self.summands = sum(
            (s.summands if isinstance(s, Sum) else [s] for s in summands), []
        )

    def __repr__(self):
        args = ", ".join(repr(summand) for summand in self.summands)
        return f"{self.__class__.__name__}({args})"

    @property
    def dependencies(self) -> Iterable["Expression"]:
        for summand in self.summands:
            yield from summand.dependencies

    def evaluate(self, context: Mapping["Node", float]) -> float:
        return float(sum(summand.evaluate(context) for summand in self.summands))


class NegativeOf(NonNode):
    """Negative value of the given expression."""

    def __init__(self, expr: ExpressionLike):
        self.expr = Expression.wrap(expr)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.expr})"

    @property
    def dependencies(self) -> Iterable["Expression"]:
        yield from self.expr.dependencies

    def evaluate(self, context: Mapping["Node", float]) -> float:
        return -self.expr.evaluate(context)


class Product(NonNode):
    """Product of multiple expressions."""

    def __init__(self, *factors):
        factors = [Expression.wrap(factor) for factor in factors]
        self.factors = sum(
            (s.factors if isinstance(s, Product) else [s] for s in factors), []
        )

    def __repr__(self):
        args = ", ".join(repr(factor) for factor in self.factors)
        return f"{self.__class__.__name__}({args})"

    @property
    def dependencies(self) -> Iterable["Expression"]:
        for factor in self.factors:
            yield from factor.dependencies

    def evaluate(self, context: Mapping["Node", float]) -> float:
        return float(
            reduce(
                operator.mul,
                (factor.evaluate(context) for factor in self.factors),
                1,
            )
        )


class Model:
    """A Model is a collection of Stocks and Flows with functionality for creating nodes
    as well as solving the resulting system of ordinary differential equations.
    """

    def __init__(self):
        self.stocks = []
        self.flows = []

    def stock(self, label: str):
        """Create a new Stock and add it to this model.

        >>> m = Model()
        >>> m.stock("test")
        Stock('test')
        >>> m.stocks
        [Stock('test')]
        """
        stock = Stock(label)
        self.stocks.append(stock)
        return stock

    def flow(self, label: str, source: Node, sink: Node, value: ExpressionLike):
        """Create a new Flow and add it to this model.

        >>> m = Model()
        >>> m.flow("flow", Stock("one"), Stock("two"), Constant(1) + 2)
        Flow('flow', Stock('one'), Stock('two'), Sum(Constant(1), Constant(2)))
        >>> m.flows
        [Flow('flow', Stock('one'), Stock('two'), Sum(Constant(1), Constant(2)))]
        """
        flow = Flow(label, source, sink, value)
        self.flows.append(flow)
        return flow

    @property
    def evaluation_order(self) -> Iterable[Node]:
        """Determine an order of evaluations implied by node dependency structure.

        >>> m = Model()
        >>> f1 = m.flow(None, None, None, Constant(1))
        >>> f2 = m.flow(None, None, None, f1 + 2)
        >>> f3 = m.flow(None, None, None, f1 + f2)
        >>> list(m.evaluation_order) == [f1, f2, f3]
        True
        >>> m = Model()
        >>> f1 = m.flow(None, None, None, Constant(1))
        >>> list(m.evaluation_order) == [f1]
        True
        """
        deps = {node: list(node.dependencies_resolving_self) for node in self.flows}
        yield from topological_sort(deps)

    @property
    def ode_func(self) -> Callable:
        """Retrieve function for solving system of ordinary differential equations.

        >>> m = Model()
        >>> s1, s2 = m.stock("s1"), m.stock("s2")
        >>> f1 = m.flow("f1", s1, s2, 1)
        >>> f2 = m.flow("f2", s2, None, 0.5 * f1 - 0.5)
        >>> list(m.evaluation_order) == [f1, f2]
        True
        >>> f = m.ode_func
        >>> f([2, 3], 0)
        [-1, 1.0]
        """
        eval_order = list(self.evaluation_order)
        stock_idx = {stock: i for i, stock in enumerate(self.stocks)}

        def func(y, t):
            assert len(y) == len(self.stocks)
            context = {stock: val for stock, val in zip(self.stocks, y)}
            dy_dt = type(y)([0 for _ in y])
            for node in eval_order:
                val = node.evaluate(context)
                if isinstance(node, Flow):
                    if node.source:
                        dy_dt[stock_idx[node.source]] -= val
                    if node.sink:
                        dy_dt[stock_idx[node.sink]] += val
                context[node] = val
            return dy_dt

        return func


if __name__ == "__main__":
    import doctest

    doctest.testmod()
