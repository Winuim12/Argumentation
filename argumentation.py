# # Parse a simple .af file format and draw the attack graph with NetworkX + matplotlib.
# # Supported input format (each line):
# #   arg(X).
# #   att(X,Y).
# # Lines starting with # are comments and ignored.
# # The script will:
# #  - parse the text
# #  - build a directed graph (attack graph)
# #  - show node list and edge list
# #  - save a PNG image to /mnt/data/attack_graph.png
# #  - display an adjacency table to the user
# #
# # You can replace `sample_af` with reading from a real file if you want:
# # with open("myframework.af") as f:
# #     text = f.read()

# import re
# import networkx as nx
# import matplotlib.pyplot as plt
# import pandas as pd
# import os

# sample_af = """
# # Example AF
# arg(a).
# arg(b).
# arg(c).
# att(a,b).
# att(b,a).
# att(b,c).
# """

# def parse_af(text):
#     args = set()
#     attacks = []
#     for line in text.strip().splitlines():
#         line = line.strip()
#         if not line or line.startswith("#"):
#             continue
#         m_arg = re.match(r"arg\(\s*([A-Za-z0-9_]+)\s*\)\s*\.", line)
#         m_att = re.match(r"att\(\s*([A-Za-z0-9_]+)\s*,\s*([A-Za-z0-9_]+)\s*\)\s*\.", line)
#         if m_arg:
#             args.add(m_arg.group(1))
#         elif m_att:
#             a, b = m_att.group(1), m_att.group(2)
#             attacks.append((a, b))
#             # ensure arguments mentioned in attacks are included
#             args.add(a); args.add(b)
#         else:
#             # try a fallback simple formats like "a -> b" or "a b" if needed
#             m_arrow = re.match(r"([A-Za-z0-9_]+)\s*->\s*([A-Za-z0-9_]+)", line)
#             if m_arrow:
#                 a, b = m_arrow.group(1), m_arrow.group(2)
#                 attacks.append((a, b)); args.add(a); args.add(b)
#     return sorted(args), attacks

# args, attacks = parse_af(sample_af)

# # Build directed graph
# G = nx.DiGraph()
# G.add_nodes_from(args)
# G.add_edges_from(attacks)

# # Print nodes/edges
# print("Arguments (nodes):", args)
# print("Attacks (edges):", attacks)

# # Create adjacency matrix (rows attackers -> columns attacked)
# adj_df = pd.DataFrame(0, index=args, columns=args, dtype=int)
# for a, b in attacks:
#     adj_df.loc[a, b] = 1

# print(adj_df)

# # # Draw the attack graph and save it
# # plt.figure(figsize=(6,5))
# # pos = nx.spring_layout(G)  # layout
# # nx.draw(G, pos, with_labels=True, node_size=900, arrowsize=18)
# # # draw edge labels if you want: nx.draw_networkx_edge_labels(G, pos, edge_labels={(u,v): "" for u,v in G.edges()})
# # out_path = "/mnt/data/attack_graph.png"
# # plt.title("Attack graph (AF)")
# # plt.tight_layout()
# # plt.savefig(out_path, dpi=150)
# # plt.show()

# # # Provide path to the saved image for download
# # print(f"Saved attack graph image to: {out_path}")
# # os.path.exists(out_path)

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
