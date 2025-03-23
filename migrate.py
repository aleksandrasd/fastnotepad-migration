import hashlib
import json
import time
import random
import datetime
import argparse
import os
import sys

TIME_FORMAT = "%Y-%m-%d-%H-%M-%S"

def convert_to_unix(timestamp_str, time_format):
  dt = datetime.datetime.strptime(timestamp_str, time_format)
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
        unix_time = convert_to_unix(base_name, TIME_FORMAT)
        
        with open(file_path, "r", encoding="utf-8") as f:
          content = f.read()
        title = content[:min(32, content.find('\n'))] 
        notes.append((title, content, unix_time))
  
  return notes  

def main():
  parser = argparse.ArgumentParser(description="Migrate (convert) Fastnotepad notes to the newest format.")
  parser.add_argument("notes_folder", type=str, help="Path to the folder containing Fastnotepad notes")
  parser.add_argument("output_file", type=str, help="Path to the output file")
  args = parser.parse_args()

  if not os.path.isdir(args.notes_folder):
    sys.stdout.write(f"Error: The provided path '{args.notes_folder}' is not a valid directory.\n")
    sys.stdout.flush()
    exit(1)
  try:  
    notes_list = extract_notes(args.notes_folder)    
    formatted_notes = generate_notes(notes_list)
    with open(args.output_file, "w", encoding="utf-8") as text_file:
      text_file.write(formatted_notes)
  except Exception as e:
    sys.stdout.write(f"Migration failed: {e}.\n")
    sys.stdout.flush()
    exit(1)
  else:   
    sys.stdout.write(f"Converted {len(notes_list)} notes.\n")
    sys.stdout.flush()
    exit(0)

if __name__ == "__main__":
  main()