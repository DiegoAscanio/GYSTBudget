import typer
from GYSTBudgetCLI import add, delete, export

app = typer.Typer()
app.add_typer(add.app, name='add')
app.add_typer(delete.app, name='delete')
app.add_typer(export.app, name='export')
