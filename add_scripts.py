import csv
import re

pattern = r"===  Your score is (\d+)%  ==="

with open("CodeQuickCopy.csv") as f:
    data = list(csv.reader(f, delimiter=','))

for item in data[1:]:
    match = re.search(pattern, item[2])
    score = match.group(1) if match else ""
    with open(f"{item[0]}.py", "w") as f:
        f.write(f"# Claimed Score: {score}\n\n{item[1]}")
