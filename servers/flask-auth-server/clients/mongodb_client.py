import requests
import json

class MongoDBClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    def _send_request(self, method, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"
        headers = {"Content-Type": "application/json"}
        try:
            if method == "POST":
                response = requests.post(url, headers=headers, data=json.dumps(data))
            elif method == "GET":
                response = requests.get(url, headers=headers, params=data)
            elif method == "PUT":
                response = requests.put(url, headers=headers, data=json.dumps(data))
            elif method == "DELETE":
                response = requests.delete(url, headers=headers, params=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during request to {url}: {e}")
            return {"error": str(e)}

    def insert_one(self, collection_name, document):
        return self._send_request("POST", f"insert/{collection_name}", document)

    def find_one(self, collection_name, query):
        return self._send_request("GET", f"find_one/{collection_name}", query)

    def update_one(self, collection_name, query, new_values):
        data = {"query": query, "new_values": new_values}
        return self._send_request("PUT", f"update/{collection_name}", data)

    def delete_one(self, collection_name, query):
        return self._send_request("DELETE", f"delete/{collection_name}", query)

if __name__ == "__main__":
    # This is a simple example of how to use the client.
    # In a real scenario, you would have the MongoDB MCP server running.
    client = MongoDBClient(base_url="http://localhost:8000") # Replace with your MCP server URL

    # Example: Insert a document
    print("Inserting document...")
    insert_result = client.insert_one("mycollection", {"name": "Test User", "age": 30})
    print(f"Insert Result: {insert_result}")

    # Example: Find a document
    print("\nFinding document...")
    find_result = client.find_one("mycollection", {"name": "Test User"})
    print(f"Find Result: {find_result}")

    # Example: Update a document
    if find_result and not find_result.get("error"):
        print("\nUpdating document...")
        update_result = client.update_one("mycollection", {"name": "Test User"}, {"$set": {"age": 31}})
        print(f"Update Result: {update_result}")

        # Verify update
        print("\nVerifying update...")
        verify_result = client.find_one("mycollection", {"name": "Test User"})
        print(f"Verify Result: {verify_result}")

    # Example: Delete a document
    print("\nDeleting document...")
    delete_result = client.delete_one("mycollection", {"name": "Test User"})
    print(f"Delete Result: {delete_result}")

    # Verify deletion
    print("\nVerifying deletion...")
    verify_delete_result = client.find_one("mycollection", {"name": "Test User"})
    print(f"Verify Delete Result: {verify_delete_result}")