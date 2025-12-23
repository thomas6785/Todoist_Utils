from todoist_api_python.api import TodoistAPI
import os
import sys
import tempfile
import subprocess

key_path = os.path.expanduser("~/todoist_utils/api_key")
with open(key_path, encoding="utf8") as f:
    api_key = f.read().strip()

client = TodoistAPI(api_key)

# Check if a task ID was provided
task_id = sys.argv[1] if len(sys.argv) > 1 else None
edit_mode = task_id is not None

# Create a temporary file
with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp_file:
    tmp_filename = tmp_file.name
    
    # If editing an existing task, pre-populate with task content and description
    if edit_mode:
        try:
            task = client.get_task(task_id=task_id)
            # First line is the task content
            tmp_file.write(task.content + "\n")
            # Rest is the description
            if task.description:
                tmp_file.write(task.description)
            print(f"Editing task: {task.content}")
        except Exception as e:
            print(f"Error retrieving task: {e}")
            sys.exit(1)

try:
    # Open Vim to edit the temporary file
    subprocess.call(['vim', tmp_filename])
    
    # Read the contents after Vim closes
    with open(tmp_filename, 'r', encoding='utf8') as f:
        content = f.read()
    
    if edit_mode:
        # Update the existing task's content and description
        lines = content.strip().split('\n')
        
        if not lines or not lines[0].strip():
            print("Error: No task content provided")
            sys.exit(1)
        
        # First line is the task content
        task_content = lines[0].strip()
        
        # Rest is the description
        description = '\n'.join(lines[1:]).strip() if len(lines) > 1 else ""
        
        resp = client.update_task(task_id=task_id, content=task_content, description=description)
        print(f"Task updated: {resp.content}")
        if description:
            print(f"Description set: {len(description)} characters")
    else:
        # Create a new task
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
        resp = client.add_task(content=task_content, description=description)
        
        print(f"Task created: {resp.content}")
        if description:
            print(f"Description set: {len(description)} characters")
    
finally:
    # Clean up the temporary file
    if os.path.exists(tmp_filename):
        os.unlink(tmp_filename)
