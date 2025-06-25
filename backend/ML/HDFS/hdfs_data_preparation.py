import pandas as pd
import numpy as np
from sklearn.utils import shuffle

df = pd.read_csv("./log_data/HDFS_v1/preprocessed/Event_occurrence_matrix.csv")

rows = []

for _, row in df.iterrows():
    block_id = row['BlockId']
    label = row['Label']
    event_counts = row[3:]
    events = []
    event_counts = event_counts.fillna(0)
    for event_type, count in event_counts.items():
        events.extend([event_type] * int(count))

    rows.append({
        'BlockId': block_id,
        'Label': label,
        'Events': events
    })

df_exploded = pd.DataFrame(rows)


def generate_thin_blocks(row, max_chunk_size=5, min_chunk_size=1):
    events = row['Events']
    label = row['Label']
    chunks = []
    np.random.shuffle(events)

    i = 0
    while i < len(events):
        chunk_size = np.random.randint(min_chunk_size, max_chunk_size + 1)
        chunk = events[i:i + chunk_size]
        i += chunk_size

        event_count = {f"E{i}": 0 for i in range(1, 30)}
        for ev in chunk:
            event_count[ev] += 1

        chunk_row = event_count
        chunk_row["Label"] = label
        chunks.append(chunk_row)

    return chunks


thin_blocks = []
for _, row in df_exploded.iterrows():
    thin_blocks.extend(generate_thin_blocks(row))

df_thin = pd.DataFrame(thin_blocks)

df_thick = df.drop(columns=["BlockId", "Type"]).copy()


def generate_medium_blocks(row, min_chunk_size=6, max_chunk_size=15):
    events = row['Events']
    label = row['Label']
    chunks = []
    np.random.shuffle(events)

    i = 0
    while i < len(events):
        chunk_size = np.random.randint(min_chunk_size, max_chunk_size + 1)
        chunk = events[i:i + chunk_size]
        i += chunk_size

        event_count = {f"E{i}": 0 for i in range(1, 30)}
        for ev in chunk:
            if ev in event_count:
                event_count[ev] += 1

        chunk_row = event_count
        chunk_row["Label"] = label
        chunks.append(chunk_row)

    return chunks


medium_blocks = []
for _, row in df_exploded.iterrows():
    medium_blocks.extend(generate_medium_blocks(row))

df_medium = pd.DataFrame(medium_blocks)

df_final = pd.concat([df_thin, df_medium, df_thick], ignore_index=True)
df_final = shuffle(df_final, random_state=42)

df_final.to_csv("./log_data/HDFS_v1/preprocessed/hybrid_training_dataset.csv", index=False)
