# genpark-enterprise-data-lineage-impact-graph-analyzer-skill

[![GenPark AI](https://img.shields.io/badge/GenPark_AI-www.genpark.ai-blue.svg)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark_Company_92955550-0077B5.svg)](https://www.linkedin.com/company/92955550)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Dependencies](https://img.shields.io/badge/dependencies-0%20(Pure%20Stdlib)-brightgreen.svg)](requirements.txt)
[![MCP Compliant](https://img.shields.io/badge/MCP-JSON--RPC%202.0-purple.svg)](mcp_server.py)

Enterprise Data Lineage & Schema Change Blast-Radius Impact Analyzer. Constructs column- and table-level Directed Acyclic Graphs (DAGs) across Tencent Cloud Data Warehouses, Tencent Docs spreadsheets, and BI executive dashboards, performs upstream provenance and downstream blast-radius traversal, and renders Mermaid lineage diagrams.

---

## 🌐 Official GenPark AI Ecosystem Links

- **GenPark Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Official Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550) ([https://www.llinkedin.com/company/92955550](https://www.llinkedin.com/company/92955550))

---

## 🌟 Key Features

- **100% Zero External Dependencies**: Runs entirely on the Python 3.9+ standard library.
- **Model Context Protocol (MCP) Standard**: Native support for JSON-RPC 2.0 `initialize`, `tools/list`, and `tools/call`.
- **Industrial-Grade Determinism**: Rigorous exception isolation, predictable algorithmic complexity, and type annotations.
- **Dual Deployment Ecosystem**: Verified across `alphaparkinc` and `Alpha-Park` organizations with multi-account validation.

---

## 🚀 Quick Start

### 1. Direct Python SDK Usage

```python
"""Example usage for EnterpriseDataLineageImpactGraphAnalyzer."""
import sys
import json
from client import EnterpriseDataLineageImpactGraphAnalyzer

sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("=== Enterprise WorkBuddy Data Lineage & Schema Blast-Radius Analyzer Demo ===")
    analyzer = EnterpriseDataLineageImpactGraphAnalyzer()

    pipeline_edges = [
        {"source": "wechat_pay_raw_stream", "target": "dwd_merchant_settlement", "transformation": "FLINK_STREAM", "criticality": "HIGH"},
        {"source": "dwd_merchant_settlement", "target": "ads_q4_gmv_summary", "transformation": "SPARK_SQL", "criticality": "CRITICAL"},
        {"source": "ads_q4_gmv_summary", "target": "tencent_docs_board_sheet", "transformation": "MCP_CONNECTOR", "criticality": "CRITICAL"},
        {"source": "tencent_docs_board_sheet", "target": "workbuddy_ceo_briefing_ppt", "transformation": "SLIDE_COMPILER", "criticality": "CRITICAL"}
    ]

    # 1. Register DAG lineage edges
    print("\n--- 1. Registering Enterprise Data Pipeline Lineage Graph ---")
    reg = analyzer.register_lineage_edges(pipeline_edges)
    print(f"Registered {reg['edges_registered']} edges across {reg['total_nodes']} nodes.")

    # 2. Perform Downstream Blast-Radius Impact Analysis
    print("\n--- 2. Analyzing Downstream Impact of Schema Change on 'wechat_pay_raw_stream' ---")
    impact = analyzer.analyze_downstream_impact("wechat_pay_raw_stream")
    print(f"Blast Radius Severity: {impact['blast_radius_severity']} (Impacted Artifacts: {impact['total_downstream_impacted']})")
    for dep in impact["impacted_dependents"]:
        print(f"  Hop {dep['hop_distance']}: {dep['node_id']} (via {dep['transformation']}, Criticality: {dep['criticality']})")

    # 3. Render Mermaid Architecture Diagram
    print("\n--- 3. Rendering Mermaid Lineage Diagram ---")
    print(analyzer.render_mermaid_lineage())

if __name__ == "__main__":
    main()

```

### 2. Run as Model Context Protocol (MCP) Server

Start standard JSON-RPC 2.0 server over `stdio`:

```bash
python mcp_server.py
```

Execute embedded test harness:

```bash
python mcp_server.py --test
```

---

## 🛠️ MCP Tool Specification

Inspect [`skill.json`](skill.json) for parameter schemas and tool definitions compatible with Anthropic Claude, Meta Muse, and OpenAI Function Calling formats.

---

## 📜 License & Community

Licensed under the [MIT License](LICENSE). Copyright © 2026 [GenPark AI](https://www.genpark.ai).
Follow us on LinkedIn: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550) | [https://www.llinkedin.com/company/92955550](https://www.llinkedin.com/company/92955550)
