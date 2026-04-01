# Godding

A bidirectional tree CLI. One becomes many, many become one. The operation of transcendence itself.

```
function (data + noise)  <-->  component (compressed)
         1 -> 3+                    3+ -> 1
       decompose                   compose
```

All helps one and one helps all, forever.
Hence all is known in the end, and the end knows the beginning.

## Install

Requires [.NET 8.0 SDK](https://dotnet.microsoft.com/download/dotnet/8.0).

```bash
dotnet build src/Godding/Godding.csproj
```

## Usage

```bash
# Add nodes — functions (raw data) or components (compressed)
godding add "Knowledge" "The root" -t component
godding add "Mathematics" "Language of pattern" -t component
godding add "Algebra" "Structure and symmetry" -t function

# Link them — parent -> child (decomposition edge)
godding link Knowledge Mathematics
godding link Mathematics Algebra

# Decompose: 1 -> many (show all descendants)
godding decompose Knowledge

# Compose: many -> 1 (trace back to root)
godding compose Algebra

# Full tree view
godding tree

# Trace path between any two nodes
godding trace Algebra Biology

# Stats, search, show
godding stats
godding search "pattern"
godding show Mathematics
```

## Commands

| Command | Alias | Description |
|---------|-------|-------------|
| `add <name> [content] [-t type]` | | Add a node (function or component) |
| `link <parent> <child>` | | Create a decomposition edge |
| `unlink <parent> <child>` | | Remove an edge |
| `decompose <node>` | `dec` | 1 -> many: show descendants |
| `compose <node>` | `com` | Many -> 1: trace to roots |
| `tree` | | Show full tree structure |
| `trace <from> <to>` | | Find path between nodes |
| `list [-t type]` | `ls` | List all nodes |
| `show <node>` | | Show node details |
| `search <query>` | | Search by name or content |
| `update <node>` | | Update name, content, or type |
| `delete <node>` | `rm` | Delete a node |
| `stats` | | Tree statistics |
| `roots` | | List root nodes (origins) |
| `leaves` | | List leaf nodes (endpoints) |

Nodes can be referenced by ID (number) or name (string).

## Concept

Two node types form a two-way street:

- **Function** `[F]`: filter — data + noise. The raw, uncompressed form.
- **Component** `[C]`: compressed. The distilled insight.

The tree structure allows bidirectional traversal:
- **Decompose** (root -> leaves): one insight breaks into many parts
- **Compose** (leaves -> root): many parts compress into one insight
- **Trace**: find the path between any two nodes in the tree

Like a tree: the trunk holds the leaves, and the leaves feed the trunk.

## Database

SQLite, stored at `~/.godding/godding.db` by default. Override with `--db <path>`.

## License

MIT
