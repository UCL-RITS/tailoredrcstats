'''
  This module contains routines for generating CSVs of stats for a particular set of
  users and a particular database.
  Owain Kenway
'''

# Generate a valid SQL list from a python one.
def sqllist(pylist):
    sqlstr="("
    for a in pylist:
        if sqlstr!= "(":
            sqlstr = sqlstr + ", "
        sqlstr = sqlstr + "'" + a + "'"
    sqlstr = sqlstr + ")"
    return sqlstr

# Perform an SQL query on a particular DB and return results.
def dbquery(db, query, mysqlhost="mysql.external.legion.ucl.ac.uk", mysqlport = 3306 ):
    from auth.secrets import Secrets
    import MySQLdb   # Note need mysql connector > 2.0

    # Set up our authentication.
    s = Secrets()

    # Connect to database.
    conn = MySQLdb.Connect(host=mysqlhost,
                           port=mysqlport,
                           user=s.dbuser,
                           passwd=s.dbpasswd,
                           db=db)

    # Set up cursor.
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)

    # Run query.
    cursor.execute(query)

    # Dump output.
    output = cursor.fetchall()

    # Tidy up.
    cursor.close()
    conn.close()

    return output

# Get usage for list of users from database name db between 
# start and stop.
# if nodes = "*" then all nodes.
def usage(users, db, start, stop, nodes = "*"):
    userlist = sqllist(users)

    # Construct our query.
    query = "select sum((ru_wallclock*cost)) from " + db + ".accounting where ((end_time > unix_timestamp('" + start +  "')) and (end_time < unix_timestamp('" + stop + "')) and owner in " + userlist
    
    # if nodes != * then construct a node list.
    if nodes != "*":
        nodelist = sqllist(nodes)
        query = query + " and where hostname in " + nodelist + ")"

    query = query + ");"

    print(query)

    # Dump output.
    output = dbquery(db=db, query=query)

    return output[0]['sum((ru_wallclock*cost))']

# Main so something happens if we run this script directly.    
if __name__ == "__main__":
    print("Testing DB connection")

    u = usage(users = ["uccaoke", "cceahke"], db = "sgelogs2", start = "2015-01-01 00:00:01", stop = "2016-01-01 00:00:00")
    print(u)