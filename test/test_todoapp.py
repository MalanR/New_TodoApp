import asyncio
import pytest
from src.todoapp import TodoApp  # Adjust the import based on your directory structure

@pytest.mark.asyncio
async def test_create_task():
    app = TodoApp.new()
    title = 'Test List'
    description = 'Task 1'
    task = await app.create(title, description)
    task_id = list(task.keys())[0]
    
    assert task_id in app.todo_list[title]
    assert app.todo_list[title][task_id]['description'] == description
    assert app.todo_list[title][task_id]['is_completed'] == False
    assert app.todo_list[title][task_id]['completed_on'] == None

@pytest.mark.asyncio
async def test_delete_task():
    app = TodoApp.new()
    title = 'Test List'
    task = await app.create(title, 'Task to delete')
    task_id = list(task.keys())[0]
    
    result = await app.delete(title, task_id)
    assert result == f"Task {task_id} deleted"
    assert task_id not in app.todo_list[title]

@pytest.mark.asyncio
async def test_update_task():
    app = TodoApp.new()
    title = 'Test List'
    task = await app.create(title, 'Task to update')
    task_id = list(task.keys())[0]
    new_description = 'Updated Task'
    
    result = await app.update(title, task_id, new_description)
    assert result == f"Task {task_id} updated with '{new_description}'"
    assert app.todo_list[title][task_id]['description'] == new_description

@pytest.mark.asyncio
async def test_complete_task():
    app = TodoApp.new()
    title = 'Test List'
    task = await app.create(title, 'Task to complete')
    task_id = list(task.keys())[0]
    
    result = await app.complete(title, task_id)
    assert result == f"Task {task_id} completed."
    assert app.todo_list[title][task_id]['is_completed'] == True
    assert app.todo_list[title][task_id]['completed_on'] is not None

@pytest.mark.asyncio
async def test_filter_completed_tasks():
    app = TodoApp.new()
    title = 'Test List'
    await app.create(title, 'Task 1')
    task2 = await app.create(title, 'Task 2')
    task2_id = list(task2.keys())[0]
    await app.complete(title, task2_id)
    
    completed_tasks = await app.filter_tasks(title, 'completed')
    assert len(completed_tasks) == 1
    assert task2_id in completed_tasks
    assert completed_tasks[task2_id]['is_completed'] == True

@pytest.mark.asyncio
async def test_filter_todo_tasks():
    app = TodoApp.new()
    title = 'Test List'
    task1 = await app.create(title, 'Task 1')
    task1_id = list(task1.keys())[0]
    await app.create(title, 'Task 2')
    
    todo_tasks = await app.filter_tasks(title, 'todo')
    assert len(todo_tasks) == 2
    assert task1_id in todo_tasks
    assert todo_tasks[task1_id]['is_completed'] == False

@pytest.mark.asyncio
async def test_filter_tasks_by_description():
    app = TodoApp.new()
    title = 'Test List'
    task1 = await app.create(title, 'Task 1')
    task1_id = list(task1.keys())[0]
    task2 = await app.create(title, 'Another task')
    
    filtered_tasks = await app.filter_tasks(title, 'Task')
    assert len(filtered_tasks) == 1
    assert task1_id in filtered_tasks
    assert list(task2.keys())[0] not in filtered_tasks

@pytest.mark.asyncio
async def test_create_multiple_titles():
    app = TodoApp.new()
    title1 = 'Work'
    title2 = 'Personal'
    task1 = await app.create(title1, 'Work task 1')
    task2 = await app.create(title2, 'Personal task 1')
    
    assert list(task1.keys())[0] in app.todo_list[title1]
    assert list(task2.keys())[0] in app.todo_list[title2]

@pytest.mark.asyncio
async def test_delete_non_existent_task():
    app = TodoApp.new()
    title = 'Test List'
    await app.create(title, 'Task 1')
    
    result = await app.delete(title, 'non-existent-id')
    assert result == 'Task non-existent-id not found'

@pytest.mark.asyncio
async def test_update_non_existent_task():
    app = TodoApp.new()
    title = 'Test List'
    await app.create(title, 'Task 1')
    
    result = await app.update(title, 'non-existent-id', 'New Description')
    assert result == 'Task non-existent-id not found'

@pytest.mark.asyncio
async def test_complete_non_existent_task():
    app = TodoApp.new()
    title = 'Test List'
    await app.create(title, 'Task 1')
    
    result = await app.complete(title, 'non-existent-id')
    assert result == 'Task non-existent-id not found'

if __name__ == "__main__":
    pytest.main()
