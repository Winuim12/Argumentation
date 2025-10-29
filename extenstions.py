import itertools

def format_set(S):
    if not S:
        return "∅"       # hoặc "" nếu bạn chỉ muốn trống hẳn
    else:
        return "{" + ", ".join(S) + "}"
    
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
    # a được bảo vệ nếu với mọi b tấn công a, tồn tại c trong S tấn công lại b
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
        if not any(S < T for T in complete_sets):  # không bị chứa trong set lớn hơn
            preferred.append(S)
    return preferred

def stable_extensions(args, attacks):
    stable = []
    for L in itertools.chain.from_iterable(itertools.combinations(args, r) for r in range(len(args)+1)):
        S = set(L)
        if is_conflict_free(S, attacks):
            # Kiểm tra: mọi argument ngoài S đều bị ít nhất 1 phần tử trong S tấn công
            others = set(args) - S
            if all(any((a, b) in attacks for a in S) for b in others):
                stable.append(S)
    return stable

if __name__ == "__main__":
    args, attacks = parse_af("af.txt")
    print(args, attacks)
    exts = complete_extensions(args, attacks)
    preferred = preferred_extensions(args, attacks)
    stable=stable_extensions(args,attacks)
    print("Complete sets:", exts)
    print("Preferred sets:", preferred)
    print("Stable set:", stable)
