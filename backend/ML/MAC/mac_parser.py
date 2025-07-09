import re
import pandas as pd


def check_lines(line):
    pattern = r'^[A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}'
    if re.match(pattern, line):
        return True
    else:
        return False


def parse_line(line):
    tokens = line.split()
    message = " ".join(tokens[5:]).strip()
    i = 4  # the magic number for finding the process name and its identifier
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
    lines = []
    parsed_lines = []

    if for_train:
        path = f"log_data/MAC/{filename}"
    else:
        path = f"logs/{filename}"

    with open(path, 'r') as f:
        for line in f.readlines():
            response = check_lines(line.strip())
            if response:
                lines.append(line.strip())
            else:
                # This fixes an IndexOutOfRangeException error when tests were done by Paramon.
                if len(lines) != 0:
                    lines[-1] += line.strip()
        for line in lines:
            response = parse_line(line)
            if response:
                parsed_lines.append(response)
    df = pd.DataFrame(parsed_lines)

    if for_train:
        return df
    else:
        df.to_csv("Mac.csv")

if __name__ == "__main__":
    parse_file("mac_template.csv")