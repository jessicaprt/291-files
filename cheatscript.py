import cx_Oracle
from pprint import pprint

def oracle_Connect():
    auth = open('.info')
    username = auth.readline().strip()
    password = auth.readline().strip()
    connection = cx_Oracle.connect(username, password, "gwynne.cs.ualberta.ca:1521/CRS")
    print("connected")
    return connection

def get_Cursor(con):    
    return con.cursor()

def commit_And_Close(con):
    con.commit
    con.close()

def execute_List(statement, cursor):
    print("printing list")
    cursor.execute(statement)
    slist = cursor.fetchall()
    pprint(slist)

def execute_Fetchall(statement,cursor,bindvars=None):
    print("printing fetchall")
    
    if bindvars == None:
        cursor.execute(statement)
    else:
        cursor.execute(statement,bindvars)

    for i in cursor.fetchall():
        print(i)

def execute_Fetchone(statement, cursor):
    print("printing by fetching one each")
    cursor.execute(statement)
    i = cursor.fetchone()
    while i:
        print(i)
        i=cursor.fetchone()

def search(rows, table, variable, cursor):
    string = input("search input: ")
    print("searching")
    statement = "select {0} from {1} where upper({2}) = :1".format(rows, table, variable)
    execute_Fetchall(statement, cursor,(string.upper().ljust(15),)) 

def get_Description(cursor):
    rows = cursor.description
    for i in rows:
        print(i[0])

if __name__ == "__main__":
    connection = oracle_Connect()
    cursor = get_Cursor(connection)

    rows = [(1, "George"), (2,"Freddy"), (3,"Liza"), (4,"Nicole"), (5,"Danielle"), (6,"Justine"), (7,"Nicolas")]
    
    cursor.execute("drop table friends")
    cursor.execute("create table friends(id integer, name char(15))")
    print("table created")

    cursor.executemany("insert into friends values (:1,:2)", rows)
    
    statement = "select * from friends"
    execute_List(statement, cursor)
    execute_Fetchall(statement, cursor)
    execute_Fetchone(statement, cursor)

    rows = "*"
    table = "friends"
    variable = "name"
    search(rows, table, variable, cursor)
    
    #to get and print the fow based on the last executed querys
    get_Description
    commit_And_Close(connection)
