import pandas as pd


def parse_line(line, for_train=False):
    tokens = line.split(" ")
    if for_train:
        ind = 9
    else:
        ind = 8
    message = " ".join(tokens[ind:]).strip()
    if message.isnumeric() or len(message) == 0:
        return False
    if for_train:
        return {
            "prefix": tokens[0],
            "timestamp1": tokens[1],
            "date": tokens[2],
            "node_id1": tokens[3],
            "full_datetime": tokens[4],
            "node_id2": tokens[5],
            "token1": tokens[6],
            "token2": tokens[7],
            "severity": tokens[8],
            "message": message
        }
    return {
        "timestamp1": tokens[0],
        "date": tokens[1],
        "node_id1": tokens[2],
        "full_datetime": tokens[3],
        "node_id2": tokens[4],
        "token1": tokens[5],
        "token2": tokens[6],
        "severity": tokens[7],
        "message": message
    }


def parse_file(filename, for_train=False):
    parsed_lines = []
    if for_train:
        path = f"../log_data/BGL/{filename}"
    else:
        path = f"../../logs/{filename}"
    with open(path, 'r') as f:
        for line in f:
            response = parse_line(line, for_train)
            if response:
                parsed_lines.append(response)
    df = pd.DataFrame(parsed_lines)
    if for_train:
        return df
    else:
        df.to_csv(f"../../logs/{filename.split('.log')[0]}.csv")