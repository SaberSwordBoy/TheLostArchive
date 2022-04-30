import sys

ips = ["208.115.199.26", "54.36.108.162", "51.222.107.173"]

try:
    lines = []
    file = open(sys.argv[1], "r")
    for line in file.readlines():
        for ip in ips:
            if not ip in line:
                lines.append(line)
            elif ip in line:
                continue
    with open(sys.argv[2], "w") as f:
        f.writelines(lines)
except:
    print("Usage: python3 clean.py <file>")
