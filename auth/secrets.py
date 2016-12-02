# This class lets us keep the user ids and passwords outside of the git repo.
# This is basically a port of the equivalent I added to Bruno's old stats code.
# Owain Kenway

class Secrets:
    def __init__(self):
        import configparser
        from os.path import expanduser

        filename = expanduser("~") + "/.stats_secrets/accounts"

        secretconfig = configparser.ConfigParser()
        secretconfig.read(filename)

        self.dbuser = secretconfig.get("database", "user").strip("'")
        self.dbpasswd = secretconfig.get("database", "pass").strip("")

        self.ldapuser = secretconfig.get("ldap", "user").strip("'")
        self.ldappasswd = secretconfig.get("ldap", "pass").strip("'")