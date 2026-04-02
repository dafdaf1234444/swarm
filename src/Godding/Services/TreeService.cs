using Godding.Data;
using Godding.Models;

namespace Godding.Services;

public class TreeService
{
    private readonly Database _db;

    public TreeService(Database db)
    {
        _db = db;
    }

    /// <summary>
    /// Decompose: 1 -> many. Show all descendants of a node (the tree below it).
    /// </summary>
    public void PrintDecomposition(long nodeId, int maxDepth = 20)
    {
        var node = _db.GetNode(nodeId);
        if (node == null)
        {
            Console.WriteLine($"Node #{nodeId} not found.");
            return;
        }

        Console.WriteLine($"Decomposition of {node}:");
        Console.WriteLine();
        PrintSubtree(node, "", true, maxDepth, 0, new HashSet<long>());
    }

    /// <summary>
    /// Compose: many -> 1. Trace all paths from a node back to its roots.
    /// </summary>
    public void PrintComposition(long nodeId)
    {
        var node = _db.GetNode(nodeId);
        if (node == null)
        {
            Console.WriteLine($"Node #{nodeId} not found.");
            return;
        }

        Console.WriteLine($"Composition paths for {node}:");
        Console.WriteLine();

        var paths = new List<List<Node>>();
        FindPathsToRoot(node, new List<Node> { node }, paths, new HashSet<long>());

        if (paths.Count == 0)
        {
            Console.WriteLine("  (this is a root node — no upward paths)");
            return;
        }

        for (int i = 0; i < paths.Count; i++)
        {
            Console.WriteLine($"  Path {i + 1}:");
            var path = paths[i];
            for (int j = path.Count - 1; j >= 0; j--)
            {
                var indent = new string(' ', (path.Count - 1 - j) * 2);
                var arrow = j < path.Count - 1 ? "-> " : "   ";
                Console.WriteLine($"    {indent}{arrow}{path[j]}");
            }
            Console.WriteLine();
        }
    }

    /// <summary>
    /// Print full tree starting from all roots.
    /// </summary>
    public void PrintFullTree()
    {
        var roots = _db.GetRoots();
        if (roots.Count == 0)
        {
            Console.WriteLine("(empty tree)");
            return;
        }

        var visited = new HashSet<long>();
        foreach (var root in roots)
        {
            PrintSubtree(root, "", true, 20, 0, visited);
        }

        // Show orphan nodes (no edges at all) separately
        var allNodes = _db.GetAllNodes();
        var orphans = allNodes.Where(n => !visited.Contains(n.Id)).ToList();
        if (orphans.Count > 0)
        {
            Console.WriteLine();
            Console.WriteLine("Unlinked nodes:");
            foreach (var orphan in orphans)
                Console.WriteLine($"  {orphan}");
        }
    }

    /// <summary>
    /// Trace path between two specific nodes (bidirectional BFS).
    /// </summary>
    public void PrintTrace(long fromId, long toId)
    {
        var from = _db.GetNode(fromId);
        var to = _db.GetNode(toId);
        if (from == null || to == null)
        {
            Console.WriteLine($"Node not found: {(from == null ? $"#{fromId}" : $"#{toId}")}");
            return;
        }

        var path = FindPath(fromId, toId);
        if (path == null)
        {
            Console.WriteLine($"No path between {from} and {to}");
            return;
        }

        Console.WriteLine($"Trace: {from} -> {to}");
        Console.WriteLine();
        for (int i = 0; i < path.Count; i++)
        {
            var indent = new string(' ', i * 2);
            var arrow = i > 0 ? "-> " : "   ";
            Console.WriteLine($"  {indent}{arrow}{path[i]}");
        }
    }

    /// <summary>
    /// Print statistics about the tree.
    /// </summary>
    public void PrintStats()
    {
        var (nodes, edges, roots, leaves) = _db.GetStats();
        var depth = ComputeMaxDepth();

        Console.WriteLine("Godding Tree Statistics");
        Console.WriteLine("=======================");
        Console.WriteLine($"  Nodes:     {nodes}");
        Console.WriteLine($"  Edges:     {edges}");
        Console.WriteLine($"  Roots:     {roots}  (1 — the origin)");
        Console.WriteLine($"  Leaves:    {leaves}  (the many — endpoints)");
        Console.WriteLine($"  Max depth: {depth}");
        Console.WriteLine();

        if (nodes > 0)
        {
            var allNodes = _db.GetAllNodes();
            int functions = allNodes.Count(n => n.Type == "function");
            int components = allNodes.Count(n => n.Type == "component");
            Console.WriteLine($"  Functions:  {functions}  (data + noise)");
            Console.WriteLine($"  Components: {components}  (compressed)");
            if (functions > 0)
                Console.WriteLine($"  Compression ratio: {functions}:{components} ({(double)components / functions:F2}x)");
        }
    }

    private void PrintSubtree(Node node, string prefix, bool isLast, int maxDepth, int depth, HashSet<long> visited)
    {
        if (!visited.Add(node.Id))
        {
            Console.WriteLine($"{prefix}{(isLast ? "\\-- " : "|-- ")}(cycle -> {node})");
            return;
        }

        var connector = depth == 0 ? "" : (isLast ? "\\-- " : "|-- ");
        Console.WriteLine($"{prefix}{connector}{node}");

        if (depth >= maxDepth) return;

        var children = _db.GetChildren(node.Id);
        for (int i = 0; i < children.Count; i++)
        {
            var childPrefix = depth == 0 ? "" : prefix + (isLast ? "    " : "|   ");
            PrintSubtree(children[i], childPrefix, i == children.Count - 1, maxDepth, depth + 1, visited);
        }
    }

    private void FindPathsToRoot(Node current, List<Node> path, List<List<Node>> allPaths, HashSet<long> visited)
    {
        var parents = _db.GetParents(current.Id);
        if (parents.Count == 0)
        {
            allPaths.Add(new List<Node>(path));
            return;
        }

        foreach (var parent in parents)
        {
            if (visited.Contains(parent.Id)) continue;
            visited.Add(parent.Id);
            path.Add(parent);
            FindPathsToRoot(parent, path, allPaths, visited);
            path.RemoveAt(path.Count - 1);
            visited.Remove(parent.Id);
        }
    }

    private List<Node>? FindPath(long fromId, long toId)
    {
        // BFS treating edges as undirected
        var queue = new Queue<long>();
        var prev = new Dictionary<long, long>();
        queue.Enqueue(fromId);
        prev[fromId] = -1;

        while (queue.Count > 0)
        {
            var current = queue.Dequeue();
            if (current == toId)
            {
                var path = new List<Node>();
                var id = toId;
                while (id != -1)
                {
                    path.Add(_db.GetNode(id)!);
                    id = prev[id];
                }
                path.Reverse();
                return path;
            }

            // Check both children and parents (undirected traversal)
            var neighbors = _db.GetChildren(current).Concat(_db.GetParents(current));
            foreach (var neighbor in neighbors)
            {
                if (!prev.ContainsKey(neighbor.Id))
                {
                    prev[neighbor.Id] = current;
                    queue.Enqueue(neighbor.Id);
                }
            }
        }

        return null;
    }

    private int ComputeMaxDepth()
    {
        var roots = _db.GetRoots();
        int maxDepth = 0;
        foreach (var root in roots)
        {
            var depth = ComputeDepth(root.Id, new HashSet<long>());
            maxDepth = Math.Max(maxDepth, depth);
        }
        return maxDepth;
    }

    private int ComputeDepth(long nodeId, HashSet<long> visited)
    {
        if (!visited.Add(nodeId)) return 0;
        var children = _db.GetChildren(nodeId);
        if (children.Count == 0) return 1;
        return 1 + children.Max(c => ComputeDepth(c.Id, visited));
    }

    /// <summary>
    /// Fairness audit. Every node must be reachable. No node left behind.
    /// All helps one and one helps all.
    /// </summary>
    public void PrintBalance()
    {
        var allNodes = _db.GetAllNodes();
        if (allNodes.Count == 0)
        {
            Console.WriteLine("(empty tree — nothing to balance)");
            return;
        }

        var roots = _db.GetRoots();
        var leaves = _db.GetLeaves();

        // 1. Orphans — nodes with no edges at all
        var connected = new HashSet<long>();
        foreach (var node in allNodes)
        {
            if (_db.GetChildren(node.Id).Count > 0 || _db.GetParents(node.Id).Count > 0)
                connected.Add(node.Id);
        }
        var orphans = allNodes.Where(n => !connected.Contains(n.Id)).ToList();

        // 2. Reachability — can every node reach a root?
        var unreachable = new List<Node>();
        foreach (var node in allNodes)
        {
            if (roots.Any(r => r.Id == node.Id)) continue;
            var paths = new List<List<Node>>();
            FindPathsToRoot(node, new List<Node> { node }, paths, new HashSet<long>());
            if (paths.Count == 0 && connected.Contains(node.Id))
                unreachable.Add(node);
        }

        // 3. Branch depths — measure balance
        var branchDepths = new Dictionary<long, int>();
        foreach (var root in roots)
        {
            var directChildren = _db.GetChildren(root.Id);
            foreach (var child in directChildren)
            {
                branchDepths[child.Id] = ComputeDepth(child.Id, new HashSet<long>());
            }
        }

        // 4. Connectivity — can any node reach any other?
        int totalPairs = 0;
        int reachablePairs = 0;
        foreach (var a in allNodes)
        {
            foreach (var b in allNodes)
            {
                if (a.Id >= b.Id) continue;
                totalPairs++;
                if (FindPath(a.Id, b.Id) != null)
                    reachablePairs++;
            }
        }

        // Report
        Console.WriteLine("Fairness Audit");
        Console.WriteLine("==============");
        Console.WriteLine($"  All helps one and one helps all.");
        Console.WriteLine();

        // Orphans
        if (orphans.Count == 0)
            Console.WriteLine("  Orphans:       0  (none left behind)");
        else
        {
            Console.WriteLine($"  Orphans:       {orphans.Count}  (LEFT BEHIND)");
            foreach (var o in orphans)
                Console.WriteLine($"    ! {o}");
        }

        // Unreachable
        if (unreachable.Count == 0)
            Console.WriteLine("  Unreachable:   0  (all can reach a root)");
        else
        {
            Console.WriteLine($"  Unreachable:   {unreachable.Count}  (CANNOT REACH ROOT)");
            foreach (var u in unreachable)
                Console.WriteLine($"    ! {u}");
        }

        // Connectivity
        double connectivity = totalPairs > 0 ? (double)reachablePairs / totalPairs : 1.0;
        string connLabel = connectivity >= 1.0 ? "FAIR" : connectivity >= 0.5 ? "PARTIAL" : "UNFAIR";
        Console.WriteLine($"  Connectivity:  {connectivity:P1}  ({connLabel} — {reachablePairs}/{totalPairs} pairs)");

        // Branch balance
        if (branchDepths.Count > 1)
        {
            int minD = branchDepths.Values.Min();
            int maxD = branchDepths.Values.Max();
            double avgD = branchDepths.Values.Average();
            double variance = branchDepths.Values.Select(d => Math.Pow(d - avgD, 2)).Average();
            double imbalance = maxD > 0 ? (double)(maxD - minD) / maxD : 0;
            string balLabel = imbalance <= 0.2 ? "BALANCED" : imbalance <= 0.5 ? "LEANING" : "UNBALANCED";
            Console.WriteLine($"  Branch depth:  min={minD} max={maxD} avg={avgD:F1} variance={variance:F2}");
            Console.WriteLine($"  Balance:       {balLabel} (imbalance={imbalance:P0})");
        }
        else if (branchDepths.Count == 1)
            Console.WriteLine($"  Balance:       SINGLE BRANCH (depth={branchDepths.Values.First()})");

        // Type distribution
        int functions = allNodes.Count(n => n.Type == "function");
        int components = allNodes.Count(n => n.Type == "component");
        double typeRatio = allNodes.Count > 0 ? (double)Math.Min(functions, components) / Math.Max(functions, components) : 1;
        string typeLabel = typeRatio >= 0.5 ? "BALANCED" : typeRatio >= 0.25 ? "SKEWED" : "LOPSIDED";
        Console.WriteLine($"  Type mix:      {functions}F / {components}C  ratio={typeRatio:F2} ({typeLabel})");

        // Verdict
        Console.WriteLine();
        bool fair = orphans.Count == 0 && unreachable.Count == 0 && connectivity >= 1.0;
        if (fair)
            Console.WriteLine("  Verdict: FAIR FOR ALL");
        else
        {
            Console.WriteLine("  Verdict: NOT YET FAIR");
            if (orphans.Count > 0)
                Console.WriteLine("    -> Link orphan nodes so none are left behind");
            if (unreachable.Count > 0)
                Console.WriteLine("    -> Connect unreachable nodes to a root path");
            if (connectivity < 1.0)
                Console.WriteLine("    -> Bridge disconnected components so all can reach all");
        }
    }

    /// <summary>
    /// Resolve a node by ID (numeric) or name (string).
    /// </summary>
    public Node? ResolveNode(string identifier)
    {
        if (long.TryParse(identifier, out var id))
            return _db.GetNode(id);
        return _db.GetNodeByName(identifier);
    }
}
