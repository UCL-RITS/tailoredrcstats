# Tool for generating tailored stats reports from Legion/Grace accounting database.
Scripts for generating data on Legion/Grace usage for specific paying users, e.g. the FARR

Needs a plain text list of users and a plain text list of nodes.

## Usage

```
$ python3 stats.py --help                                                                                                                
usage: stats.py [-h] [-u user list] [-n node list] [-d database]                                                                                                               
                [-b start date] [-e end date] [-p prefix] [-t]                                                                                                                 
                                                                                                                                                                               
Generate usage reports.                                                                                                                                                        
                                                                                                                                                                               
optional arguments:                                                                                                                                                            
  -h, --help     show this help message and exit                                                                                                                               
  -u user list   File containing list of users                                                                                                                                 
  -n node list   File containing list of nodes                                                                                                                                 
  -d database    DB name                                                                                                                                                       
  -b start date  Start date [YYYY-MM-DD hh:mm:ss]                                                                                                                              
  -e end date    End date [YYYY-MM-DD hh:mm:ss]                                                                                                                                
  -p prefix      Prefix for report files                                                                                                                                       
  -t             Do a quick test run instead of a report.      
```
