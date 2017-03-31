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
    
def execute_get_name_address(statement,cursor,bindvars=None):
    """executing a query and printing by iterating through fetchall"""
    # print("printing fetchall")
    
    if bindvars == None:
        cursor.execute(statement)
    else:
        cursor.execute(statement,bindvars)
    print("------------------")

    for i in cursor.fetchall():
        print("Name: %s\nAddress: %s" % (i[0], i[1]))
        print("------------------")

def formatsearch (keyword):
    result = '%{0}%'.format(keyword.upper())
    # print(result)
    return result

def search(string, columns, table, variable, cond, cursor):
    # print("searching %s" % string.upper().ljust(50))
    statement = "select {0} from {1} where upper({2}) like :1 {3}".format(columns, table, variable, cond)
    # print(statement)
    execute_get_name_address(statement, cursor,(formatsearch(string),)) 

if __name__ == "__main__":
    connection = oracle_Connect()
    cursor = get_Cursor(connection)

    store_address = input("enter address:")
    columns = "name, address"
    table = "c291.stores"
    variable = "address"
    cond = "order by name asc"
    search(store_address, columns, table, variable, cond, cursor)

    commit_And_Close(connection, 0)