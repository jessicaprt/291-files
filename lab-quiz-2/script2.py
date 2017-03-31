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
        con.commit()
    
    con.close()

def execute_category(category, statement,cursor,bindvars=None):
    """executing a query and printing by iterating through fetchall"""
    # print("printing fetchall")
    
    if bindvars == None:
        cursor.execute(statement)
    else:
        cursor.execute(statement,bindvars)

    table_name = category.ljust(30).replace(" ", "_")
    prod = cursor.fetchall()

    drop_table_statement = "drop table {0}".format(table_name)
    cursor.execute("select * from c291.products")
    cols = cursor.description
    print(cols)

    cols_ = ""
    for i in cols:
        cols_ += i[0] + " char(30),"

    table_statement = "create table {0} ({1})".format(table_name, cols_[:-1])

    cursor.execute(drop_table_statement)
    cursor.execute(table_statement)

    #cursor.bindarraysize = len(cols)
    add_statement = "insert into {0} values (:1,:2,:3,:4)".format(table_name)

    for i in prod:
        cursor.execute(add_statement, i)

    cursor.execute("select * from {0}".format(table_name))
    
    for i in cursor.fetchall():
        print(i)


def search(string, columns, table, variable, cursor):
    # print("searching %s" % string.upper().ljust(50))
    statement = "select {0} from {1} where upper({2}) = :1".format(columns, table, variable)
    # print(statement)
    execute_category(string, statement, cursor,(string.upper().ljust(20),)) 

if __name__ == "__main__":
    connection = oracle_Connect()
    cursor = get_Cursor(connection)

    store_address = input("product category:")
    columns = "*"
    table = "c291.products"
    variable = "category"
    search(store_address, columns, table, variable, cursor)

    commit_And_Close(connection, 1)