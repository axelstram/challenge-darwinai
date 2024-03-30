from ..src.db_manager import DatabaseManager
from ..models.user import User
from ..models.expenses import Expense
import pytest
import psycopg2


def value_is_present_in_query_result(value, l):
    return len(list(filter(lambda x: x.count(value) > 0, l))) == 1


def test_that_when_db_is_created_the_two_tables_exist():
    db = DatabaseManager()
    db.create_tables()

    query= """SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'"""

    table_names = db.execute_query(query)
    table_names_set = set()

    for table_name in table_names:
        table_names_set.add(table_name[0])    

    assert "users" in table_names_set
    assert "expenses" in table_names_set

    db.delete_tables()

def test_that_tables_are_deleted_correctly():
    db = DatabaseManager()
    db.delete_tables()

    query = """SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'"""

    table_names = db.execute_query(query)

    assert len(table_names) == 0


def test_that_user_is_correctly_added_to_the_users_table():
    db = DatabaseManager()
    db.delete_tables()
    db.create_tables()

    user1 = User(123)
    user2 = User(456)
    user3 = User(999)
    
    db.insert_user(user1)
    db.insert_user(user2)

    assert db.user_is_present(user1)
    assert db.user_is_present(user2)
    assert not db.user_is_present(user3)

    db.delete_tables()


def test_that_expenses_are_correctly_inserted_for_a_user():
    db = DatabaseManager()
    db.delete_tables()
    db.create_tables()


    user = User(telegram_id=123)
    db.insert_user(user)

    expense1 = Expense(user_telegram_id=user.get_telegram_id(), description="burguer", amount=20, category="Food")
    expense2 = Expense(user_telegram_id=user.get_telegram_id(), description="notebook", amount=13230, category="Utilities")
    db.insert_expenses(expense1)
    db.insert_expenses(expense2)


    expenses = db.get_expenses_from_user(user)

    assert len(expenses) == 2
    assert value_is_present_in_query_result('notebook', expenses)
    assert value_is_present_in_query_result('burguer', expenses)

    db.delete_tables()



def test_that_when_an_expense_is_added_for_a_non_existent_user_then_it_fails():
    db = DatabaseManager()
    db.delete_tables()
    db.create_tables()

    expense = Expense(user_telegram_id=444, description="burguer", amount=20, category="Food")
    
    assert db.insert_expenses(expense) == False

    db.delete_tables()