import numpy as np
import sqlite3
import io
import os


def convert_array(text):
   out = io.BytesIO(text)
   out.seek(0)
   return np.load(out)
   
conn_db = sqlite3.connect('database.db')
cursor = conn_db.execute("SELECT * FROM face_info")
db_data = cursor.fetchall()

total_distances = []
total_names = []
for data in db_data:
    total_names.append(data[1])
    db_embeddings = convert_array(data[2])
    distance = round(np.linalg.norm(db_embeddings - embeddings), 2)
    total_distances.append(distance)
total_result = dict(zip(total_names, total_distances))
idx_min = np.argmin(total_distances)

distance, name = total_distances[idx_min], total_names[idx_min]
conn_db.close()

if distance < threshold:
    return name, distance, total_result
else:
    name = "Unknown Person"
    return name, distance, total_result
