"""MCP Server for Enterprise Data Lineage Impact Graph Analyzer."""
import sys
import json
import time
from client import EnterpriseDataLineageImpactGraphAnalyzer

analyzer = EnterpriseDataLineageImpactGraphAnalyzer()

def handle_call_tool(params):
    name = params.get("name")
    args = params.get("arguments", {})
    if name != "analyze_enterprise_data_lineage":
        raise ValueError(f"Unknown tool: {name}")

    action = args.get("action", "analyze_downstream_impact")
    edges = args.get("edges", [])
    if edges:
        analyzer.register_lineage_edges(edges)

    target = args.get("target_node", "raw_orders")

    if action == "register_lineage_edges":
        return analyzer.register_lineage_edges(edges)
    elif action == "analyze_downstream_impact":
        return analyzer.analyze_downstream_impact(target)
    elif action == "trace_upstream_provenance":
        return analyzer.trace_upstream_provenance(target)
    elif action == "render_mermaid_lineage":
        return {"mermaid_diagram": analyzer.render_mermaid_lineage()}
    else:
        raise ValueError(f"Invalid action: {action}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("Running self-test...")
        edges = [
            {"source": "raw_stripe_events", "target": "stg_payments", "transformation": "DBT_CLEAN", "criticality": "HIGH"},
            {"source": "stg_payments", "target": "fct_revenue_daily", "transformation": "SQL_AGG", "criticality": "CRITICAL"},
            {"source": "fct_revenue_daily", "target": "cfo_exec_ppt_deck", "transformation": "WORKBUDDY_SYNC", "criticality": "CRITICAL"}
        ]
        analyzer.register_lineage_edges(edges)
        impact = analyzer.analyze_downstream_impact("raw_stripe_events")
        assert impact["total_downstream_impacted"] == 3
        assert impact["blast_radius_severity"] == "CRITICAL_BREAKING_CHANGE"

        prov = analyzer.trace_upstream_provenance("cfo_exec_ppt_deck")
        assert prov["total_upstream_ancestors"] == 3
        mmd = analyzer.render_mermaid_lineage()
        assert "flowchart LR" in mmd
        print("Self-test PASSED!")
        sys.exit(0)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            msg_id = req.get("id")
            method = req.get("method")
            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": {"name": "EnterpriseDataLineageImpactGraphAnalyzer", "version": "1.0.0"},
                        "capabilities": {"tools": {}}
                    }
                }
            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [{
                            "name": "analyze_enterprise_data_lineage",
                            "description": "Register data pipeline edges, trace upstream data provenance, compute downstream schema change blast radius, and render Mermaid lineage diagrams.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "action": {"type": "string", "enum": ["register_lineage_edges", "analyze_downstream_impact", "trace_upstream_provenance", "render_mermaid_lineage"]},
                                    "edges": {"type": "array"},
                                    "target_node": {"type": "string"}
                                },
                                "required": ["action"]
                            }
                        }]
                    }
                }
            elif method == "tools/call":
                res = handle_call_tool(req.get("params", {}))
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {}}
            print(json.dumps(resp), flush=True)
        except Exception as e:
            err_resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err_resp), flush=True)

if __name__ == "__main__":
    main()
