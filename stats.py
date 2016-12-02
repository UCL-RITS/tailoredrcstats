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

    print(">>> DEBUG SQL query: " + query)

    # Run query.
    cursor.execute(query)

    # Dump output.
    output = cursor.fetchall()

    # Tidy up.
    cursor.close()
    conn.close()

    return output

# Build owner/node limit string for queries
def onlimits(users="*", nodes="*"):
    query = ""

    # if users != * then construct a node list.
    if users != "*":
        userlist = sqllist(users)
        query = query + " and owner in " + userlist

    # if nodes != * then construct a node list.
    if nodes != "*":
        nodelist = sqllist(nodes)
        query = query + " and where hostname in " + nodelist

    return query

# Get usage for list of users from database name db between 
# start and stop.
# if nodes = "*" then all nodes.
def usage(db, start, stop, users="*", nodes = "*"):

    # Construct our query.
    query = "select sum((ru_wallclock*cost)) from " + db + ".accounting where ((end_time > unix_timestamp('" + start +  "')) and (end_time < unix_timestamp('" + stop + "')) " + onlimits(users=users, nodes=nodes) + ");"

    # Dump output.
    output = dbquery(db=db, query=query)

    return output[0]["sum((ru_wallclock*cost))"]

# Get active users for list of users from database name db between 
# start and stop.
# if nodes = "*" then all nodes.
def activeusers(db, start, stop, users = "*", nodes = "*"):

    # Construct our query.
    query = "select owner from " + db + ".accounting where ((end_time > unix_timestamp('" + start +  "')) and (end_time < unix_timestamp('" + stop + "')) " + onlimits(users=users, nodes=nodes) + ");"

    # Dump output.
    output = dbquery(db=db, query=query)

    active = set()
    for a in output:
        active.add(a["owner"])
    return list(active)

# Main so something happens if we run this script directly.    
if __name__ == "__main__":

    import argparse

    # Some default values
    prefix="test_"
    users = "*"
    db = "sgelogs2"
    nodes = "*"
    start = "2015-01-01 00:00:01"
    stop = "2016-01-01 00:00:00"

    parser = argparse.ArgumentParser(description="Generate usage reports.")
    parser.add_argument('-u', metavar='user list', type=str, help="File containing list of users")
    parser.add_argument('-n', metavar='node list', type=str, help="File containing list of nodes")
    parser.add_argument('-d', metavar='database', type=str, help="DB name")
    parser.add_argument('-b', metavar='start date', type=str, help="Start date [YYYY-MM-DD hh:mm:ss]")
    parser.add_argument('-e', metavar='end date', type=str, help="End date [YYYY-MM-DD hh:mm:ss]")
    parser.add_argument('-p', metavar='prefix', type=str, help="Prefix for report files")

    options = parser.parse_args()

    if (options.u != None):
        users = open(options.u).read().splitlines()

    if (options.n != None):
        nodes = open(options.n).read().splitlines()

    if (options.d != None):
        db = options.d

    if (options.b != None):
        start = options.b

    if (options.e != None):
        stop = options.e

    if (options.p != None):
        prefix = options.p

    u = usage(users = users, db = db, start = start, stop = stop)
    nu = activeusers(users = users, db = db, start = start, stop = stop)
    print(u)
    print(nu)