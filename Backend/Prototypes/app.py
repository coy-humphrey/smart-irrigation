from flask import Flask, redirect, url_for
from flask_restful import reqparse, abort, Api, Resource
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import ConfigParser
import MySQLdb
import datetime
import os


application = Flask(__name__)
auth = HTTPBasicAuth()
api = Api(application)

config = ConfigParser.RawConfigParser()
config.read('config')
#config = ConfigParser.ConfigParser()
#configdir = os.path.dirname(os.path.realpath(__file__))
#configpath = os.path.join(configdir, "config", "configAPI.ini")
#config.read(configpath)

# Pull settings from the MySQL section of config file
sql_config = {
  'user': config.get('MySQL', 'user'),
  'passwd': config.get('MySQL', 'password'),
  'host': config.get('MySQL', 'host'),
  'db': config.get('MySQL', 'database'),
}

# Basic test to see if authentication is working
class Welcome(Resource):
    decorators = [auth.login_required]
    def get(self):
        return "All Hail %s!" % (auth.username())

# Arguments will be field: the name of the field to pull (specify field multiple times to pull multiple fields)
# Start and end, the start and end dates. Results will be in the form of
# a list of all times and fields (in a dict) that fall between the start and end date
# Times and fields will be expressed as Strings
# Sample call: /get_field?field=temp&start=%222014-10-06_06:27:29%22&end=%222015-12-22_14:04:29%22
# Sample call (pulling multiple fields): /get_field?table=entry&field=s1&field=s2&start=%222014-10-06_06:27:29%22&end=%222015-12-22_14:04:29%22
class GetFieldBetweenTime(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('field', required=True, action='append')
        self.parser.add_argument('start', required=True)
        self.parser.add_argument('end', required=True)
        self.parser.add_argument('table', required=True)
        super(GetFieldBetweenTime, self).__init__()

    def validate(self, args):
        fields_valid = validateFields (args['field'])
        dates_valid = validateDates ([args['start'], args['end']])
        message = ""
        message += "" if fields_valid else "Invalid fields. "
        message += "" if dates_valid else "Invalid dates."
        return (fields_valid and dates_valid, message)

    def get(self):
        # Parse arguments
        args = self.parser.parse_args()

        valid = self.validate(args)
        if not valid[0]:
            abort(400, message=valid[1])
        # Form query using the received arguments
        query = ("SELECT time, {} FROM {} where time BETWEEN {} and {}".format(",".join(args['field']), args['table'], args['start'], args['end']))
        # Print for debugging
        print query

        # Perform the query and store result
        result = performQuery (query)
        print result

        return result

# Arguments will be field: the name of the field to pull (specify field multiple times to pull multiple fields)
# Start and end, the start and end values. Results will be in the form of
# a list of all times and fields (in a dict) that fall between the start and end key
# Keys and fields will be expressed as Strings
# Sample call: /get_field_between_key?field=s1&field=s2&start=80&end=120&table=entry&key=temp
# Sample call (pulling multiple fields): /get_field_between_key?field=s1&field=s2&field=s2&start=80&end=120&table=entry&key=temp
class GetFieldBetweenKey(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('field', required=True, action='append')
        self.parser.add_argument('start', required=True)
        self.parser.add_argument('end', required=True)
        self.parser.add_argument('key', required=True)
        self.parser.add_argument('table', required=True)
        super(GetFieldBetweenKey, self).__init__()

    def validate(self, args):
        fields_valid = validateFields (args['field'])
        key_valid = validateKey (args['key'])
        message = ""
        message += "" if fields_valid else "Invalid fields. "
        message += "" if key_valid else "Invalid key. "
        return (fields_valid and key_valid, message)

    def get(self):
        # Parse arguments
        args = self.parser.parse_args()

        valid = self.validate(args)
        if not valid[0]:
            abort(400, message=valid[1])
        # Form query using the received arguments
        query = ("SELECT {}, {} FROM {} where {} BETWEEN {} and {}".format(args['key'], ",".join(args['field']), args['table'], args['key'], args['start'], args['end']))
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
    decorators = [auth.login_required]

    def __init__(self):
        # Set up the RequestParser
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('field', required=True, action='append')
        self.parser.add_argument('start', required=True)
        self.parser.add_argument('end', required=True)
        self.parser.add_argument('table', required=True)
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

    def get(self):
        # Parse arguments
        args = self.parser.parse_args()

        # If the request is invalid, abort
        valid = self.validate(args)
        if not valid[0]:
            abort(400, message=valid[1])

        # Form query using the received arguments, in this case putting field arguments in the AVG function
        fields = map (lambda s: "AVG({0}) as {0}".format(s), args['field'])
        query = ("SELECT {} FROM {} where time BETWEEN {} and {}".format(",".join(fields), args['table'], args['start'], args['end']))
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

class PostWatering(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        # Set up the RequestParser
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('start', required=True)
        self.parser.add_argument('duration', type=int, required=True)
        self.parser.add_argument('gal_per_min', type=float, required=True)
        self.parser.add_argument('table', required=True)
        super(PostWatering, self).__init__()

    def post(self):
        args = self.parser.parse_args()

        #TODO: Validation
        d = args['start']

        if d.startswith('"') and d.endswith('"'):
            d = d[1:-1]

        start = datetime.datetime.strptime(d, '%Y-%m-%d_%H:%M:%S')
        entry_dict = {"start": start.strftime('"%Y-%m-%d %H:%M:%S"'), "duration_minutes": args['duration'], "gal_per_minute": args['gal_per_min']}

        add_entry = ("INSERT INTO watering_entries "
                    "(start, duration_minutes, gal_per_minute) "
                    "VALUES (%(start)s, %(duration_minutes)s, %(gal_per_minute)s)") % entry_dict

        commitQuery (add_entry)

        end = start + datetime.timedelta(minutes=args['duration'])

        query = ("SELECT * FROM {} where time BETWEEN {} and {}".format(args['table'], start.strftime('"%Y-%m-%d %H:%M:%S"'), end.strftime('"%Y-%m-%d %H:%M:%S"')))
        return performQuery(query)



#Authentication Functions, first hardcoded later DB interacted
def get_pw(username):
        
    userQry = performQueryRaw("SELECT password FROM userDB WHERE username='%s'" % username);
    if not userQry :
        return ""
        
    return userQry[0]["password"]
        
 #flask function to verify pw.
@auth.verify_password
def verify_pw(username, password):
    return check_pw(username, password)

#hashes a password for storage using SHA1 + salt
def hashed_pw(password) :
    return generate_password_hash(password)

#user Werkzeug function to check unhashed password against hashed.
def check_pw(username, password) :
    return check_password_hash(get_pw(username), password)

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

def commitQuery (query):
    # Connect to db
    conn = MySQLdb.connect(**sql_config)
    cursor = conn.cursor()
    # Perform query and fetch results
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

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

def validateKey (key):
    if key.lower() not in [x.lower() for x in config.options("fields")]:
        return False
    return True

## Actually setup the Api resource routing here
api.add_resource(Welcome, '/')

api.add_resource(GetFieldBetweenTime, '/get_field', '/get_field_between_time')
api.add_resource(GetAvg, '/get_average')
api.add_resource(GetFieldBetweenKey, '/get_field_between_key')
api.add_resource(PostWatering, '/post_watering')



if __name__ == '__main__':
    application.run(debug=True)