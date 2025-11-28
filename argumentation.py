# argumentation.py
import re
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import os

# --- Example: thay bằng đọc file nếu cần ---
# sample_af = """
# # Example AF
# arg(a).
# arg(b).
# arg(c).
# arg(d).
# att(a,b).
# att(b,a).
# att(b,c).
# att(b,d).
# att(d,d).
# """

with open("af.txt", "r", encoding="utf-8") as f:
    sample_af = f.read()

def parse_af(text):
    args = set()
    attacks = []
    for line in text.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m_arg = re.match(r"arg\(\s*([A-Za-z0-9_]+)\s*\)\s*\.", line)
        m_att = re.match(r"att\(\s*([A-Za-z0-9_]+)\s*,\s*([A-Za-z0-9_]+)\s*\)\s*\.", line)
        if m_arg:
            args.add(m_arg.group(1))
        elif m_att:
            a, b = m_att.group(1), m_att.group(2)
            attacks.append((a, b))
            args.add(a); args.add(b)
        else:
            m_arrow = re.match(r"([A-Za-z0-9_]+)\s*->\s*([A-Za-z0-9_]+)", line)
            if m_arrow:
                a, b = m_arrow.group(1), m_arrow.group(2)
                attacks.append((a, b)); args.add(a); args.add(b)
    return sorted(args), attacks

# Nếu bạn muốn đọc từ file: uncomment đoạn này và comment sample_af ở trên
# with open("myframework.af", "r", encoding="utf-8") as f:
#     sample_af = f.read()

args, attacks = parse_af(sample_af)

# Build directed graph
G = nx.DiGraph()
G.add_nodes_from(args)
G.add_edges_from(attacks)

# Print nodes/edges
print("Arguments (nodes):", args)
print("Attacks (edges):", attacks)

# Create adjacency matrix (rows attackers -> columns attacked)
adj_df = pd.DataFrame(0, index=args, columns=args, dtype=int)
for a, b in attacks:
    adj_df.loc[a, b] = 1

# Print adjacency matrix to console
print(adj_df.to_string())

# Prepare output path in current directory
out_filename = "attack_graph.png"
out_path = os.path.join(os.getcwd(), out_filename)

# Draw the attack graph and save it
plt.figure(figsize=(6,5))
pos = nx.spring_layout(G)  # layout
# nx.draw(G, pos, with_labels=True, node_size=900, arrowsize=18)
nx.draw(
    G,
    pos=nx.spring_layout(G,seed=42),
    with_labels=True,
    node_size=900,
    edgelist=G.edges(),
    connectionstyle='arc3,rad=0.1',  # tạo độ cong cho cạnh
    arrows=True,
    arrowsize=18
)
plt.title("Attack graph (AF)")

# Save with bbox_inches to avoid tight_layout warning and ensure file is written
plt.savefig(out_path, dpi=150, bbox_inches='tight')
plt.show()

print(f"Saved attack graph image to: {out_path}")
