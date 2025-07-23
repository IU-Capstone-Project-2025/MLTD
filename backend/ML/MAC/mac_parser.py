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
    message = " ".join(tokens[6:] if tokens[0].isdigit() else tokens[5:]).strip()
    i = 4  # the magic number for finding the process name and its identifier
    s = ""
    process = None
    while i != len(tokens):
        s += tokens[i]
        match = re.match(r'^(.*?)\[?(\d+)\]?', s)
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
        path = f"ML/log_data/MAC/{filename}"
    else:
        path = f"logs/{filename}"

    with open(path, 'r') as f:
        for i, line in enumerate(f.readlines()):
            if filename.endswith(".csv"):
                if i == 0:
                    continue
                line = " ".join(line.split(",")[2:])
            line = line.strip()

            response = check_lines(line)
            if response:
                lines.append(line)
            else:
                return False

        if len(lines) == 0:
            return False

        for line in lines:
            try:
                response = parse_line(line)
                if response:
                    if response["process"] == 'sshd':
                        return False
                    parsed_lines.append(response)
            except:
                return False
    df = pd.DataFrame(parsed_lines)
    if df.empty:
        return False
    if for_train:
        return df
    else:
        df.to_csv(f"logs/{filename.split('.log')[0]}.csv")
        return True
