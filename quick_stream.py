from todoist_api_python.api import TodoistAPI
import os
import sys
import tempfile
import subprocess

key_path = os.path.expanduser("~/todoist_utils/api_key")
with open(key_path, encoding="utf8") as f:
    api_key = f.read().strip()

client = TodoistAPI(api_key)

# Create a temporary file
with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp_file:
    tmp_filename = tmp_file.name

try:
    # Open Vim to edit the temporary file
    subprocess.call(['vim', tmp_filename])
    
    # Read the contents after Vim closes
    with open(tmp_filename, 'r', encoding='utf8') as f:
        content = f.read()
    
    # Split into lines
    lines = content.strip().split('\n')
    
    if not lines or not lines[0].strip():
        print("Error: No task content provided")
        sys.exit(1)
    
    # First line is the task content
    task_content = lines[0].strip()
    
    # Rest is the description
    description = '\n'.join(lines[1:]).strip() if len(lines) > 1 else ""
    
    # Create the task using quick_add
    resp = client.add_task_quick(task_content)
    resp = client.update_task(resp.id, description=description)

    print(f"Task created: {resp.content}")
    
finally:
    # Clean up the temporary file
    if os.path.exists(tmp_filename):
        os.unlink(tmp_filename)
