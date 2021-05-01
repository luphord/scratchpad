from typing import Mapping, Iterable, TypeVar, Dict, Set, Union
from collections import defaultdict
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


class Node(Expression):
    """Abstract base class for all nodes."""

    @property
    def dependencies(self) -> Iterable["Expression"]:
        yield self


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


if __name__ == "__main__":
    import doctest

    doctest.testmod()
