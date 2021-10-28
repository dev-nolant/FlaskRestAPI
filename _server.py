from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import os

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

'''
Changes working directory to current path execution
directory to avoid errors with Pandas.
'''
os.chdir(os.path.dirname(os.path.abspath(__file__)))
'''
The main 'Users' class deals with everything that has to deal with users.
 - Account Diction
 - Account Creation
 - Account Management
 - Account Deletion
'''
#----------------------------------------------------------------


class Users(Resource):
    '''
    Post to create a new user account.
    '''
    def post(self):
        '''

        '''
        parser.add_argument('userId', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('city', required=True)
        args = parser.parse_args()
        data = pd.read_csv('db/users.csv')

        if args['userId'] in list(data['userId']):
            return {
                'message':
                f"'{args['userId']}' already exists."
            }, 401

        else:
            new_dataframe = pd.DataFrame({
                'userId':
                args['userId'],
                'name':
                args['name'],
                'city':
                args['city'],
                'locations': [[]]
                })

            data = data.append(new_dataframe, ignore_index=True)
            data = data.to_csv('db/users.csv', index=False)
            return{
                'data':
                "Added user: %s" % args['userId']
            }, 200
    pass
    '''
    Get to dictate all of the users in users.csv.
    '''
    def get(self):
        '''
        Get to display all users.
        '''
        data = pd.read_csv('db/users.csv')
        data = data.to_dict()
        return {
            'data':
            data
        }, 200

    pass
    '''
    Put to modify data, in this case only location.
    '''
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required=True)
        parser.add_argument('location', required=True)
        args = parser.parse_args()

        data = pd.read_csv('db/users.csv')

        if args['userId'] in list(data['userId']):
            data['locations'] = data['locations'].apply(
                lambda x:
                ast.literal_eval(x)
            )

            user_data = data[data['userId'] == args['userId']]

            user_data['locations'] == user_data['locations'].values[0]\
                .append(args['location'])

            data.to_csv('db/users.csv', index=False)
            return{
                'data':
                "Added location: %s" % args['location']
            }, 200
        else:
            return{
                'message':
                f"'{args['userId']} : user not found'"
            }, 404
    '''
    Delete to delete a user from users.csv.
    '''
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required=True)
        parser.add_argument('adminId', required=True)
        args = parser.parse_args()

        admin_data = pd.read_csv('db/admins.csv')
        data = pd.read_csv('db/users.csv')

        if args['userId'] in list(data['userId']):
            if args['adminId'] in list(admin_data['adminId']):
                mdata = data[
                    ~data['userId'].str.contains(args['userId'], na=False)]
                mdata.to_csv('db/users.csv', index=False)
                return{
                    'data':
                    "Removed User: %s" % args['userId']
                }, 200
            else:
                return{
                    'message':
                    f"'{args['adminId'] } ': Not Authorized"
                }, 401
        else:
            return{
                'message':
                f"'{args['userId']}': Not Found"
            }, 404

'''
The main locations class is simply to
display the locations.csv upon get request.
'''
#----------------------------------------------------------------


class Locations(Resource):
    '''
    Get to display all of the csv locations.
    '''
    def get(self):
        '''
        Get to display all ove the csv locations.
        '''
        data = pd.read_csv('db/locations.csv')
        data = data.to_dict()
        return {
            'data':
            data
        }, 200

    pass

'''
Add new endpoints that point to our new classes above.
 - Will add to 'api', which is declaired above as the app.
'''
api.add_resource(
    Users, '/users'
)
api.add_resource(
    Locations, '/locations'
)


#----------------------------------------------------------------
'''
If the file is being ran as the main application, it will execute.
 - It will not autorun as a module/import.
'''
if __name__ == '__main__':
    app.run(debug='True')
# run our Flask app
