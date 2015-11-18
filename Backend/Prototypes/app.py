from flask import Flask, redirect, url_for
from flask_restful import reqparse, abort, Api, Resource
from flask_httpauth import HTTPBasicAuth
import ConfigParser
import MySQLdb
import datetime
import os


application = Flask(__name__)
auth = HTTPBasicAuth()
api = Api(application)


config = ConfigParser.ConfigParser()
configdir = os.path.dirname(os.path.realpath(__file__))
configpath = os.path.join(configdir, "config", "configAPI.ini")
config.read(configpath)


# Pull settings from the MySQL section of config file
sql_config = {
  'user': config.get('MySQL', 'user'),
  'passwd': config.get('MySQL', 'password'),
  'host': config.get('MySQL', 'host'),
  'db': config.get('MySQL', 'database'),
}

class User(Resource):
    def get(self, username):
        query = "SELECT tablename from userDB WHERE username='%s'" % username
        result = performQueryRaw(query)
        if result == []:
            return "No user with this username"
        else:
            print(result)
            return {'username': username, 'tables': result[0]['tablename']}

table = config.get("MySQL", 'table')

# Arguments will be field: the name of the field to pull (specify field multiple times to pull multiple fields)
# Start and end, the start and end dates. Results will be in the form of
# a list of all times and fields (in a dict) that fall between the start and end date
# Times and fields will be expressed as Strings
# Sample call: /get_field?field=temp&start=%222014-10-06_06:27:29%22&end=%222015-12-22_14:04:29%22
# Sample call (pulling multiple fields): /get_field?field=s1&field=s2&start=%222014-10-06_06:27:29%22&end=%222015-12-22_14:04:29%22
class GetField(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('field', required=True, action='append')
        self.parser.add_argument('start', required=True)
        self.parser.add_argument('end', required=True)
        super(GetField, self).__init__()

    def validate(self, args):
        fields_valid = validateFields (args['field'])
        dates_valid = validateDates ([args['start'], args['end']])
        message = ""
        message += "" if fields_valid else "Invalid fields. "
        message += "" if dates_valid else "Invalid dates."
        return (fields_valid and dates_valid, message)

    def get(self, username, table):
        # Parse arguments
        args = self.parser.parse_args()

        valid = self.validate(args)
        if not valid[0]:
            abort(400, message=valid[1])
        # Form query using the received arguments
        query = ("SELECT time, {} FROM {} where time BETWEEN {} and {}".format(",".join(args['field']), table, args['start'], args['end']))
        # Print for debugging
        print query

        # Perform the query and store result
        result = performQuery (query)
        print result

        return result


# Given any number of fields, a start date and an end date, returns the average of each field
# between the start and end date.
# Example call: /get_average?field=temp&start=%222014-10-06_06:27:29%22&end=%222015-12-22_14:04:29%22
class GetAvg(Resource):

    def __init__(self):
        # Set up the RequestParser
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('field', required=True, action='append')
        self.parser.add_argument('start', required=True)
        self.parser.add_argument('end', required=True)
        super(GetAvg, self).__init__()

    def validate(self, args):
        # Make sure the request is valid
        # Requests are valid if the fields exist in the db and the times are valid times
        fields_valid = validateFields (args['field'])
        dates_valid = validateDates ([args['start'], args['end']])
        message = ""
        message += "" if fields_valid else "Invalid fields. "
        message += "" if dates_valid else "Invalid dates."
        return (fields_valid and dates_valid, message)

    @auth.login_required
    def get(self, username, table):
        # Parse arguments
        args = self.parser.parse_args()

        # If the request is invalid, abort
        valid = self.validate(args)
        if not valid[0]:
            abort(400, message=valid[1])

        # Form query using the received arguments, in this case putting field arguments in the AVG function
        fields = map (lambda s: "AVG({0}) as {0}".format(s), args['field'])
        query = ("SELECT {} FROM {} where time BETWEEN {} and {}".format(",".join(fields), table, args['start'], args['end']))
        # Print for debugging
        print query

        # Perform the query and store result
        result = performQueryRaw (query)
        # Convert from strings into doubles
        for row in result:
            for key in row:
                row[key] = float(row[key])

        print result

        return result

#Authentication Functions, first hardcoded later DB interacted
@auth.get_password
def get_pw(username):
    #if username in users :
    #   return users.get(username)
        
    userQry = performQueryRaw("SELECT password FROM userDB WHERE username='%s'" % username);
    if not userQry :
        return None
        
    return userQry[0]["password"]
        
# @app.route('/')
# @auth.login_required
# def index():
#   return "All Hail %s!" % (auth.username())

class Welcome(Resource):
    @auth.login_required
    def get(self):
        return "All Hail %s!" % (auth.username())
    
#for hashing if/when deemed neccessary
#@auth.hash_password
#def hash_pw (username, password) :
#   get_salt(username)
#   return hash(password,salt)
#
#   OR
#
#@auth.verify_password
#def verify_pw(username, password) :
#   return ourVerificationFunction(usr,pw)

def performQuery (query):
    """Perform query and convert results into JSONable objects

    Arguments:
    query - A string containing a valid MySQL query

    Performs the query given in the string query. Converts all of the results of the query into objects that
    can be converted to JSON.
    """

    results = performQueryRaw (query)
    # Transform values from weird MySQL types into JSONable types
    for row in results:
        for key in row:
            # Map datatype to conversion function. If datatype unknown, convert to string
            functs = {"TIMESTAMP": str, "INT": int, "DOUBLE":float, None: str}
            # Try to determine data type
            key_type = None
            try: 
                key_type = config.get('fields', key).upper()
            except:
                key_type = None 
            # Apply conversion function
            row[key] = (functs[key_type])(row[key])

    return results


def performQueryRaw (query):
    """Perform query and return raw results

    Arguments:
    query - A string containing a valid MySQL query

    Performs the query given in the string query. Results may be in MySQL types that will fail to convert
    to JSON.
    """

    # Connect to db
    conn = MySQLdb.connect(**sql_config)
    cursor = conn.cursor()
    # Perform query and fetch results
    cursor.execute(query)
    result = cursor.fetchall()
    # Make a list of the fields that were queried
    columns = [column[0] for column in cursor.description]
    results = []

    # Transform the results from a list of tuples to a list of dicts
    for row in result:
        results.append(dict(zip(columns, row)))

    # Clean up and return
    cursor.close( )
    conn.close( )
    return results

def validateFields (fields):
    for field in fields:
        if field.lower() not in [x.lower() for x in config.options("fields")]:
            return False
    return True

def validateDates (dates):
    for d in dates:
        if d.startswith('"') and d.endswith('"'):
            d = d[1:-1]
        try:
            datetime.datetime.strptime(d, '%Y-%m-%d_%H:%M:%S')
        except ValueError as e:
            print e
            return False
    return True

## Actually setup the Api resource routing here
api.add_resource(Welcome, '/')
api.add_resource(GetField, '/users/<string:username>/mygarden/<string:table>/get_field')
api.add_resource(GetAvg, '/users/<string:username>/mygarden/<string:table>/get_average')
api.add_resource(User, '/users/<string:username>/mygarden')


if __name__ == '__main__':
    application.run(debug=True)
