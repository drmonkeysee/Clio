# Clio — Design Document
## Trade Network Emergence Simulator

---

## Overview

Clio is a self-running, tile-based civilization simulator focused on the emergent behavior of trade networks. Starting from a procedurally generated world, independent settlements arise, discover what they have and lack, and begin exchanging goods. From that economic foundation, culture, conflict, and complexity grow organically.

The simulation runs in real time with no player input required. The primary appeal is watching unexpected patterns emerge from simple rules.

---

## 1. Map Generation

### 1.1 Tile Shape

**Square grid** with ASCII character rendering, consistent with the Dwarf Fortress / roguelike aesthetic. Each tile is represented by a single character and a foreground/background color.

Tiles are addressed by `(col, row)` integer coordinates. The grid has 8 neighbors per tile: 4 cardinal (N, S, E, W) and 4 diagonal (NW, NE, SW, SE).

**Movement costs** use the standard roguelike integer approximation of the 1 : √2 cardinal-to-diagonal ratio:

| Direction | Base cost |
|-----------|-----------|
| Cardinal (N/S/E/W) | 2 |
| Diagonal (NW/NE/SW/SE) | 3 |

This keeps all costs as integers while preserving roughly correct relative distances (true diagonal is 2√2 ≈ 2.83, so 3 is a close approximation). Terrain modifiers are added on top of these base costs.

### 1.2 Map Size

| Size | Dimensions | Use case |
|------|-----------|----------|
| Small | 64 × 64 | Development / fast iteration |
| Medium | 128 × 128 | Standard simulation |
| Large | 256 × 256 | Long-run experiments |

Start with small maps during development. Scale up once the simulation is stable.

### 1.3 Terrain Generation

Terrain is generated in layers, each building on the previous.

**Step 1 — Elevation (Simplex noise)**
- Two octaves of simplex noise produce a heightmap
- Thresholds determine terrain class: deep water, shallow water, lowland, highland, mountain
- Islands and continents emerge naturally from noise parameters

**Step 2 — Temperature**
- Base temperature derived from latitude (equator = hot, poles = cold)
- Elevation modifier (highlands are cooler)
- Temperature determines biome eligibility

**Step 3 — Moisture**
- Second noise pass, loosely correlated with distance from coast
- Combined with temperature to assign biome: desert, grassland, forest, tundra, etc.

**Step 4 — Rivers**
- Trace downhill paths from highland tiles to coast or inland sea
- Rivers occupy tile edges, not tile centers
- River tiles get a movement cost bonus (travel along river is fast) and fertility bonus

**Step 5 — Resource placement**
- Resources are seeded based on terrain type (see Section 3)
- Clustering algorithm ensures resources appear in patches, not uniform scatter

### 1.4 Terrain Types

Movement costs are **terrain modifier only** — add to the base cardinal (2) or diagonal (3) cost to get the total cost for that move.

| Terrain | Movement Modifier | Cardinal Total | Diagonal Total | Notes |
|---------|------------------|---------------|----------------|-------|
| Deep water | Impassable (early) | — | — | Navigable later |
| Shallow water | +2 | 4 | 5 | Coastal trade |
| Lowland | +0 | 2 | 3 | Default |
| Highland | +2 | 4 | 5 | Slower movement |
| Mountain | Impassable | — | — | Blocks routes; passes possible later |
| Forest | +2 | 4 | 5 | Timber resource |
| Desert | +2 | 4 | 5 | Sparse resources |
| Tundra | +2 | 4 | 5 | Sparse resources |

River-adjacent tiles reduce the movement modifier by 2 (minimum modifier 0, so lowland river travel costs the base 2/3 with no added penalty).

---

## 2. Tile Content

Each tile is a data structure tracking the following:

### 2.1 Static Properties (set at generation, rarely change)
- `terrain_type` — from the table above
- `elevation` — raw float, 0.0–1.0
- `temperature` — float
- `moisture` — float
- `biome` — derived from temperature + moisture
- `river_sides` — bitmask of which of the 4 cardinal sides carry a river (rivers run between tiles, not through them)
- `resources[]` — list of resource types present (see Section 3)

### 2.2 Dynamic Properties (change during simulation)
- `settlement_id` — which settlement claims this tile (None if unclaimed)
- `population_density` — affects resource extraction rate
- `improvement` — farm, mine, road, port, etc. (one per tile, added over time)
- `trade_traffic` — rolling count of trade units passing through this turn
- `fertility` — current agricultural yield (degrades with overuse)
- `control` — which polity exerts political control (may differ from settlement_id)

### 2.3 Visual Representation
- Each tile is a single ASCII character with a foreground and background color
- Character encodes the primary feature: terrain, settlement, or improvement (see Section 7)
- River presence shown by character choice on river tiles (e.g. `~` for water, `=` for a ford)
- Trade route heat: background color intensity on path tiles scales with `trade_traffic`
- Settlement tiles use a distinct character that scales with population tier

---

## 3. Resources

Resources are the foundation of trade. Every settlement needs things it doesn't have locally.

### 3.1 Resource Categories

| Category | Examples | Primary Use |
|----------|---------|-------------|
| Food | Grain, Fish, Game, Fruit | Sustains population |
| Raw materials | Timber, Stone, Clay | Construction |
| Metals | Copper, Iron, Gold, Silver | Tools, weapons, currency |
| Luxury goods | Spices, Dyes, Gems, Furs | Culture, status, trade value |
| Energy | Peat, Coal (later eras) | Production |

### 3.2 Resource Distribution Rules
- Food resources are moderately common but not universal — every region can sustain *some* population, but not all foods grow everywhere
- Metals are rare and clustered — the location of an iron deposit shapes regional history
- Luxury goods are intentionally scarce and geographically specific — spices only in tropical biomes, gems only in certain mountain types, etc.
- No tile has everything — scarcity is a design requirement, not an accident

### 3.3 Resource Extraction
- Each resource tile has a `yield` value, modified by improvement and population
- Extraction is gradual — a settlement doesn't instantly consume a resource node
- Depletion is possible for non-renewable resources (metals, game); renewable resources (timber, fish) recover if extraction stops

---

## 4. Settlements

### 4.1 Founding
- Initial settlements are seeded at generation time at locations that score well on a habitability function: freshwater access, arable land, defensible position, coastal or river access
- Minimum distance enforced between starting settlements to prevent crowding
- New settlements can also be founded during simulation by population overflow or deliberate migration events

### 4.2 Settlement Properties
- `name` — procedurally generated
- `population` — integer, drives everything else
- `tiles[]` — list of claimed tiles (expands over time)
- `resources_available{}` — what it can produce locally
- `resources_needed{}` — what it lacks and will seek through trade
- `trade_partners[]` — active trade relationships
- `wealth` — accumulated surplus value
- `culture_id` — which cultural group it belongs to
- `era` — current technological/social era

### 4.3 Population Dynamics
- Population grows when food supply exceeds consumption
- Growth is logistic (slows as it approaches carrying capacity of claimed tiles)
- Population decline from starvation, plague, or conflict
- Population pressure drives expansion: new tile claims, new settlements, or migration

### 4.4 Needs and Surpluses
Each settlement computes a simple supply/demand balance each turn:
- **Surplus**: resources extracted beyond local consumption → available for export
- **Deficit**: resources consumed but not locally available → import demand
- The gap between surplus and deficit is the economic engine of the simulation

---

## 5. Trade

### 5.1 Route Formation
Trade routes are not drawn by a planner — they emerge from agent behavior:

1. A settlement with a deficit broadcasts a "seeking" signal for that resource
2. Nearby settlements with a matching surplus respond
3. A route is established along the lowest-cost path (Dijkstra over square grid movement costs, cardinal and diagonal)
4. Routes are represented as a sequence of tiles; each tile's `trade_traffic` increments each turn the route is active

### 5.2 Route Cost
Movement cost per tile (from Section 1.4) plus:
- Political cost: crossing a hostile or unrelated polity's territory adds risk cost
- Infrastructure bonus: roads reduce cost, ports enable sea routes

### 5.3 Trade Mechanics
- Each turn, a notional "trade unit" moves along established routes
- Arriving trade units transfer resources between settlements
- Settlements pay in surplus goods or accumulated wealth
- Exchange rates are simple supply/demand: a resource rare in the buyer's region commands higher value

### 5.4 Emergent Geography
The most important emergent outcome of trade routing is **chokepoint amplification**:
- Tiles at river crossings, mountain passes, and coastal harbors become mandatory waypoints for many routes
- High traffic → settlements there grow faster → they develop improvements → routes become even cheaper through them → more traffic
- This positive feedback loop produces realistic hub cities without any explicit rule that says "cities form at crossings"

### 5.5 Route Instability
Routes are not permanent. They are re-evaluated periodically and can:
- Shift if a new road shortens an alternate path
- Break if political hostility makes a path too costly
- Collapse if the source resource is exhausted
- Redirect around a settlement that has been destroyed or abandoned

Route instability is a feature — watching trade networks reorganize after a disruption is a primary source of emergent narrative.

---

## 6. Progression and Eras

The simulation advances through broad eras that unlock new mechanics:

| Era | Key Mechanics Unlocked |
|-----|----------------------|
| Hunter-Gatherer | Migration, basic resource gathering, no permanent settlements |
| Pastoral / Early Agriculture | Permanent settlements, farming improvements, animal husbandry |
| Early Civilization | Organized trade, specialization, basic governance |
| Classical | Long-distance trade, roads, ports, coinage, early conflict |
| Medieval | *(future scope)* |
| Early Modern | *(future scope)* |

Era advancement is not global — different settlements can be in different eras simultaneously, which creates asymmetric interactions (a classical merchant encountering a pastoral village).

---

## 7. Visual Design

### 7.1 Aesthetic Reference
Dwarf Fortress and classic roguelikes: ASCII characters with colored foreground/background. Information-dense and readable at a glance. Every tile is one character; color carries the secondary information layer.

### 7.2 ASCII Character Palette (provisional)

| Feature | Character | Notes |
|---------|-----------|-------|
| Lowland / grassland | `.` | Default open terrain |
| Forest | `♣` or `T` | Tree character |
| Desert | `·` | Sparse dot |
| Tundra | `_` | Flat, cold |
| Highland | `n` | Low hills suggestion |
| Mountain | `^` | Classic roguelike mountain |
| Deep water | `≈` | Wave character |
| Shallow water / coast | `~` | Calmer water |
| River | `=` (E/W) / `║` (N/S) | Follows cardinal direction |
| Small settlement | `∙` | Hamlet |
| Town | `○` | Growing settlement |
| City | `●` | Major hub |
| Road | `·` (brightened) | Subtle infrastructure |
| Mine | `±` | Extraction site |
| Farm | `‰` | Agricultural improvement |

Characters are suggestions — the palette will evolve during development.

We will be using IBM's Code Page 437 (https://en.wikipedia.org/wiki/Code_page_437) as the ASCII character set, although the actual codepoints will use their UTF-8 equivalents, not the actual code page.

### 7.3 Color Usage
- **Background color**: encodes terrain biome (dark green for forest, tan for desert, etc.)
- **Foreground color**: encodes the feature character (blue river, white mountain, yellow city)
- **Trade route heat**: tiles on active routes get a slightly brightened background; heavily trafficked routes pulse or use a distinct color
- **Zoom levels**: at world scale, settlement characters dominate; at local scale, terrain and resource detail is visible

### 7.4 Camera
- Pan and zoom over the tile map
- Zoom levels: world view (settlements and major geography only) → regional view (settlement names visible beside their tile) → local view (tile terrain and resource details)

### 7.5 Time Controls
- Pause / Play / Fast-forward
- Turn counter and in-world date display
- Event log panel: notable events scroll as they occur (new settlement founded, trade route established, resource exhausted, etc.)

---

## 8. Technical Notes

### 8.1 Stack
- **Language**: Python
- **Renderer**: pygame-ce
- **Package manager**: uv (app mode)
- **Noise**: `noise` library (Simplex/Perlin)
- **Grid math**: standard 2D array with 8-neighbor adjacency; Chebyshev distance for range checks, weighted Dijkstra for pathfinding
- **Tile Map**: use numpy for efficiency and speed?

### 8.1.1 Should we use numpy?

Yes, with some caveats worth thinking through before you commit to it.

**Where numpy is a clear win:**

The tile map is the obvious case. A set of 2D arrays — one per property — is exactly what numpy is designed for. Instead of a dict of tile objects, you'd have:

```python
elevation   = np.zeros((rows, cols), dtype=np.float32)
temperature = np.zeros((rows, cols), dtype=np.float32)
terrain     = np.zeros((rows, cols), dtype=np.uint8)
trade_traffic = np.zeros((rows, cols), dtype=np.float32)
```

This pays off immediately in map generation (noise → array operations), in rendering (slice the viewport, pass to pygame as a surface), and in any spatial query like "find all forest tiles within range." Those operations vectorize naturally and are much faster than iterating a dict of objects.

**Where numpy is a poor fit:**

Entities with heterogeneous, variable state — settlements, trade routes, cultural groups — are a bad match. A settlement has a name, a list of trade partners, a dict of resource balances, an era, and so on. Numpy wants homogeneous numeric arrays of fixed shape. You'd end up fighting it constantly to model things that are naturally objects or dicts.

**The practical split:**

Use numpy for the **world layer** (anything that maps 1:1 to a tile), and plain Python objects/dicts for **entities** (anything that has identity, relationships, and variable structure). The two layers talk to each other: a settlement object holds a `(col, row)` position and reads/writes into the numpy arrays when it needs to know terrain or update trade traffic.

This is actually the standard pattern in Python game/sim development — numpy for the field, objects for the agents.

**One additional consideration:**

Pathfinding (Dijkstra over the cost array) is a case where you might want to look at `scipy.sparse.csgraph` or just use a pure Python heap-based implementation. Numpy alone doesn't give you graph algorithms, and the overhead of converting the array to a graph for each route calculation may negate the benefit. Pure Python Dijkstra with a numpy cost array lookup per step is often the right middle ground.

So the short answer: yes for the tile world, no for simulation entities.

### 8.2 Data Model
- Map is a flat dict keyed by `(col, row)` integer coordinates (or a 2D array)
- Settlements are objects stored in a registry, referenced by ID from tile data
- Trade routes are objects with a list of tile coordinates and metadata
- Event log is an append-only list of structured event dicts

### 8.3 Simulation Loop
```
each tick:
  1. Resource extraction for all settlements
  2. Population update (growth / decline)
  3. Needs/surplus recalculation
  4. Trade route evaluation (re-route if needed)
  5. Trade execution (move goods along active routes)
  6. Wealth update
  7. Event detection (thresholds crossed → log event)
  8. Render
```

### 8.4 Performance Considerations
- Route pathfinding is the most expensive operation — cache routes and only recompute on change events
- Render only visible tiles (viewport culling)
- Separate simulation tick rate from render frame rate

---

## 9. Out of Scope (for now)

The following are intentionally deferred to keep the initial build tractable:

- Military conflict
- Political systems and governance
- Religion and culture spread
- Disease
- Sea navigation
- Named historical figures
- Diplomacy

These all hang naturally off the trade foundation and can be added in later layers once the core is stable and interesting on its own.

---

## 10. Open Questions

- Should settlements be able to split or merge, or are they fixed entities once founded?
- How granular should resource types be? (10 types vs 50 types changes the emergent variety significantly)
- What is the right tick rate for "watchable" emergence — seconds per turn? Minutes?
- Should the map wrap (toroidal) or have hard edges?
- How should era advancement be triggered — automatic by population/wealth threshold, or event-driven?
