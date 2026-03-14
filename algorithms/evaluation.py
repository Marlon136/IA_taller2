from __future__ import annotations

from typing import TYPE_CHECKING
from algorithms.utils import bfs_distance, dijkstra

visited_positions = set()
if TYPE_CHECKING:
    from world.game_state import GameState


def evaluation_function(state: GameState) -> float:
    """
    Evaluation function for non-terminal states of the drone vs. hunters game.

    A good evaluation function can consider multiple factors, such as:
      (a) BFS distance from drone to nearest delivery point (closer is better).
          Uses actual path distance so walls and terrain are respected.
      (b) BFS distance from each hunter to the drone, traversing only normal
          terrain ('.' / ' ').  Hunters blocked by mountains, fog, or storms
          are treated as unreachable (distance = inf) and pose no threat.
      (c) BFS distance to a "safe" position (i.e., a position that is not in the path of any hunter).
      (d) Number of pending deliveries (fewer is better).
      (e) Current score (higher is better).
      (f) Delivery urgency: reward the drone for being close to a delivery it can
          reach strictly before any hunter, so it commits to nearby pickups
          rather than oscillating in place out of excessive hunter fear.
      (g) Adding a revisit penalty can help prevent the drone from getting stuck in cycles.

    Returns a value in [-1000, +1000].

    Tips:
    - Use state.get_drone_position() to get the drone's current (x, y) position.
    - Use state.get_hunter_positions() to get the list of hunter (x, y) positions.
    - Use state.get_pending_deliveries() to get the set of pending delivery (x, y) positions.
    - Use state.get_score() to get the current game score.
    - Use state.get_layout() to get the current layout.
    - Use state.is_win() and state.is_lose() to check terminal states.
    - Use bfs_distance(layout, start, goal, hunter_restricted) from algorithms.utils
      for cached BFS distances. hunter_restricted=True for hunter-only terrain.
    - Use dijkstra(layout, start, goal) from algorithms.utils for cached
      terrain-weighted shortest paths, returning (cost, path).
    - Consider edge cases: no pending deliveries, no hunters nearby.
    - A good evaluation function balances delivery progress with hunter avoidance.
    """
    
    if state.is_win():
        return 1000

    if state.is_lose():
        return -1000

    drone = state.get_drone_position()
    hunters = state.get_hunter_positions()
    deliveries = state.get_pending_deliveries()

    layout = state.get_layout()

    score = state.get_score()

    value = 0.0

  
    # (a) distancia a delivery usando DIJKSTRA (se multiplica por 5 para darle peso)
    
    if deliveries:
        
        d_delivery = min(
            dijkstra(layout, drone, d)[0]
            for d in deliveries
        )

        value -= 5 * d_delivery

    # (b) distancia a cazadores BFS restringido (se multiplica por 3 cada distancia para darle peso)
   

    min_hunter_dist = float("inf")

    for h in hunters:

        d_hunter = bfs_distance(
            layout,
            h,
            drone,
            True
        )

        if d_hunter == 0:
            return -1000

        if d_hunter < min_hunter_dist:
            min_hunter_dist = d_hunter

        if d_hunter != float("inf"):
            value += 3 * d_hunter

 
    # (c) safe position (se multiplica por 4 cada distancia para darle peso)
  

    if min_hunter_dist != float("inf"):
        value += 4 * min_hunter_dist

 
    # (d) deliveries pendientes (se multiplica por 50 el numero de deliveries para darle peso)


    value -= 50 * len(deliveries)

    
    # (e) score actual
 

    value += score

    
    # (f) urgency usando DIJKSTRA
    

    for d in deliveries:

        d_drone = dijkstra(layout, drone, d)[0]

        hunter_dists = [
            bfs_distance(layout, h, d, True)
            for h in hunters
        ]

        if hunter_dists and d_drone < min(hunter_dists):
            value += 20

    # (g) evitar ciclos 
    if drone in visited_positions:
      value -= 5

    visited_positions.add(drone)

    # limitar rango

    value = max(-1000, min(1000, value))

    return value
