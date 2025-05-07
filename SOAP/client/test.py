from zeep import Client
from zeep.exceptions import TransportError
import json

WSDL_URL = 'http://127.0.0.1:8000/?wsdl'

def test_soap_operations():
    # Initialize SOAP client
    client = Client(WSDL_URL)

    # CREATE - Test user creation
    print("\n=== Testing CREATE ===")
    create_response = client.service.create_user(
        name='SOAP Test User',
        email='soap@test.com',
        password='soap123'
    )
    print("Create Response:", {
        'id': create_response.id,
        'name': create_response.name,
        'email': create_response.email
    })

    # READ - Test getting all users
    print("\n=== Testing GET All ===")
    users = client.service.get_users()
    users_list = [{
        'id': user.id,
        'name': user.name,
        'email': user.email
    } for user in users]
    print("All Users:", json.dumps(users_list, indent=2))

if __name__ == "__main__":
    try:
        test_soap_operations()
    except TransportError:
        print("Error: Could not connect to SOAP server. Make sure it's running on port 8000")
    except Exception as e:
        print(f"Error: {str(e)}")