import json
from pathlib import Path

from graphify.analyze import god_nodes, surprising_connections, suggest_questions
from graphify.build import build_from_json
from graphify.cluster import cluster, score_all
from graphify.export import to_html, to_json
from graphify.report import generate


ROOT = Path(__file__).parent
OUT = ROOT / "graphify-out"
OUT.mkdir(exist_ok=True)
extraction = json.loads((ROOT / "AI-SYSTEM-EXTRACTION.json").read_text(encoding="utf-8"))
detection = {
    "total_files": len(list(ROOT.glob("*.md"))),
    "total_words": sum(len(p.read_text(encoding="utf-8").split()) for p in ROOT.glob("*.md")),
    "needs_graph": True,
    "warning": None,
    "files": {"document": [str(p) for p in ROOT.glob("*.md")]},
}

graph = build_from_json(extraction)
communities = cluster(graph)
cohesion = score_all(graph, communities)
labels = {
    cid: {
        0: "Shared AI Services",
        1: "D-Drive Storage",
        2: "Clients and Interfaces",
        3: "Runtime Gaps",
    }.get(cid, f"System Community {cid}")
    for cid in communities
}
gods = god_nodes(graph)
surprises = surprising_connections(graph, communities)
questions = suggest_questions(graph, communities, labels)
tokens = {"input": 0, "output": 0}

report = generate(
    graph,
    communities,
    cohesion,
    labels,
    gods,
    surprises,
    detection,
    tokens,
    str(ROOT),
    suggested_questions=questions,
)
(OUT / "GRAPH_REPORT.md").write_text(report, encoding="utf-8")
to_json(graph, communities, str(OUT / "graph.json"))
if graph.number_of_nodes() <= 5000:
    to_html(graph, communities, str(OUT / "graph.html"), community_labels=labels)

(OUT / "graph-analysis.json").write_text(
    json.dumps(
        {
            "communities": {str(k): v for k, v in communities.items()},
            "cohesion": {str(k): v for k, v in cohesion.items()},
            "gods": gods,
            "surprises": surprises,
            "questions": questions,
        },
        indent=2,
    ),
    encoding="utf-8",
)
print(json.dumps({"nodes": graph.number_of_nodes(), "edges": graph.number_of_edges(), "communities": len(communities)}))
