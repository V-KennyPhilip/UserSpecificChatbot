#!/usr/bin/env python
"""
A script to test backend connectivity and diagnose connection issues.
This checks authentication, API endpoints, and diagnoses common problems.
"""

import requests
import sys
import logging
import json
import time
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("connection_tester")

# Backend details
BASE_URL = "http://localhost:8080/api"
LOGIN_URL = f"{BASE_URL}/login"
TEST_ENDPOINTS = [
    "userbot/query?prompt_id=4",  # Profile
    "userbot/query?prompt_id=5",  # KYC
    "userbot/query?prompt_id=6",  # CIBIL
    "userbot/query?prompt_id=8",  # Salary
    "userbot/query?prompt_id=13",  # Active Loans
    "userbot/query?prompt_id=16",  # Loan Status
    "userbot/query?prompt_id=17"   # Bank Accounts
]
CREDENTIALS = {
    "email": "john.doe@example.com",
    "password": "John@pwd"
}

def check_server_availability():
    """Check if the server is available and responsive"""
    logger.info(f"Checking server availability at {BASE_URL}...")
    
    try:
        # Just try to connect without a specific endpoint
        parsed_url = urlparse(BASE_URL)
        base = f"{parsed_url.scheme}://{parsed_url.netloc}"
        response = requests.get(base, timeout=5)
        logger.info(f"Server connection successful: Status {response.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        logger.error(f"⚠️ CONNECTION ERROR: Could not connect to {BASE_URL}")
        logger.error("⚠️ Please check if the backend service is running.")
        return False
    except requests.exceptions.Timeout:
        logger.error(f"⚠️ TIMEOUT: Connection to {BASE_URL} timed out")
        logger.error("⚠️ The server might be overloaded or not responding.")
        return False
    except Exception as e:
        logger.error(f"⚠️ ERROR: Unexpected error connecting to server: {str(e)}")
        return False

def test_authentication():
    """Test authentication with the backend service"""
    logger.info(f"Testing authentication with credentials: {CREDENTIALS['email']}")
    
    try:
        session = requests.Session()
        response = session.post(LOGIN_URL, json=CREDENTIALS, timeout=10)
        
        if response.status_code == 200:
            logger.info("✅ Authentication successful!")
            return session
        else:
            logger.error(f"⚠️ Authentication failed: Status {response.status_code}")
            logger.error(f"⚠️ Response: {response.text}")
            return None
    except Exception as e:
        logger.error(f"⚠️ Authentication error: {str(e)}")
        return None

def test_api_endpoints(session):
    """Test all API endpoints to ensure they're working"""
    if not session:
        logger.error("⚠️ Cannot test endpoints without authenticated session")
        return
    
    logger.info("Testing API endpoints...")
    
    for endpoint in TEST_ENDPOINTS:
        url = f"{BASE_URL}/{endpoint}"
        logger.info(f"Testing endpoint: {url}")
        
        try:
            start_time = time.time()
            response = session.get(url, timeout=10)
            end_time = time.time()
            
            if response.status_code == 200:
                logger.info(f"✅ Endpoint {endpoint} is working (took {end_time - start_time:.2f}s)")
                try:
                    data = response.json()
                    if "data" in data:
                        logger.info(f"✅ Response data: {json.dumps(data['data'], indent=2)[:100]}...")
                    else:
                        logger.warning(f"⚠️ Response has no 'data' field: {json.dumps(data, indent=2)[:100]}...")
                except ValueError:
                    logger.warning(f"⚠️ Response is not valid JSON: {response.text[:100]}...")
            else:
                logger.error(f"⚠️ Endpoint {endpoint} failed: Status {response.status_code}")
                logger.error(f"⚠️ Response: {response.text}")
        except requests.exceptions.Timeout:
            logger.error(f"⚠️ Request to {endpoint} timed out")
        except Exception as e:
            logger.error(f"⚠️ Error testing endpoint {endpoint}: {str(e)}")

def provide_recommendations():
    """Provide recommendations based on test results"""
    logger.info("\n======= RECOMMENDATIONS =======")
    logger.info("1. Check that your backend service is running at http://localhost:8080")
    logger.info("2. Verify that the credentials (john.doe@example.com/John@pwd) are correct")
    logger.info("3. Ensure that the backend service has CORS configured to accept requests from Rasa")
    logger.info("4. Check for any firewall or network issues that might be blocking connections")
    logger.info("5. Try restarting both the backend service and the Rasa action server")
    logger.info("6. Check the backend logs for any errors during authentication or API calls")
    logger.info("7. If using Docker, verify that the containers can communicate with each other")
    logger.info("=========================================")

def main():
    """Main test function"""
    logger.info("=== BACKEND CONNECTION TESTER ===")
    
    if not check_server_availability():
        logger.error("⚠️ Server is not available. Cannot proceed with further tests.")
        provide_recommendations()
        return
    
    session = test_authentication()
    if session:
        test_api_endpoints(session)
    
    provide_recommendations()

if __name__ == "__main__":
    main()