py: 3.13.1

# Game overview
A roguelike dungeon crawler turn-based cli game being build in python with curses.

## Entity Actions
Player and enemies share the same system of actions.\
AI/ Input decides on a queue of actions that are le than `action_points` of the entity. \
Acceptable actions are for example: `Move(Direction)`, `Attack(Entity)`, `Use(Item)` \
Actions share `action_cost` and `perform()`.

## UI
Made using curses and abstracted to widgets like: MapScreen, PlayerInfo, Logs, LevelInfo.

## Generation
Map generation starting with creating a graph of connections between rooms.\
Assigning tags to nodes:
- Spawn: first node in graph
- Boss: deepest node
- Main: connect boss to spawn
- Genetic-labs: random & childrenless
- Traps: random & remaining untagged

Creating actual rooms with data and corridors based on tags.

## Progression
### Stages
Each main room has a chance to separate stages of the dungeon. Each stage is\
progressively harder (more enemies with higher stats), equality of stages is not \
guaranteed (new stage may happen right after another and branches may not even exist).
### Modifiers
Killing enemies gives xp allowing to grow in stats. Genetic-labs allow to gain traits \
that apply both buffs & debuffs through modifying (visibility, costs of actions,\
affinities with types of damage). 
### Win condition
At the end of level (killing the boss), starts another level clearing xp, but preserving the traits. \
Killing the third boss is the win condition.

# Ideas
While rendering double the width to keep the aspect ratio 1:1.
Most likely by inserting spaces between characters.

# Cycle
- input
- update:
  - player_action
  - enemy_update
  - environment_update
- render:
  - map
  - entities
  - ui
- tick_counter

# File Structure:
game/
  core/
    state.py # only rng handling for now 
    types.py
  map/
    graph.py
    layout.py
    tile_map.py
    level.py
    room_tags.py
  interface/
    debug.py
    rederer.py # empty
    widget.py # scratch
  utils/
    reducers.py