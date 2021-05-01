from typing import Mapping, Iterable, TypeVar, Dict, Set
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


class Expression(ABC):
    """Abstract base class for all types of expressions including nodes."""

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
        pass


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


if __name__ == "__main__":
    import doctest

    doctest.testmod()