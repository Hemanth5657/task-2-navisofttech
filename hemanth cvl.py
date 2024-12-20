import click

@click.group
def mycommands():
    pass

@click.command()
@click.option("--name", prompt="Enter the name", help="The name of the user")
def hello(name):
    click.echo(f"Hello {name}!")

PRIORITIES = {
    "O": "options",
    "l": "Low",
    "m": "Medium",
    "h": "High",
    "c": "crucial",
}

@click.command()
@click.argument("priority", type=click.Choice(PRIORITIES.keys()), default="m")  # Fixed: click.Choice
@click.argument("todofile", type=click.Path(exists=False), required=False)
@click.option("-n", "--name", prompt="Enter the todo name", help="The name of the todo item")
@click.option("--desc", prompt="Describe the todo name", help="The description of the todo item")
def add_todo(name, description, priority, todofile):
    filename = todofile if todofile is not None else "mytodos.txt"
    with open(filename, "a+") as f:
        f.write(f"{name}: {description} [Priority: {PRIORITIES[priority]}]\n")

@click.command()
@click.argument("idx", type=int, required=True)
@click.argument("todofile", type=click.Path(exists=True), required=False)
def delete_todo(idx, todofile):
    filename = todofile if todofile is not None else "mytodos.txt"
    with open(filename, "r") as f:
        todo_list = f.read().splitlines()
        if idx < len(todo_list):
            todo_list.pop(idx)
            with open(filename, "w") as f:
                f.write("\n".join(todo_list) + "\n")
        else:
            click.echo(f"Invalid index {idx}")

@click.command()
@click.option("-p", "--priority", type=click.Choice(PRIORITIES.keys()), required=False)  # Fixed: click.Choice
@click.argument("todofile", type=click.Path(exists=True), required=False)
def list_todos(priority, todofile):
    filename = todofile if todofile is not None else "mytodos.txt"
    with open(filename, "r") as f:
        todo_list = f.read().splitlines()
    if priority is None:
        for idx, todo in enumerate(todo_list):
            click.echo(f"({idx}) - {todo}")
    else:
        for idx, todo in enumerate(todo_list):
            if f"[Priority: {PRIORITIES[priority]}]" in todo:
                click.echo(f"({idx}) - {todo}")

mycommands.add_command(hello)
mycommands.add_command(add_todo)
mycommands.add_command(delete_todo)
mycommands.add_command(list_todos)

if __name__ == "__main__":
    mycommands()
