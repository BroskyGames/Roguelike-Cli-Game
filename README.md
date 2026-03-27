# Pre-download
pip install windows-curses
py: 3.13.1

# Ideas
While rendering double the width to keep the ascpect ratio 1:1.
Most likly by inserting spaces between characters.

# Cycle
- input
- update:
  - player_action
  - enemy_update
  - enviroment_update
- render:
  - map
  - entites
  - ui
- tick_counter

# Game
```
class Game:
  player: Player
  map: Map
  eniemies: List[Eniemies]
  traps: List[Trap] // maybe
```

# Level
```python
class Map:
  seed: int
  
  rooms: list[Room]
  corridors: list[Corridor]

  grid: dict[Pos, str]

class Room:
  pos: Pos
  template: (str/ enum/ class_instance)
  rotate: int
  min_doors: int

  shape: (asci)
  doors: list[Pos]

class Corridor:
  start: Pos
  end: Pos
  path: list[Pos]
```

# UI
```python
class UI:
  def map_render(self, x, y, w, h):
```
