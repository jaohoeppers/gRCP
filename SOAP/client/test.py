from zeep import Client
from zeep.exceptions import TransportError
import json
import uuid

WSDL_URL = 'http://127.0.0.1:8000/?wsdl'

def test_soap_operations():
    # Initialize SOAP client
    client = Client(WSDL_URL)
    created_user_id = None

    try:
        # CREATE - Test user creation
        print("\n=== Testing CREATE ===")
        create_response = client.service.create_user(
            name='SOAP Test User',
            email=f'soap_{uuid.uuid4().hex[:8]}@test.com',
            password='soap123'
        )
        created_user_id = create_response.id
        print("Created User:", {
            'id': create_response.id,
            'name': create_response.name,
            'email': create_response.email
        })

        # READ ALL - Test getting all users
        print("\n=== Testing READ ALL ===")
        users = client.service.get_users()
        users_list = [{
            'id': user.id,
            'name': user.name,
            'email': user.email
        } for user in users]
        print("All Users:", json.dumps(users_list, indent=2))

        # READ ONE - Test getting user by ID
        print("\n=== Testing READ ONE ===")
        user = client.service.get_user_by_id(created_user_id)
        print("Found User:", {
            'id': user.id,
            'name': user.name,
            'email': user.email
        })

        # UPDATE - Test updating user
        print("\n=== Testing UPDATE ===")
        updated_user = client.service.update_user(
            user_id=created_user_id,
            name='Updated SOAP User',
            email='updated_soap@test.com',
            password='updated123'
        )
        print("Updated User:", {
            'id': updated_user.id,
            'name': updated_user.name,
            'email': updated_user.email
        })

        # DELETE - Test deleting user
        print("\n=== Testing DELETE ===")
        delete_response = client.service.delete_user(created_user_id)
        print("Delete Response:", delete_response)

        # Verify deletion
        print("\n=== Verifying Deletion ===")
        try:
            client.service.get_user_by_id(created_user_id)
            print("Error: User still exists!")
        except Exception as e:
            print("Success: User was deleted")

    except TransportError:
        print("Error: Could not connect to SOAP server. Make sure it's running on port 8000")
    except Exception as e:
        print(f"Error during operation: {str(e)}")
    finally:
        if created_user_id:
            try:
                client.service.delete_user(created_user_id)
            except:
                pass

def main():
    print("Starting SOAP Client Tests...")
    print("Connecting to:", WSDL_URL)
    test_soap_operations()
    print("\nTests completed.")

if __name__ == "__main__":
    main()