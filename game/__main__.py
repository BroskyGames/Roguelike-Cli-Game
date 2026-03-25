# import sys,os
# import curses
#
# def cursor_movement(k: int, cx: int, cy: int, w: int,  h: int) -> tuple[int, int]:
#     if k == curses.KEY_DOWN:
#         cy = min(h-1, cy+1)
#     elif k == curses.KEY_UP:
#         cy = max(0, cy-1)
#     elif k == curses.KEY_RIGHT:
#         cx = min(w-1, cx+1)
#     elif k == curses.KEY_LEFT:
#         cx = max(0, cx-1)
#
#     return cx, cy
#
# def center_x_str(string: str, width: int) -> int:
#     return (width // 2) - (len(string) // 2)
#
# def draw_menu(stdscr):
#     k = 0
#     cursor_x = 0
#     cursor_y = 0
#
#     # Reset Canvas
#     stdscr.clear()
#     stdscr.refresh()
#
#     # Colors
#     curses.start_color()
#     curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
#     curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
#     curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
#
#     # Loop where k is the last character pressed
#     while k != ord('q'):
#         stdscr.clear()
#         height, width = stdscr.getmaxyx()
#
#         cursor_x, cursor_y = cursor_movement(k, cursor_x, cursor_y, width, height)
#
#         # Strings
#         title = "Curses example"[:width-1]
#         subtitle = "Written by Clay McLeod"[:width-1]
#         keystr = "Last key pressed: {}".format(k)[:width-1]
#         statusbarstr = f"Press 'q' to exit | STATUS BAR | Pos: {cursor_x}, {cursor_y}"[:width-1]
#         if k == 0:
#             keystr = "No key press detected..."[:width-1]
#         start_y = (height // 2) - 3
#
#         # Rendering some text
#         whstr = f"Width: {width}, Height: {height}"
#         stdscr.addstr(0, 0, whstr, curses.color_pair(1))
#
#         # Render status bar
#         stdscr.attron(curses.color_pair(3))
#         stdscr.addstr(height-1, 0, statusbarstr)
#         stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
#         stdscr.attroff(curses.color_pair(3))
#
#         stdscr.addstr(start_y, center_x_str(title, width), title, curses.color_pair(2)|curses.A_BOLD)
#         stdscr.addstr(start_y + 1, center_x_str(subtitle, width), subtitle)
#         stdscr.addstr(start_y + 3, (width // 2) - 2, '-' * 4)
#         stdscr.addstr(start_y + 5, center_x_str(keystr, width), keystr)
#         stdscr.move(cursor_y, cursor_x)
#
#         # Refresh the screen
#         stdscr.refresh()
#
#         # Wait for next input
#         k = stdscr.getch()
#
# def main():
#     curses.wrapper(draw_menu)
#
import random
from pprint import pprint

from game.logic.graph import generate_graph, RoomNode, find_longest_path, RoomTags
from game.utils import init_rng

# For each .connection print(" "*depth + "Node")

def print_nodes(node: RoomNode, visited=None, prefix="", is_last=True):
    if visited is None:
        visited = set()
    if node.id in visited:
        return
    visited.add(node.id)

    connector = "└─ " if is_last else "├─ "
    match node.tag:
        case RoomTags.NORMAL:
            icon = 'N'
        case RoomTags.SPAWN:
            icon = 'S'
        case RoomTags.MAIN:
            icon = 'M'
        case RoomTags.BOSS:
            icon = 'B'
        case RoomTags.CHEST:
            icon = 'C'

    print(prefix + connector + f"{icon}{node.id}")

    new_prefix = prefix + ("   " if is_last else "│  ")

    children = [n for n in node.connections if n.id not in visited]

    for i, child in enumerate(children):
        is_last_child = i == len(children) - 1
        print_nodes(child, visited, new_prefix, is_last_child)

if __name__ == "__main__":
    # main()
    init_rng(2332 ** random.randint(5, 100))
    spawn = generate_graph(25, {1: 1.3, 2: 1.1, 3: 1})
    main_path = find_longest_path(spawn)
    print_nodes(spawn)