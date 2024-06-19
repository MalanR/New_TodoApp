import json
import os

def read_file(self):
    for filename in os.listdir():
        if filename.endswith('.json'):
            with open(filename, 'r') as file:
                todo_list = json.load(file)
                self.todos.append(todo_list)
    print(f"Loaded {len(self.todos)} todo lists from files")


def save_JSON(self, todo_list):
    filename = f"{todo_list['title'].replace(' ','_')}_{len(self.todo_list)}.json"
    with open(filename, 'w') as file:
        json.dump(todo_list, file, indent=4)
    print(f"TodoList '{todo_list['title']}' saved to  {filename}.")