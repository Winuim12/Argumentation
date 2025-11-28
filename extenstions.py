import itertools
import os

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def format_set(S):
    if not S:
        return "∅"
    else:
        return "{" + ", ".join(sorted(S)) + "}"
    
def parse_af(file):
    args, attacks = [], []
    with open(file) as f:
        for line in f:
            line = line.strip().replace('.', '')
            if line.startswith('arg('):
                args.append(line[4:-1])
            elif line.startswith('att('):
                parts = line[4:-1].split(',')
                attacks.append((parts[0], parts[1]))
    return args, attacks

def is_conflict_free(S, attacks):
    for (a, b) in attacks:
        if a in S and b in S:
            return False
    return True

def defended_by(S, a, attacks):
    attackers = [x for (x, y) in attacks if y == a]
    for b in attackers:
        if not any((c, b) in attacks for c in S):
            return False
    return True

def complete_extensions(args, attacks):
    complete = []
    for L in itertools.chain.from_iterable(itertools.combinations(args, r) for r in range(len(args)+1)):
        S = set(L)
        if is_conflict_free(S, attacks):
            defended = {a for a in args if defended_by(S, a, attacks)}
            if defended == S:
                complete.append(S)
    return complete

def preferred_extensions(args, attacks):
    complete_sets = complete_extensions(args, attacks)
    preferred = []
    for S in complete_sets:
        if not any(S < T for T in complete_sets):
            preferred.append(S)
    return preferred

def stable_extensions(args, attacks):
    stable = []
    for L in itertools.chain.from_iterable(itertools.combinations(args, r) for r in range(len(args)+1)):
        S = set(L)
        if is_conflict_free(S, attacks):
            others = set(args) - S
            if all(any((a, b) in attacks for a in S) for b in others):
                stable.append(S)
    return stable

def normalize_setlist(lst):
    return ",".join(sorted(format_set(s) for s in lst))

def load_expected(path):
    with open(path, encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
    expected = {}
    for line in lines:
        if line.startswith("COMPLETE:"):
            expected["COMPLETE"] = line.replace("COMPLETE:", "").strip()
        elif line.startswith("PREFERRED:"):
            expected["PREFERRED"] = line.replace("PREFERRED:", "").strip()
        elif line.startswith("STABLE:"):
            expected["STABLE"] = line.replace("STABLE:", "").strip()
    return expected

if __name__ == "__main__":
    folder = "testcase"
    exp_folder = "expected"

    files = sorted([f for f in os.listdir(folder) if f.endswith(".txt")])

    total = 0
    correct = 0

    for f in files:
        tc_path = os.path.join(folder, f)
        out_path = os.path.join(exp_folder, f.replace(".txt", ".out"))

        if not os.path.exists(out_path):
            print(f"⚠️ No expected output for {f}, skipping!")
            continue

        args, attacks = parse_af(tc_path)

        complete = complete_extensions(args, attacks)
        preferred = preferred_extensions(args, attacks)
        stable = stable_extensions(args, attacks)

        my_output = {
            "COMPLETE": normalize_setlist(complete),
            "PREFERRED": normalize_setlist(preferred),
            "STABLE": normalize_setlist(stable),
        }

        expected = load_expected(out_path)

        print("\n===============================")
        print("🔎 Testing:", f)
        print("===============================")

        ok = True
        for key in ["COMPLETE", "PREFERRED", "STABLE"]:
            if my_output[key] == expected[key]:
                color = GREEN
                status = "correct"
            else:
                color = RED
                status = "wrong"
                ok = False
            print(f"  {status.upper()}: {key} {color}{status}{RESET}")
            print(f"    Expected: {color}{expected[key]}{RESET}")
            print(f"    Got     : {color}{my_output[key]}{RESET}")

        total += 1
        if ok:
            correct += 1

    print("\n===============================")
    print(f"🎯 Result: {correct}/{total} tests passed")
    print("===============================")