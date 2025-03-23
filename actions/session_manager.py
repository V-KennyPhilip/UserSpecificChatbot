# import requests
# import logging
# from typing import Dict, Optional

# # Configure logger
# logger = logging.getLogger(__name__)

# class SessionManager:
#     """
#     Manages authentication and session with the backend service.
#     Implements a singleton pattern to ensure single session across actions.
#     """
#     _instance = None
    
#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super(SessionManager, cls).__new__(cls)
#             cls._instance.session = requests.Session()
#             cls._instance.base_url = "http://localhost:8080/api"
#             cls._instance.is_authenticated = False
#             cls._instance.response_cache = {}  # Cache for API responses
#             cls._instance.cache_timeout = 300  # Cache timeout in seconds (5 minutes)
#             cls._instance.cache_timestamp = {}  # Timestamp for cached responses
#         return cls._instance
    
#     def login(self, email: str = "john.doe@example.com", password: str = "John@pwd") -> bool:
#         """
#         Authenticates with the backend service.
#         Returns True if authentication was successful, False otherwise.
#         """
#         try:
#             login_url = f"{self.base_url}/login"
#             payload = {
#                 "email": email,
#                 "password": password
#             }
            
#             response = self.session.post(login_url, json=payload)
            
#             if response.status_code == 200:
#                 logger.info("Authentication successful")
#                 self.is_authenticated = True
#                 return True
#             else:
#                 logger.error(f"Authentication failed: {response.status_code}, {response.text}")
#                 self.is_authenticated = False
#                 return False
#         except Exception as e:
#             logger.error(f"Error during authentication: {str(e)}")
#             self.is_authenticated = False
#             return False
    
#     def ensure_authenticated(self) -> bool:
#         """
#         Ensures that the session is authenticated.
#         Returns True if already authenticated or if authentication is successful.
#         """
#         if not self.is_authenticated:
#             return self.login()
#         return True
    
#     def make_api_request(self, endpoint: str, method: str = "get", 
#                          params: Optional[Dict] = None, 
#                          json_data: Optional[Dict] = None,
#                          use_cache: bool = True) -> Optional[Dict]:
#         """
#         Makes an API request to the backend service.
#         Ensures authentication before making the request.
        
#         Args:
#             endpoint: API endpoint path
#             method: HTTP method (get, post, put, delete)
#             params: URL parameters
#             json_data: JSON data for request body
#             use_cache: Whether to use cached response if available
            
#         Returns:
#             Response data as dictionary or None if request failed
#         """
#         import time
        
#         # Only cache GET requests
#         can_use_cache = use_cache and method.lower() == "get"
        
#         # Create a cache key based on endpoint and parameters
#         cache_key = None
#         if can_use_cache:
#             param_str = str(params) if params else ""
#             cache_key = f"{endpoint}:{param_str}"
            
#             # Check if we have a cached response
#             if cache_key in self.response_cache:
#                 # Check if the cache is still valid
#                 now = time.time()
#                 timestamp = self.cache_timestamp.get(cache_key, 0)
#                 if now - timestamp < self.cache_timeout:
#                     logger.info(f"Using cached response for {endpoint}")
#                     return self.response_cache[cache_key]
        
#         # If not using cache or no valid cache, proceed with API request
#         if not self.ensure_authenticated():
#             logger.error("Cannot make API request: Authentication failed")
#             return None
        
#         try:
#             url = f"{self.base_url}/{endpoint}"
#             logger.debug(f"Making {method.upper()} request to {url}")
            
#             if method.lower() == "get":
#                 response = self.session.get(url, params=params, timeout=5)  # Added timeout to prevent long waits
#             elif method.lower() == "post":
#                 response = self.session.post(url, json=json_data, params=params, timeout=5)
#             elif method.lower() == "put":
#                 response = self.session.put(url, json=json_data, params=params, timeout=5)
#             elif method.lower() == "delete":
#                 response = self.session.delete(url, params=params, timeout=5)
#             else:
#                 logger.error(f"Unsupported HTTP method: {method}")
#                 return None
            
#             if response.status_code >= 200 and response.status_code < 300:
#                 result = response.json()
                
#                 # Cache the result if using GET
#                 if can_use_cache and cache_key:
#                     self.response_cache[cache_key] = result
#                     self.cache_timestamp[cache_key] = time.time()
#                     logger.debug(f"Cached response for {endpoint}")
                
#                 return result
#             else:
#                 logger.error(f"API request failed: {response.status_code}, {response.text}")
#                 return None
#         except requests.exceptions.Timeout:
#             logger.error(f"Request timeout for {endpoint}")
#             return None
#         except Exception as e:
#             logger.error(f"Error making API request: {str(e)}")
#             return None
            
#     def get_user_bot_response(self, prompt_id: int, additional: Optional[str] = None) -> Optional[str]:
#         """
#         Gets a response from the userbot API endpoint.
        
#         Args:
#             prompt_id: The prompt ID based on intent
#             additional: Additional parameter (like loan_id or bank_id)
            
#         Returns:
#             Response text or None if request failed
#         """
#         params = {"prompt_id": prompt_id}
#         if additional:
#             params["additional"] = additional
            
#         response_data = self.make_api_request("userbot/query", params=params)
        
#         if response_data and "data" in response_data:
#             # Handle structured response format
#             data = response_data["data"]
#             if isinstance(data, dict):
#                 # Extract and format the response text based on the expected structure
#                 if "responseText" in data:
#                     # If there's extraAction data, include it in the response
#                     result_text = data["responseText"]
                    
#                     # Check if there's extra profile data to include
#                     if "extraAction" in data and data["extraAction"]:
#                         extra = data["extraAction"]
#                         if isinstance(extra, dict):
#                             # Format profile information
#                             result_text += "\n\n**Your Profile Details**\n\n"
#                             for key, value in extra.items():
#                                 label = key.capitalize()
#                                 if key == "email":
#                                     label = "Email"
#                                 elif key == "phone":
#                                     label = "Phone Number"
#                                 result_text += f"**{label}:** {value}\n"
                    
#                     return result_text
#                 return str(data)  # Fallback to string conversion if no responseText
#             return str(data)  # Convert to string if not a dict but some other type
#         return None
# session_manager.py
import requests
import logging
import json
from typing import Dict, Any, Optional

# Configure logger
logger = logging.getLogger(__name__)

# Map prompt IDs to their corresponding HTTP methods
PROMPT_ID_TO_HTTP_METHOD = {
    # GET requests
    4: "GET",   # ACC_PROFILE
    5: "GET",   # ACC_KYC
    6: "GET",   # ACC_CIBIL
    8: "GET",   # ACC_VIEW_SALARY
    13: "GET",  # LOAN_ACTIVE_NUMBER
    14: "GET",  # LOAN_ACTIVE_DETAILS
    15: "GET",  # LOAN_EMI_DETAILS
    16: "GET",  # LOAN_STATUS
    17: "GET",  # BANK_LINKED_NUMBER
    18: "GET",  # BANK_LINKED_DETAILS
    
    # PUT requests
    10: "PUT",  # ACC_UPDATE_SALARY
    12: "PUT",  # ACC_CONTACT
    19: "PUT",  # BANK_UPDATE
    
    # POST requests
    20: "POST"  # BANK_ADD
}

class SessionManager:
    """
    Manages API interactions with the Spring Boot backend, including authentication
    """
    
    # Class-level storage for session cookies to maintain login state across instances
    _cookies = {}
    _authenticated = False
    
    # Hardcoded credentials
    _email = "john.doe@example.com"
    _password = "John@pwd"
    
    # This variable will ensure we only try to auto-initialize once
    _initialization_attempted = False
    
    @classmethod
    def login(cls, email: str = None, password: str = None) -> bool:
        """
        Performs login and stores the JWT token from the HttpOnly cookie
        Uses hardcoded credentials if none provided
        """
        base_url = "http://localhost:8080"
        headers = {"Content-Type": "application/json"}
        endpoint = "/api/login"
        
        # Use provided credentials or fallback to hardcoded ones
        email = email or cls._email
        password = password or cls._password
        
        payload = {"email": email, "password": password}
        
        try:
            logger.info(f"Attempting login with email: {email}")
            response = requests.post(
                f"{base_url}{endpoint}",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                # The token is in HttpOnly cookie, store all cookies from the response
                cls._cookies = dict(response.cookies)
                cls._authenticated = True
                logger.info(f"Login successful for user: {email}")
                return True
            else:
                logger.error(f"Login failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error during login: {str(e)}")
            return False
    
    # Static initialization - will be called when this module is imported
    @classmethod
    def initialize(cls):
        """
        Initializes the session by logging in with hardcoded credentials
        """
        if not cls._initialization_attempted:
            cls._initialization_attempted = True
            logger.info("Attempting automatic login on startup...")
            return cls.login()
        return cls._authenticated
    
    def __init__(self):
        self.base_url = "http://localhost:8080"
        self.headers = {
            "Content-Type": "application/json"
        }
        
        # Ensure we're authenticated when an instance is created
        if not SessionManager._authenticated:
            SessionManager.initialize()
    
    def get_user_bot_response(self, prompt_id: int, additional_param: Optional[str] = None) -> Dict[str, Any]:
        """
        Gets response from backend based on prompt ID using the appropriate HTTP method
        """
        # If not authenticated, try to authenticate first
        if not SessionManager._authenticated:
            logger.info("Not authenticated, attempting login...")
            SessionManager.initialize()
            
            if not SessionManager._authenticated:
                logger.error("Authentication failed - could not log in with hardcoded credentials.")
                return {"error": "Authentication required"}
            
        endpoint = "/api/userbot/query"
        
        # Add parameters to the request
        params = {"prompt_id": prompt_id}
        if additional_param:
            params["additional"] = additional_param
        
        # Determine the appropriate HTTP method for this prompt ID
        http_method = PROMPT_ID_TO_HTTP_METHOD.get(prompt_id, "GET")
        logger.info(f"Using {http_method} request for prompt ID {prompt_id}")
        
        try:
            # For POST/PUT requests, we'll put the parameters in the JSON body instead
            if http_method in ["POST", "PUT"]:
                # Prepare the payload based on the prompt_id and additional_param
                payload = {"prompt_id": prompt_id}
                if additional_param:
                    payload["additional"] = additional_param
                
                # Make the request with appropriate method
                if http_method == "POST":
                    response = requests.post(
                        f"{self.base_url}{endpoint}",
                        headers=self.headers,
                        json=payload,
                        cookies=SessionManager._cookies
                    )
                else:  # PUT
                    response = requests.put(
                        f"{self.base_url}{endpoint}",
                        headers=self.headers,
                        json=payload,
                        cookies=SessionManager._cookies
                    )
            else:  # GET
                response = requests.get(
                    f"{self.base_url}{endpoint}",
                    headers=self.headers,
                    params=params,
                    cookies=SessionManager._cookies
                )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Successful API response for prompt ID {prompt_id}")
                
                # Extract loan IDs or bank IDs from responses if available
                if prompt_id == 13 and 'data' in data and 'extraAction' in data['data']:
                    logger.info("Extracted loan information from response")
                
                if prompt_id == 17 and 'data' in data and 'extraAction' in data['data']:
                    logger.info("Extracted bank information from response")
                
                return data.get("data", {})
            elif response.status_code == 403 or response.status_code == 401:
                logger.error("Authentication error: Token expired or invalid")
                # Try to re-authenticate
                SessionManager._authenticated = False
                SessionManager.initialize()
                # If re-authentication worked, retry the request recursively
                if SessionManager._authenticated:
                    logger.info("Re-authentication successful, retrying request")
                    return self.get_user_bot_response(prompt_id, additional_param)
                return {"error": "Authentication expired and re-authentication failed"}
            else:
                logger.error(f"API error: {response.status_code} - {response.text}")
                return {"error": f"API error: {response.status_code}"}
                
        except Exception as e:
            logger.error(f"Error connecting to backend: {str(e)}")
            return {"error": str(e)}

# Automatically try to log in when this module is imported
SessionManager.initialize()