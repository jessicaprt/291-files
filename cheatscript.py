""" 
created by: Jessica Prieto
a sample application
i created this to take important notes on embedded SQL
into a python application using cx_Oracle

"""
import cx_Oracle
from pprint import pprint

def oracle_Connect():
    """ establishing a connection """
    auth = open('.info')
    username = auth.readline().strip()
    password = auth.readline().strip()
    connection = cx_Oracle.connect(username, password, "gwynne.cs.ualberta.ca:1521/CRS")
    print("connected")
    return connection

def get_Cursor(con):
    """ getting the cursor from a connection """
    return con.cursor()

def commit_And_Close(con, com):
    """ commiting changes to DB and closing the connection """

    if com == 1:
        con.commit
    
    con.close()

def execute_List(statement, cursor):
    """when query is executed, the result is saved in 
        a list and then the list is printed"""
    print("printing list")
    cursor.execute(statement)
    slist = cursor.fetchall()
    pprint(slist)

def execute_Fetchall(statement,cursor,bindvars=None):
    """executing a query and printing by iterating through fetchall"""
    print("printing fetchall")
    
    if bindvars == None:
        cursor.execute(statement)
    else:
        cursor.execute(statement,bindvars)

    for i in cursor.fetchall():
        print(i)

def execute_Fetchone(statement, cursor):
    """executing a query and printing one by one"""
    print("printing by fetching one each")
    cursor.execute(statement)
    i = cursor.fetchone()
    while i:
        print(i)
        i=cursor.fetchone()

def search(columns, table, variable, cursor):
    """
    searching for a value
    arguments: 
        columns - the desired columns to be returned by the query
        table - the table to search from
              - assumption: user is only searching from one table
        variable - the column to be compared to
        cursor - the current cursor
    """
    string = input("search input: ")
    print("searching")
    statement = "select {0} from {1} where upper({2}) = :1".format(columns, table, variable)
    execute_Fetchall(statement, cursor,(string.upper().ljust(15),)) 

def get_Description(cursor):
    """prints the description from the table that was last executed by the dursor"""
    rows = cursor.description
    for i in rows:
        print(i[0])

if __name__ == "__main__":
    connection = oracle_Connect()
    cursor = get_Cursor(connection)
    
    # just creating some sample table
    rows = [(1, "George"), (2,"Freddy"), (3,"Liza"), (4,"Nicole"), (5,"Danielle"), (6,"Justine"), (7,"Nicolas")]
    cursor.execute("drop table friends")
    cursor.execute("create table friends(id integer, name char(15))")
    print("table created")

    cursor.executemany("insert into friends values (:1,:2)", rows)
    
    statement = "select * from friends"
    execute_List(statement, cursor)
    execute_Fetchall(statement, cursor)
    execute_Fetchone(statement, cursor)

    cols = "*"
    table = "friends"
    variable = "name"
    search(cols, table, variable, cursor)
    
    get_Description
    commit_And_Close(connection, 1)
