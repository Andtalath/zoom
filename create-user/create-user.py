import pprint
from util import (
    get_comma_separated_input,
    get_input_with_default, get_input_with_random_default,
    call_api, get_input_with_none_default, print_header,
    validate_input
)
from colorama import init
init()

def get_user_from_api(username):
    return call_api('GET', f'/users/{username}', {}, None, False)

def user_exists(username):
    response = get_user_from_api(username)
    return response.status_code == 200

def get_user():
    username = None
    while not username:
        username = get_input_with_none_default('ZOOM username (ex test@kth.se)')
    return username

def get_user_info():
    user_info = {}
    user_info['username'] = get_input_with_random_default('ZOOM username (ex test@kth.se)')
    if not user_info['username'].endswith('@kth.se'):
       user_info['username'] = f'{user_info["username"]}@kth.se'
    user_info['first_name'] = get_input_with_random_default('First name')
    user_info['last_name'] = get_input_with_random_default('Last name')
    user_info['department'] = get_input_with_default('Department', 'GVS')
    user_info['vanity_name'] = get_input_with_default('PMI vanity name (5 to 40 chars, only lowercase letters and numbers)', 'new.meeting')
    user_info['vanity_name'] = user_info['vanity_name'].lower().replace(' ', '.')
    user_info['pincode'] = get_input_with_none_default('Pincode (4 digits)')
    user_info['assistants'] = get_comma_separated_input('ZOOM assistants separated by comma (@kth.se emails)')
    return user_info

def create_user(user_info):
    return call_api('POST', '/users', 
        {
            'action': 'custCreate',
            'user_info': {
                'email': user_info['username'],
                'type': '2', # Licensed
                'first_name': user_info['first_name'],
                'last_name': user_info['last_name']
            }
        }
    ).json()

def add_department_and_vanity_name(user_info):
    return call_api('PATCH', f'/users/{user_info["username"]}',
        {
            'dept': user_info['department'],
            'vanity_name': user_info['vanity_name'] 
        }
    , user_info['username'])

def set_user_as_employee(user_info):
    return call_api('POST', '/groups/3-4mcuUrRn2w0Kfba-VxtQ/members',
        {
            'members': [
                {
                    'email': user_info['username']
                }
            ]
        }
    , user_info['username'])

def set_pincode(user_info, created_user):
    if not user_info['pincode']:
        return None
    return call_api('PATCH', f'/meetings/{created_user["pmi"]}',
        {
            'password': user_info['pincode']
        }
    , user_info['username'])

def set_join_before_host_and_topic(user_info, created_user):
    return call_api('PATCH', f'/meetings/{created_user["pmi"]}',
        {
            'settings': {
                'join_before_host': True
            } 
        }
    , user_info['username'])    

def add_assistants(user_info):
    if not user_info['assistants']:
        return None
    assistants = [{'email': ass} for ass in user_info['assistants']]
    return call_api('POST', f'/users/{user_info["username"]}/assistants', 
        {
            'assistants': assistants
        }
    , user_info['username'])

def run():
    validated = False
    user_info = None
    print_header()
    while not validated:
        user_info = get_user_info()
        validated = validate_input(user_info)
    create_user(user_info)
    created_user = get_user_from_api(user_info['username']).json()
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(created_user)
    add_department_and_vanity_name(user_info)
    set_user_as_employee(user_info)
    set_join_before_host_and_topic(user_info, created_user)
    set_pincode(user_info, created_user)
    add_assistants(user_info)

if __name__ == "__main__":
    run()
