import pandas as pd
import re


def preprocess_template(template):
    regex = re.escape(template)
    regex = regex.replace(r'\[\*\]', '.*')
    regex = regex.replace(r'\.\*', '.*')
    return f'^{regex}$'


def match_content_to_event(content, events_df):
    for _, row in events_df.iterrows():
        event = row["EventTemplate"]
        event = preprocess_template(event)
        if re.fullmatch(event, content.strip()):
            return row["EventId"]
    return None


def extract_block_id(content):
    match = re.search(r'blk_[\-]?\d+', str(content))
    return match.group(0) if match else None


def parse_line(line, events_df):
    tokens = line.split(" ")
    date = tokens[0]
    time = tokens[1]
    pid = tokens[2]
    level = tokens[3]
    tokens[4] = tokens[4][:-1]
    tokens[5] = " ".join(tokens[5:])
    component = tokens[4]
    content = tokens[5]
    block = extract_block_id(content)
    event_id = match_content_to_event(content, events_df)
    return {"Date": date, "Time": time, "Pid": pid, "Level": level, "Component": component,
            "Content": content, "BlockID": block, "EventId": event_id}


def parse_file(filename):
    events = pd.read_csv("ML/log_data/HDFS_v1/preprocessed/HDFS.log_templates.csv")
    parsed_lines = []

    with open(f"logs/{filename}", 'r') as f:
        for line in f.readlines():
            try:
                parsed_lines.append(parse_line(line.strip(), events))
            except:
                return False

    df = pd.DataFrame(parsed_lines).dropna()
    if df.empty:
        return False
    df.to_csv(f"logs/{filename.split('.log')[0]}.csv")
    return True
