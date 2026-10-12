"""
Enterprise Data Lineage & Impact Graph Analyzer (Zero External Dependencies)
Performs BFS/DFS graph traversal for downstream blast-radius and upstream provenance analysis.
Official Website: https://www.genpark.ai | LinkedIn: https://www.llinkedin.com/company/92955550
"""
import time
import math
import hashlib
import json
from typing import Dict, Any, List, Optional, Set

class EnterpriseDataLineageImpactGraphAnalyzer:
    def __init__(self):
        self.downstream_adj: Dict[str, List[Dict[str, Any]]] = {}
        self.upstream_adj: Dict[str, List[Dict[str, Any]]] = {}
        self.node_metadata: Dict[str, Dict[str, Any]] = {}

    def register_lineage_edges(self, edges: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Registers directed data pipeline edges from source tables to target artifacts."""
        added = 0
        for e in edges:
            src = e.get("source")
            tgt = e.get("target")
            if not src or not tgt:
                continue
            trans = e.get("transformation", "SQL_ETL")
            crit = e.get("criticality", "HIGH")

            if src not in self.downstream_adj:
                self.downstream_adj[src] = []
            self.downstream_adj[src].append({"target": tgt, "transformation": trans, "criticality": crit})

            if tgt not in self.upstream_adj:
                self.upstream_adj[tgt] = []
            self.upstream_adj[tgt].append({"source": src, "transformation": trans, "criticality": crit})

            self.node_metadata[src] = {"node_id": src, "type": e.get("source_type", "TABLE")}
            self.node_metadata[tgt] = {"node_id": tgt, "type": e.get("target_type", "ARTIFACT")}
            added += 1

        return {
            "edges_registered": added,
            "total_nodes": len(self.node_metadata)
        }

    def analyze_downstream_impact(self, modified_node: str) -> Dict[str, Any]:
        """Performs BFS traversal to identify all downstream tables, sheets, and dashboards impacted by a breaking schema change."""
        visited: Set[str] = set()
        queue = [(modified_node, 0)]
        impacted_nodes = []

        while queue:
            curr, depth = queue.pop(0)
            for edge in self.downstream_adj.get(curr, []):
                nxt = edge["target"]
                if nxt not in visited:
                    visited.add(nxt)
                    impacted_nodes.append({
                        "node_id": nxt,
                        "hop_distance": depth + 1,
                        "transformation": edge["transformation"],
                        "criticality": edge["criticality"]
                    })
                    queue.append((nxt, depth + 1))

        high_crit_count = sum(1 for n in impacted_nodes if n["criticality"] == "CRITICAL" or n["criticality"] == "HIGH")
        severity = "CRITICAL_BREAKING_CHANGE" if high_crit_count >= 2 else ("MODERATE_IMPACT" if impacted_nodes else "SAFE_ISOLATED")

        return {
            "source_modified_node": modified_node,
            "total_downstream_impacted": len(impacted_nodes),
            "high_criticality_impacted": high_crit_count,
            "blast_radius_severity": severity,
            "impacted_dependents": impacted_nodes
        }

    def trace_upstream_provenance(self, target_node: str) -> Dict[str, Any]:
        """Traces all root-cause upstream data sources feeding into target_node."""
        visited: Set[str] = set()
        queue = [(target_node, 0)]
        upstream_sources = []

        while queue:
            curr, depth = queue.pop(0)
            for edge in self.upstream_adj.get(curr, []):
                src = edge["source"]
                if src not in visited:
                    visited.add(src)
                    upstream_sources.append({
                        "source_node": src,
                        "hop_distance": depth + 1,
                        "transformation": edge["transformation"]
                    })
                    queue.append((src, depth + 1))

        return {
            "target_node": target_node,
            "total_upstream_ancestors": len(upstream_sources),
            "upstream_lineage": upstream_sources
        }

    def render_mermaid_lineage(self) -> str:
        """Synthesizes Mermaid Flowchart LR syntax for the registered lineage graph."""
        lines = ["flowchart LR"]
        for src, edges in sorted(self.downstream_adj.items()):
            for e in edges:
                tgt = e["target"]
                trans = e["transformation"]
                lines.append(f'    {src}["{src}"] -->|"{trans}"| {tgt}["{tgt}"]')
        return "\n".join(lines)
