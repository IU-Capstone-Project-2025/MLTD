import re
import pandas as pd


def parse_line(line):
    tokens = line.split(",")
    message = " ".join(tokens[5:]).strip()
    i = 4
    s = ""
    process = None
    while i != len(tokens):
        s += tokens[i]
        match = re.match(r'^(.*?)\[(\d+)\]', s)
        i += 1
        if match:
            process = match.group(1)
            pid = match.group(2)
            break
    if process is None:
        return None
    return {
        "month": tokens[0],
        "day": tokens[1],
        "time": tokens[2],
        "hostname": tokens[3],
        "process": process,
        "pid": pid,
        "message": message
    }


def parse_file(filename, for_train=False):
    parsed_lines = []

    if for_train:
        path = f"log_data/SSH/{filename}"
    else:
        path = f"logs/{filename}"

    with open(path, 'r') as f:
        for line in f.readlines():
            response = parse_line(line)
            if response:
                parsed_lines.append(response)
    df = pd.DataFrame(parsed_lines)

    if for_train:
        return df
    else:
        df.to_csv("SSH.csv")
