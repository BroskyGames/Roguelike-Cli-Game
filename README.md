py: 3.13.1

# Game overview

A roguelike dungeon crawler turn-based cli game being build in python with curses.

## Entity Actions

Player and enemies share the same system of actions.\
AI/ Input decides on a queue of actions that are le than `action_points` of the entity. \
Acceptable actions are for example: `Move(Direction)`, `Attack(Entity)`, `Use(Item)` \
Actions share `action_cost` and `perform()`.

## Turn

process_turn:

- render game state
- player_actions
- ai_actions
- for action
    - resolve_systems
    - render

### Populate Player Actions

UI onInput -> engine process input:

- add_action() {simulate action}
- remove_action()
- commit_turn()

## UI

Made using curses and abstracted to windows like: MapWindow, PlayerWindow, LogsWindow, LevelWindow.

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

# File Structure:

```
game/
  __main__.py
  game_factory.py
  core/
    state.py
    context.py
    engine.py
    scheduler.py
    router.py
    geometry.py
    map_types.py
  domain/
    actions.py
    components/
      data.py
      tags.py
      stats.py
  systems/
    action_queue_processor.py
    ap_procesor.py
    movement_processor.py
    turn_processor.py
  ui/
    ui.py
    debug.py
    rect.py
    layout/
      builder.py
      nodes.py
      splits.py
    views/
      map_view.py
      data_view.py
      action_view.py
    curses/
      basic.py
      manager.py
      input.py
      border.py
      windows/
        map_window.py
        data_window.py
        action_window.py
  map/
    graph.py
    room.py
    corridor.py
    tile_map.py
    level.py
    special_templates.py
  utils/
    reducers.py   
    string.py
```