from typing import Dict, Any, Optional
import requests
import json
from dataclasses import dataclass

@dataclass
class APIResponse:
    data: Optional[Dict[str, Any]]
    status_code: int
    error: Optional[str] = None

def make_api_request(
    url: str,
    method: str = 'GET',
    headers: Optional[Dict[str, str]] = None,
    data: Optional[Dict[str, Any]] = None,
    api_key: Optional[str] = None
) -> APIResponse:
    """
    Make a REST API request and process the response.
    
    Args:
        url: The API endpoint URL
        method: HTTP method (GET, POST, PUT, DELETE)
        headers: Request headers
        data: Request body data for POST/PUT requests
        api_key: API key for authentication
        
    Returns:
        APIResponse object containing the response data and status
    """
    try:
        # Set default headers if none provided
        headers = headers or {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # Add API key to headers if provided
        if api_key:
            # Eventbrite specific header format
            headers['Authorization'] = f'Bearer {api_key}'
            
        # Make the API request
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=data
        )
        
        # Print request details for debugging
        print(f"Request URL: {url}")
        print(f"Request Headers: {headers}")
        
        # Raise an exception for bad status codes
        response.raise_for_status()
        
        return APIResponse(
            data=response.json(),
            status_code=response.status_code
        )
        
    except requests.exceptions.RequestException as e:
        return APIResponse(
            data=None,
            status_code=getattr(e.response, 'status_code', 500),
            error=str(e)
        )

def process_response(response: APIResponse) -> None:
    """
    Process the API response data.
    
    Args:
        response: APIResponse object containing the response data
    """
    if response.error:
        print(f"Error: {response.error}")
        return
        
    if response.data:
        print(f"Response received successfully! Status code: {response.status_code}")
        print("Response data:")
        print(json.dumps(response.data, indent=2))
    else:
        print("No response data to process")

def main() -> None:
    # Example usage with API key
    api_key = "RCLLC6X4OJC6OK3OHTE7"  # Replace with your actual API key
    base_url = "https://www.eventbriteapi.com/v3"
    org_id = "2650046659981"  # Trybe organization ID
    
    # Make GET request to get organization events
    response = make_api_request(
        url=f"{base_url}/organizations/{org_id}/events",
        api_key=api_key
    )
    process_response(response)
    
    # Example POST request to create an event
    """
    post_data = {
        "event": {
            "name": {
                "html": "Test Event"
            },
            "description": {
                "html": "This is a test event"
            },
            "start": {
                "timezone": "America/Los_Angeles",
                "utc": "2024-12-31T19:00:00Z"
            },
            "end": {
                "timezone": "America/Los_Angeles",
                "utc": "2024-12-31T22:00:00Z"
            },
            "currency": "USD",
            "capacity": 100
        }
    }
    
    post_response = make_api_request(
        url=f"{base_url}/organizations/YOUR_ORG_ID/events",
        method="POST",
        data=post_data,
        api_key=api_key
    )
    process_response(post_response)
    """

if __name__ == "__main__":
    main() 