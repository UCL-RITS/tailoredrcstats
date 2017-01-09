'''
  This module contains routines for generating CSVs of stats for a particular set of
  users and a particular database.
  Owain Kenway
'''

# Generate a valid SQL list from a python one.
def sqllist(pylist):
    sqlstr="("
    if type(pylist) == str:
        sqlstr = sqlstr + "'" + pylist + "')"
    else:
        for a in pylist:
            if sqlstr!= "(":
                sqlstr = sqlstr + ", "
            sqlstr = sqlstr + "'" + a + "'"
        sqlstr = sqlstr + ")"
    return sqlstr

# Perform an SQL query on a particular DB and return results.
def dbquery(db, query, mysqlhost="mysql.external.legion.ucl.ac.uk", mysqlport = 3306 ):
    from auth.secrets import Secrets
    import MySQLdb   # Note need mysqlclient package from pypi

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
        query = query + " and hostname in " + nodelist

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

# Report on active users, monthly, in range start - stop.
def activeuserreport(db, start, stop, users = "*", nodes = "*", filename="active_users.csv"):
    dates = gendates(start,stop)

    f = open(filename, "w")
    f.write("Period, Active users from subset, Total active users\n")

    for a in dates:
        print("User report for " + date2str(a["start"]) + " ... " + date2str(a["stop"]))
        period = str(a["start"].year) + "-" + str(a["start"].month)
        num = len(activeusers(db, date2str(a["start"]), date2str(a["stop"]), users=users, nodes=nodes))
        tnum = len(activeusers(db, date2str(a["start"]), date2str(a["stop"]), users="*", nodes=nodes))
        f.write(period + "," + str(num) + "," + str(tnum) + "\n")

    f.close()

# Report on total usage for each user in time period.
def peruserreport(db, start, stop, users = "*", nodes = "*", filename="peruser_usage.csv"):

    f = open(filename, "w")
    f.write("User id, Total usage in compute seconds between " + start + " and " + stop + "\n")

    for a in users:
        u = usage(db = db, start = start, stop = stop, users = a, nodes=nodes)
        if type(u) == type(None):
            u = 0
        f.write(a + "," + str(u) + "\n")

    f.close()

# Report on active users, monthly, in range start - stop.
def usagereport(db, start, stop, users = "*", nodes = "*", filename="usage.csv"):
    dates = gendates(start,stop)

    f = open(filename, "w")
    f.write("Period, Usage by subset of users, Total usage\n")

    for a in dates:
        print("Usage report for " + date2str(a["start"]) + " ... " + date2str(a["stop"]))
        period = str(a["start"].year) + "-" + str(a["start"].month)
        su = usage(db, date2str(a["start"]), date2str(a["stop"]), users=users, nodes=nodes)
        u = usage(db, date2str(a["start"]), date2str(a["stop"]), users="*", nodes=nodes)
        if type(su) == type(None):
            su = 0
        if type(u) == type(None):
            u = 0
        f.write(period + "," + str(su) + "," + str(u) + "\n")

    f.close()

# Break down of usage by department.
# This gets departments from the user_depts table.
def deptreports(db, start, stop, filename="depreport.csv"):

    query = "select user_info.user_depts.department,sum((ru_wallclock*cost)) from " + db + ".accounting inner join user_info.user_depts on "
    query = query + db + ".accounting.owner=user_info.user_depts.username where ((end_time > unix_timestamp('" + start + "')) " 
    query = query + "and (end_time < unix_timestamp('" + stop + "'))) group by user_info.user_depts.department;"

    results = dbquery(db = db, query = query)

    f = open(filename, "w")
    f.write("Department, usage (s)\n")
    for i in results:
        f.write(i['department'] + "," + str(i['sum((ru_wallclock*cost))']) + "\n")

    f.close()

# Generate date ranges:
def gendates(start, stop):
    import dateutil
    from dateutil.parser import parse
    import datetime

    ret = []

    # convert to datetime so that we can do date math.
    dtstart = dateutil.parser.parse(start)
    dtstop = dateutil.parser.parse(stop)

    # Right - this is where the old stats code went terribly wrong.
    # In this code, start is an absolute value.
    # AS IS STOP.
    # We need to generate fractional months for first and last month.

    currentdate = dtstart
    while monthincflat(currentdate) < dtstop:
        qdatestart = currentdate
        qdateend = monthincflat(currentdate)
        if qdateend == flatmonth(dtstop):
            qdateend = dtstop
        dr = dict()
        dr["start"] = qdatestart
        dr["stop"] = qdateend
        ret.append(dr)
        currentdate = monthincflat(currentdate)

    return ret

# Increment dates by a month.
def monthinc(date):
    import datetime

    newyear = date.year
    newmonth = date.month + 1
    if newmonth == 13:
        newyear = newyear + 1
        newmonth = 1

    return datetime.datetime(newyear, newmonth, date.day, date.hour, date.minute, date.second)

def monthincflat(date):
    import datetime
    return monthinc(datetime.datetime(date.year, date.month, 1,0,0,0))
    
def flatmonth(date):
    import datetime
    return datetime.datetime(date.year, date.month, 1,0,0,0)

def date2str(date):
    import datetime

    f = "%Y-%m-%d %H:%M:%S"
    return date.strftime(f) 

# Main so something happens if we run this script directly.    
if __name__ == "__main__":

    import argparse

    # Some default values
    prefix="test"
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
    parser.add_argument('-t', action='store_true', help="Do a quick test run instead of a report.")
    parser.add_argument('-r', action='store_true', help="Do a per user usage report instead of normal report.")
    parser.add_argument('-x', action='store_true', help="Departmental report.")

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

    if (options.t):
        u = usage(users = users, db = db, start = start, stop = stop, nodes = nodes)
        nu = activeusers(users = users, db = db, start = start, stop = stop, nodes = nodes)
        print(u)
        print(nu)
    elif (options.r):
        peruserreport(db = db, start = start, stop = stop, users = users, nodes = nodes, filename=prefix+"_peruser_usage.csv")
    elif (options.x):
        deptreports(db = db, start = start, stop = stop, filename = prefix+'_depreport.csv')
    else: 
        activeuserreport(users = users, db = db, start = start, stop = stop, filename=prefix+"_active_users.csv", nodes = nodes)
        usagereport(users = users, db = db, start = start, stop = stop, filename=prefix+"_usage.csv", nodes = nodes)
