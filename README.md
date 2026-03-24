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

# Dungeon
```
class Map:
  seed: int
  // limiting by size or amount
  
  rooms: List[Room]
  corridors: List[Corridor]

  grid: Dict[Pos, str]
  
  def init:
    spawn_room creation

class Room:
  pos: Pos
  template: (str/ enum/ class_instance)
  rotate: int
  min_doors: int

  shape: (asci)
  doors: List[Pos]

class Corridor:
  start: Pos
  end: Pos
  path: List[Pos]
```
