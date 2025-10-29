# app.py
import os
import re
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from dotenv import load_dotenv
import extenstions as exts


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-key")  # fallback nếu chưa set

def parse_af_text(text):
    args = set()
    attacks = []
    for line in text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        m_arg = re.match(r"arg\(\s*([A-Za-z0-9_]+)\s*\)\s*\.", line)
        m_att = re.match(r"att\(\s*([A-Za-z0-9_]+)\s*,\s*([A-Za-z0-9_]+)\s*\)\s*\.", line)
        if m_arg:
            args.add(m_arg.group(1))
        elif m_att:
            a, b = m_att.group(1), m_att.group(2)
            attacks.append((a, b)); args.add(a); args.add(b)
    return sorted(args), attacks

@app.route("/", methods=["GET"])
def index():
    # trang chính với form
    return render_template("index.html")

@app.route("/compute", methods=["POST"])
def compute():
    # input options: textarea 'aftext' OR file upload 'affile'
    aftext = request.form.get("aftext", "").strip()
    uploaded = request.files.get("affile", None)
    text = aftext
    if uploaded and uploaded.filename:
        try:
            text = uploaded.stream.read().decode("utf-8")
        except Exception as e:
            # try reading bytes then decode
            uploaded.stream.seek(0)
            text = uploaded.stream.read().decode("utf-8", errors="ignore")
    if not text:
        flash("Please input text in text area or upload .af file", "error")
        return redirect(url_for("index"))

    args, attacks = parse_af_text(text)

    # compute extensions via your extenstions module
    try:
        complete = exts.complete_extensions(args, attacks)
        preferred = exts.preferred_extensions(args, attacks)
        stable = exts.stable_extensions(args, attacks)
    except Exception as e:
        flash(f"Error when compute extension: {e}", "error")
        complete = preferred = stable = []

    # convert to displayable strings
    complete_str = [exts.format_set(S) for S in complete]
    preferred_str = [exts.format_set(S) for S in preferred]
    stable_str = [exts.format_set(S) for S in stable]

    # prepare JSON-like data for Cytoscape: nodes with ids, edges as {data:{source,target}}
    cy_nodes = [{"data": {"id": n, "label": n}} for n in args]
    cy_edges = [{"data": {"id": f"{a}-{b}", "source": a, "target": b}} for a, b in attacks]

    return render_template("index.html",
                           args=args,
                           attacks=attacks,
                           complete=complete_str,
                           preferred=preferred_str,
                           stable=stable_str,
                           cy_nodes=cy_nodes,
                           cy_edges=cy_edges,
                           raw_text=text)

# optional API to return JSON (useful for SPA)
@app.route("/api/compute", methods=["POST"])
def api_compute():
    payload = request.get_json(force=True)
    text = payload.get("text","")
    args, attacks = parse_af_text(text)
    complete = exts.complete_extensions(args, attacks)
    return jsonify({
        "args": args,
        "attacks": attacks,
        "complete": [exts.format_set(s) for s in complete]
    })

if __name__ == "__main__":
    # debug True only for dev
    app.run(host="0.0.0.0", port=5000, debug=True)