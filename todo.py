from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import override

TODO_PATH = Path.home() / ".config" / "todos" / "todo"
COMPLETE_PATH = Path.home() / ".config" / "todos" / "complete"
# KEEP_DONE_COUNT = 1000
DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'


class InvalidTodoFile(Exception):
    pass


@dataclass(frozen=True)
class Todo:
    index: int
    time: datetime
    todo: str

    @staticmethod
    def create(text: str) -> "Todo":
        return Todo(-1, datetime.now(), text)

    @staticmethod
    def create_from_line(index: int, parts: list[str]) -> "Todo":
        if len(parts) != 2:
            raise InvalidTodoFile(
                f"Each line of '{TODO_PATH}', must contain exactly 1 todo, " 
                f"in the format: time | todo text"
            )

        date = datetime.strptime(parts[0], DATE_FORMAT)
        return Todo(index, date, parts[1].strip())

    @staticmethod
    def from_repr(repr: str) -> "Todo":
        parts = repr.split("|")
        if len(parts) != 3:
            raise InvalidTodoFile(
                "from_repr is intented for __repr__ -> Todo conversion only"
            )
        return Todo(int(parts[0]), datetime.strptime(parts[1], DATE_FORMAT), parts[2])


    def stringify_pretty(self) -> str:
        return f"{self.time.strftime("%d-%m-%y %H:%M")} | {self.todo}"

    def to_line(self) -> str:
        return f"{self}\n"

    @override
    def __str__(self) -> str:
        return f"{self.time.strftime(DATE_FORMAT)}|{self.todo}"

    @override
    def __repr__(self) -> str:
        return f"{self.index}|{self.time.strftime(DATE_FORMAT)}|{self.todo}"


def ensure_files_configured():
    try:
        with open(TODO_PATH) as _:
            pass
    except (OSError, IOError):
        raise Exception(
            f"Failed to open Todo File, at '{TODO_PATH}'.\n\t"
            f"Please ensure you have created an empty file at this location."
        )

    try:
        with open(COMPLETE_PATH) as _:
            pass
    except (OSError, IOError):
        raise Exception(
            f"Failed to open Complete File, at '{COMPLETE_PATH}'.\n\t"
            f"Please ensure you have created an empty file at this location."
        )
    return


def add_todo(text: str):
    todo = Todo.create(text)
    # attempt - error if not
    _ = open(TODO_PATH, 'a').write(todo.to_line())


def parse_todos() -> list[Todo]:
    raw_lines = open(TODO_PATH, 'r').readlines(-1)
    lines: list[Todo] = []

    for i, line in enumerate(raw_lines):
        parts: list[str] = line.split("|")
        todo = Todo.create_from_line(i, parts)

        lines.append(todo)

    return lines


def complete_todo(todo: Todo) -> bool:
    todos = parse_todos()
    f = open(TODO_PATH, 'w')

    found_at = -1
    for i, t in enumerate(todos):
        if t.time == todo.time and t.todo == t.todo:
            found_at = i
            continue
        _ = f.write(t.to_line())

    f.close()

    if found_at == -1:
        return False

    _ = open(COMPLETE_PATH, "a").write(
        f"{todo.time.strftime(DATE_FORMAT)}>"
        f"{datetime.now().strftime(DATE_FORMAT)}|{todo.todo}\n"
    )

    return True


if __name__ == "__main__":
    from time import sleep

    add_todo("new_todo")
    sleep(1)
    add_todo("twodo")
    sleep(1)
    add_todo("wow")

    todos = parse_todos()
    print(todos)
