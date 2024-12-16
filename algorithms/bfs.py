import dataclasses
from copy import deepcopy
from typing import Set, List, Callable, Any, NoReturn, Self, Iterable, Tuple, Optional
from algorithms.grid import Position, Grid


@dataclasses.dataclass
class BFSState:
    p: Position
    data: Any = None

    def clone(self) -> Self:
        return deepcopy(self)

    def clone_keep_data(self) -> Self:
        return BFSState(self.p.clone(), self.data)


def bfs(
        grid: Grid,
        start: BFSState,
        visit_fn: Callable[[Grid, BFSState], NoReturn],
        next_fn: Callable[[Grid, BFSState], Iterable[BFSState]],
        prevent_visiting_gt_once: bool = False,
):
    visited: Set[Position] = set()
    # [(next, current)]
    to_visit: List[Tuple[BFSState, Optional[BFSState]]] = [(start, None)]
    to_visit_set: Set[Position] = {start.p}
    for v in to_visit:
        to_visit_set.remove(v.p)
        if v.p in visited:
            continue
        visited.add(v.p)
        visit_fn(grid, v)
        all_next = next_fn(grid, v)
        for s in all_next:
            if s.p not in visited and s.p not in to_visit_set:
                to_visit_set.add(s.p)
                to_visit.append(s)
