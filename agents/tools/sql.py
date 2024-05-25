import sqlite3;

from pydantic.v1 import BaseModel
from typing import List

from langchain.tools import Tool;

conn = sqlite3.connect('db.sqlite')

def list_tables():
  c = conn.cursor()
  c.execute("select name from sqlite_master where type='table'")
  rows = c.fetchall()
  return "\n".join(row[0] for row in rows if row[0] is not None)

def run_sqlite_query(query):
  c = conn.cursor()
  try:
    c.execute(query)
    return c.fetchall()
  except sqlite3.OperationalError as err:
    return f"The following error occored {str(err)}"
  
class RunQueryArgsSchema(BaseModel):
  query: str

run_query_tool = Tool.from_function(
  name='run_sqlite_query',
  description='Run a sqlite query.',
  func=run_sqlite_query,
  args_schema=RunQueryArgsSchema
)

def describe_tables(table_names):
  c= conn.cursor()
  tables = ', '.join("'" + table + "'" for table in table_names )
  rows = c.execute(f"select sql from sqlite_master where type='table' and name in ({tables});")
  return '\n'.join(row[0] for row in rows if row[0] is not None)

class DescribeTablesArgSchema(BaseModel):
  table_names: List[str]

describe_tables_tool = Tool.from_function(
  name='describe_tables',
  description='Given the list of table names, returns the schema of the table',
  func=describe_tables,
  args_schema=DescribeTablesArgSchema
)

''' Our Tables 
{
  adresses: {},
  carts: {},
  orders: {},
  products: {},
  users: {},
  order_products: {}
}
'''