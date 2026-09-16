#!/usr/bin/env python3
from . import todo as t

from rofl.router import RofiRouter
from rofl.response import RofiResponse, RofiResponseOptions, RofiRow
from rofl.request import RofiRequest, RofiRequestType

ROUTER = RofiRouter.from_environment()


def create_todo_list() -> RofiResponse:
    todos: list[t.Todo] = t.parse_todos()

    rows: list[RofiRow] = [
        RofiRow(
            todo.time.strftime(t.DATE_FORMAT),
            display=todo.stringify_pretty(),
            icon=[],
            meta=todo.todo,
            info=repr(todo),
        )
        for todo in todos
    ]

    rofi = RofiResponse(
        rows=rows,
        options=RofiResponseOptions(
            "Todos", no_custom=False, use_hot_keys=True
        )
    )

    return rofi


@ROUTER.bind_fb()
def fallback(request: RofiRequest) -> None:
    _ = request
    list_str = create_todo_list().render()
    ROUTER.write(list_str)
    return


@ROUTER.bind(RofiRequestType.SELECTED)
def complete(request: RofiRequest) -> None:
    if request.info is None:
        return
    todo = t.Todo.from_repr(request.info)
    _ = t.complete_todo(todo)


@ROUTER.bind(RofiRequestType.CUSTOM_INPUT)
def add(request: RofiRequest) -> None:
    if request.accepted_text is None:
        import sys
        print(request, file=sys.stderr)
        return

    todo_text = request.accepted_text.strip()
    t.add_todo(todo_text)


def main():
    ROUTER.run()

if __name__ == "__main__":
    main()
