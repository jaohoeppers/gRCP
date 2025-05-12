import requests
import json
import uuid

BASE_URL = 'http://127.0.0.1:5000'

def test_crud_operations():
    created_id = None
    
    try:
        # CREATE - Create new items
        print("\n=== Testing CREATE ===")
        create_response1 = requests.post(
            f'{BASE_URL}/item', 
            json={
                'name': 'Item 1',
                'email': f'user_{uuid.uuid4().hex[:8]}@test.com',
                'password': 'test123'
            }
        )
        print(f"Creating Item 1: {create_response1.json()}")
        created_id = create_response1.json().get('id')
        
        create_response2 = requests.post(
            f'{BASE_URL}/item', 
            json={
                'name': 'Item 2',
                'email': f'user_{uuid.uuid4().hex[:8]}@test.com',
                'password': 'test456'
            }
        )
        print(f"Creating Item 2: {create_response2.json()}")

        # READ ALL - List all items
        print("\n=== Testing READ ALL ===")
        read_all_response = requests.get(f'{BASE_URL}/items')
        print(f"All items: {json.dumps(read_all_response.json(), indent=2)}")

        # READ ONE - Get item by ID
        if created_id:
            print(f"\n=== Testing READ ONE (ID: {created_id}) ===")
            read_one_response = requests.get(f'{BASE_URL}/item/{created_id}')
            print(f"Found item: {json.dumps(read_one_response.json(), indent=2)}")

        # UPDATE - Update an item
        if created_id:
            print(f"\n=== Testing UPDATE (ID: {created_id}) ===")
            update_response = requests.put(
                f'{BASE_URL}/item/{created_id}',
                json={
                    'name': 'Updated Item',
                    'email': 'updated@test.com',
                    'password': 'updated123'
                }
            )
            print(f"Updated item: {json.dumps(update_response.json(), indent=2)}")

        # DELETE - Delete an item
        if created_id:
            print(f"\n=== Testing DELETE (ID: {created_id}) ===")
            delete_response = requests.delete(f'{BASE_URL}/item/{created_id}')
            print(f"Delete response: {json.dumps(delete_response.json(), indent=2)}")

            # Verify deletion
            print("\n=== Verifying Deletion ===")
            verify_response = requests.get(f'{BASE_URL}/item/{created_id}')
            if verify_response.status_code == 404:
                print("Success: Item was deleted")
            else:
                print("Error: Item still exists!")

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server. Make sure it's running on port 5000")
    except Exception as e:
        print(f"Error during operations: {str(e)}")
    finally:
        if created_id:
            try:
                requests.delete(f'{BASE_URL}/item/{created_id}')
            except:
                pass

def main():
    print("Starting REST Client Tests...")
    print(f"Connecting to: {BASE_URL}")
    test_crud_operations()
    print("\nTests completed.")

if __name__ == "__main__":
    main()