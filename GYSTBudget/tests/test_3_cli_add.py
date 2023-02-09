import subprocess
import sys
import typer.core
import pdb
import pytest
from typer.testing import CliRunner

from GYSTBudgetCLI import main

app = main.app
runner = CliRunner()

def test_add_origin():
    result = runner.invoke(app, ['add', 'origin', 'Banco do Brasil'])
    assert result.exit_code == 0
    assert '\'Banco do Brasil\'' in result.output

def test_add_repeated_origin():
    result = runner.invoke(app, ['add', 'origin', 'Banco do Brasil'])
    assert result.exit_code == 1
    assert result.output == 'Error while adding Banco do Brasil:\nIntegrityError(\'(sqlite3.IntegrityError) UNIQUE constraint failed: origin.name\')\n'

def test_add_category():
    result = runner.invoke(app, ['add', 'category', 'Infraestrutura'])
    result = runner.invoke(app, ['add', 'category', 'Serviços'])
    assert result.exit_code == 0
    assert 'name=\'Serviços\'' in result.output
def test_add_repeated_category():
    result = runner.invoke(app, ['add', 'category', 'Serviços'])
    assert result.exit_code == 1
    assert result.output == 'Error while adding Serviços:\nIntegrityError(\'(sqlite3.IntegrityError) UNIQUE constraint failed: category.name\')\n'

@pytest.mark.skip('Budget is ready, but it won\'t be available until next release')
def test_add_budget():
    result = runner.invoke(app, ['add', 'budget', 'Orçamento Fevereiro'])
    assert result.exit_code == 0
    assert '\'Orçamento Fevereiro\'' in result.output

@pytest.mark.skip('Budget is ready, but it won\'t be available until next release')
def test_add_repeated_budget():
    result = runner.invoke(app, ['add', 'budget', 'Orçamento Fevereiro'])
    assert result.exit_code == 1
    assert result.output == 'Error while adding Orçamento Fevereiro:\nIntegrityError(\'(sqlite3.IntegrityError) UNIQUE constraint failed: budget.title\')\n'


@pytest.mark.skip('Budget is ready, but it won\'t be available until next release')
def test_add_budget_with_date():
    result = runner.invoke(app, ['add', 'budget', '--date', '2023-01-01', 'Orçamento Março'])
    assert result.exit_code == 0
    assert '\'Orçamento Março\'' in result.output

def test_add_budget_with_category():
    result = runner.invoke(app, ['add', 'budget', '--category', 'Serviços,234.48', '--category', 'Infraestrutura,434.44', 'Orçamento Abril'])

@pytest.mark.skip()
def test_add_transaction():
    result = runner.invoke(app, ['add', 'transaction', 'Transação Teste', '44.25'])
    assert result.exit_code == 0
    assert '\'Transação Teste\'' in result.output

@pytest.mark.skip()
def test_add_repeated_transaction():
    result = runner.invoke(app, ['add', 'transaction', 'Transação Teste', '44.25'])
    assert result.exit_code == 0
    assert '\'Transação Teste\'' in result.output

def test_add_expense_transaction_with_date():
    result = runner.invoke(app, ['add', 'transaction', '--date', '2023-02-08', 'Transação com Data', '44.25'])
    assert result.exit_code == 0
    assert '\'Transação com Data\'' in result.output

def test_add_income_trasanction_with_date():
    result = runner.invoke(app, ['add', 'transaction', '-i', '--date', '2023-02-08', 'Transação Income com Data', '44.25'])
    assert result.exit_code == 0
    assert '\'Transação Income com Data\'' in result.output
