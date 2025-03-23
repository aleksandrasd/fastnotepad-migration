import hashlib
import json
import time
import random
import datetime
import os 

def convert_to_unix(timestamp_str):
    dt = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d-%H-%M-%S")
    unix_timestamp = int(time.mktime(dt.timetuple()))
    return unix_timestamp


def generate_note_id():
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=16))

def create_note(title, content, timestamp):
    note_id = generate_note_id()
    color = "#00FF0000"
    text_color = "#FFFFFFFF"
    index_entry = f"^!{note_id};;{color};{timestamp};;{text_color};{len(content)};;{{\"reminder\":0}};{title}"
    return note_id, index_entry, content

def generate_notes(notes):
    index_entries = []
    note_contents = {}
    
    for title, content, timestamp in notes:
        note_id, index_entry, note_content = create_note(title, content, timestamp)
        index_entries.append(index_entry)
        note_contents[f"_{note_id}"] = note_content
        note_contents[f"ScrollY_{note_id}"] = 0
    
    index_section = json.dumps({"index": "^!" + "^!".join(index_entries)}, ensure_ascii = False)
    notes_section = json.dumps(note_contents, ensure_ascii = False)
    content = f"{index_section}{{[!*|@]}}{{}}{{[!*|@]}}{notes_section}"
    sha1_hash = hashlib.sha1(content.encode()).hexdigest()
    
    return f"{sha1_hash}#{content}"
    
def extract_notes(directory):
    notes = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                base_name = os.path.splitext(file)[0]  
                unix_time = convert_to_unix(base_name)
                
                if unix_time is None:
                    raise Exception("invalid date")
                
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                title = content[:min(32, content.find('\n'))] 
                notes.append((title, content, unix_time))
    
    return notes


folder_path = r"fastnote"
notes_list = extract_notes(folder_path)

print(len(notes_list))
formatted_notes = generate_notes(notes_list)

with open("backup", "w", encoding="utf-8") as text_file:
    text_file.write(formatted_notes)