# ROFL-todo
A very basic [rofi](https://github.com/davatorium/rofi) based Todo manager written in about 30 minutes.


##  Requirements 
- [rofi v2.0.0](https://github.com/davatorium/rofi) - A Linux quick-menu, similar to that of "spotlight"
- [rofl v0.1.0](https://github.com/H8rsbeware/rofl) - My decorator-based wrapper for the input/output encoding rofi uses


## Setup

### Defaults 
1. Create the dir, `~/.config/todos`
2. In the `~/.config/todos` dir, touch `todos` and `complete`


### Alternative
1. Create two, extension-less (or otherwise) files, in a directory of your choosing
2. Edit the repo's `todo.py` `TODO_PATH` and `COMPLETE_PATH`

---

Then: 

1. Clone [rofl](https://github.com/H8rsbeware/rofl) into a different directory
2. Back in the Todos repo, create a new `.venv` with `python -m pip venv .venv`
3. Run `source ./venv/bin/activate`
4. and then `python -m pip install {PATH_TO_ROFL_REPO}`

Finally:

1. Create the following `sh` file, in `~/.local/bin/` -  I call mine `todos`:
  ```sh
  #!/usr/bin/env bash

  PROJECT="$HOME/{PATH_TO_TODO_DIR}"
  exec "$PROJECT/.venv/bin/python" "$PROJECT/manager.py" "$@"
  ```
2. Run `chmod +x ~/.local/bin/todos`
3. Run `rofi -show todos -modes "todos:~/.local/bin/todos"` to test

> Please, replace the `{PATH_TO_TODO_DIR}` in the `sh`, with the actual path to the repository primary directory


## Usage

Within ROFL-todo, you can navigate using the default binds in rofi.

To create a new todo, type your text into the search bar and click enter.

>! Special Characters and line breaks are not allowed, due to rofi's encoding scheme - this is not validated currently

To mark one as complete, you can simply navigate to the todo in the list, and click enter once more.
All completed todos will appear in the `~/.config/todos/complete` directory.


##  Deceleration

No AI generation or assistance was used to create ROFL-todo or ROFL-projector, and only guidance (questions/answers) were used for ROFL itself.

No pull requests will be accepted or reviewed - this is a personal tool, and I will improve it for my needs.

