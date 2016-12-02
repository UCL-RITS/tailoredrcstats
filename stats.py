'''
  This module contains routines for generating CSVs of stats for a particular set of
  users and a particular database.
  Owain Kenway
'''

# Constants.
mysqlhost = "mysql.external.legion.ucl.ac.uk"
mysqlport = 3306

# Get usage for list of users from database name db between 
# start and stop.
# if nodes = "*" then all nodes.
def usage(users, db, start, stop, nodes = "*"):
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

    userlist = ""
    for a in users:
        if userlist != "":
            userlist = userlist + ", "
        userlist = userlist + "'" + a + "'"

    # Construct our query.
    query = "select sum((ru_wallclock*cost)) from " + db + ".accounting where ((end_time > unix_timestamp('" + start +  "')) and (end_time < unix_timestamp('" + stop + "')) and owner in (" + userlist + ") " 
    
    # if nodes != * then construct a node list.
    if nodes != "*":
        nodelist = ""
        for a in nodes:
            if nodelist != "":
                nodelist = nodelist + ", "
            nodelist = nodelist + "'" + a + "'"
        query = query + " and where hostname in ('" + nodelist *"')"

    query = query + ");"

    print(query)

    # Set up cursor.
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)

    # Run query.
    cursor.execute(query)

    # Dump output.
    output = cursor.fetchall()

    # Tidy up.
    cursor.close()
    conn.close()

    return output[0]['sum((ru_wallclock*cost))']

# Main so something happens if we run this script directly.    
if __name__ == "__main__":
    print("Testing DB connection")

    u = usage(users = ["uccaoke", "cceahke"], db = "sgelogs2", start = "2015-01-01 00:00:01", stop = "2016-01-01 00:00:00")
    print(u)