'''
  This module contains routines for generating CSVs of stats for a particular set of
  users and a particular database.
  Owain Kenway
'''

# Constants.
mysqlhost = "mysql.external.legion.ucl.ac.uk"
mysqlport = 3306

# Get usage for list of users from database name db on nodes list nodes between 00:00:00 on start and
# 23:59:59 on end.
def usage(users, db, nodes, start, stop):
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

# Main so something happens if we run this script directly.    
if __name__ == "__main__":
    print("Testing DB connection")
    usage(["uccaoke"], "sgelogs", "test", 1,1)