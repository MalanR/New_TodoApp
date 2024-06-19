import asyncio
import uuid
import datetime
from fileHandeling import read_file , save_JSON

# TODO: go through the functions again and look for ways to make it simpler, and more effiecient.



class TodoApp:
    def __init__(self):
        self.todo_list = {}

    @staticmethod
    def new():
        return TodoApp()

    async def create(self, title, description):
        task_id = str(uuid.uuid4())[:10]
        todo_task = {
            'description': description,
            'created_on': datetime.datetime.now().strftime("%d %H:%M:%S"),
            'completed_on': None,
            'is_completed': False
        }
        if title not in self.todo_list:
            self.todo_list[title] = {}
            
        self.todo_list[title][task_id] = todo_task
        save_JSON(self, {'title': title, 'tasks': self.todo_list[title]})
        return {task_id: todo_task}
    

    async def delete(self, title , task_id):
        if title in self.todo_list and task_id in self.todo_list[title]:
            del self.todo_list[title][task_id]
            save_JSON(self, {'title': title, 'tasks': self.todo_list[title]})
            return f"Task {task_id} deleted"
        else:
            return f"Task {task_id} not found"
        
        
        

    async def update(self, task_id, title,  description):
        if title in self.todo_list and task_id in self.todo_list[title]:
            self.todo_list[title][task_id]['description'] = description
            save_JSON(self, {'title': title, 'tasks': self.todo_list[title]})
            return f"Task {task_id} updated with '{description}'"
        else:
            return f"Task {task_id} not found"
        
        
        
        

    async def complete(self, title, task_id):
        if title in self.todo_list and task_id in self.todo_list[title]:
            self.todo_list[title][task_id]['completed_on'] = datetime.datetime.now().strftime("%d %H:%M:%S")
            self.todo_list[title][task_id]['is_completed'] = True
            save_JSON(self, {'title': title, 'tasks': self.todo_list[title]})
            return f"Task {task_id} completed."
        else:
            return f"Task {task_id} not found"
        
        
        
        
        
        
    async def filter_tasks(self, title, criteria):
        if title not in self.todo_list:
            return {}
        
        if criteria == 'completed':
            return {task_id: task for task_id, task in self.todo_list[title].items() if task['is_completed']}
        elif criteria == 'todo':
            return {task_id: task for task_id, task in self.todo_list[title].items() if not task['is_completed']}
        else:
            return {task_id: task for task_id, task in self.todo_list[title].items() if criteria.lower() in task['description'].lower()}
        

async def main():
    app = TodoApp.new()
    
    task1 = await app.create('Shopping List', 'Buy milk')
    print(task1)
    
    task2 = await app.create('Shopping List', 'Buy eggs')
    print(task2)
    
    task3 = await app.create('Today\'s Goals', 'Finish report')
    print(task3)
    
    task2_id = list(task2.keys())[0]
    delete_task = await app.delete('Shopping List', task2_id)
    print(delete_task)
    
    task1_id = list(task1.keys())[0]
    update_task = await app.update('Shopping List', task1_id, 'Buy almond milk')
    print(update_task)
    
    task3_id = list(task3.keys())[0]
    complete_task = await app.complete('Today\'s Goals', task3_id)
    print(complete_task)
    
    # Call filter_tasks to filter and print completed tasks
    completed_tasks = await app.filter_tasks('Today\'s Goals', 'completed')
    print("Completed tasks in Today's Goals:")
    for task_id, task_details in completed_tasks.items():
        print(f"{task_id}: {task_details}")
    
    # Call filter_tasks to filter and print todo tasks
    todo_tasks = await app.filter_tasks('Shopping List', 'todo')
    print("Todo tasks in Shopping List:")
    for task_id, task_details in todo_tasks.items():
        print(f"{task_id}: {task_details}")
    
    # Call filter_tasks to filter and print tasks containing the word 'Task'
    filtered_tasks = await app.filter_tasks('Shopping List', 'milk')
    print("Filtered tasks in Shopping List (containing 'milk'):")
    for task_id, task_details in filtered_tasks.items():
        print(f"{task_id}: {task_details}")
    
    print("All tasks in Shopping List:")
    for task_id, task_details in app.todo_list['Shopping List'].items():
        print(f"{task_id}: {task_details}")

if __name__ == "__main__":
    asyncio.run(main())