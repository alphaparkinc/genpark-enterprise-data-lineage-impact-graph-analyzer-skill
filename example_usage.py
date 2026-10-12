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
