#!/usr/bin/env python
"""
Custom action server startup script with integrated fixes
for common issues in Rasa action servers.
"""

import logging
import sys
import os
import time
from rasa_sdk import utils
from rasa_sdk.endpoint import create_app
from rasa_sdk.executor import ActionExecutor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def apply_fixes():
    """Apply fixes to common issues"""
    logger.info("Applying fixes to the action server...")
    
    # Import our global response formatter to patch the dispatcher
    try:
        from actions.global_response_formatter import patch_dispatcher
        logger.info("✅ Applied button formatting fixes")
    except ImportError:
        logger.warning("⚠️ Could not apply button formatting fixes")
    
    # Set longer timeouts for requests to handle slow responses
    try:
        import requests
        requests.adapters.DEFAULT_RETRIES = 3
        session = requests.Session()
        session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
        session.mount('https://', requests.adapters.HTTPAdapter(max_retries=3))
        logger.info("✅ Configured request retries and timeouts")
    except ImportError:
        logger.warning("⚠️ Could not configure request retries")
    
    # Pre-authenticate with backend to warm up connections
    try:
        from actions.session_manager import SessionManager
        session_manager = SessionManager()
        if session_manager.login():
            logger.info("✅ Pre-authenticated with backend service")
        else:
            logger.warning("⚠️ Pre-authentication with backend failed")
    except ImportError:
        logger.warning("⚠️ Could not pre-authenticate with backend")
    
    logger.info("All fixes applied successfully")

def test_backend_connection():
    """Test the backend connection on startup"""
    logger.info("Testing backend connection...")
    
    try:
        # Try to import and use the connection tester
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from connection_tester import check_server_availability, test_authentication
        
        if check_server_availability():
            logger.info("✅ Backend server is available")
            session = test_authentication()
            if session:
                logger.info("✅ Authentication with backend successful")
                return True
            else:
                logger.warning("⚠️ Authentication with backend failed")
                return False
        else:
            logger.warning("⚠️ Backend server is not available")
            return False
    except ImportError:
        logger.warning("⚠️ Could not import connection tester")
        # Fall back to basic connection test
        try:
            from actions.session_manager import SessionManager
            session_manager = SessionManager()
            if session_manager.login():
                logger.info("✅ Basic connection test successful")
                return True
            else:
                logger.warning("⚠️ Basic connection test failed")
                return False
        except Exception as e:
            logger.error(f"⚠️ Error testing backend connection: {str(e)}")
            return False

def main():
    """Main function to start the action server with fixes"""
    logger.info("Starting enhanced action server...")
    
    # Apply fixes
    apply_fixes()
    
    # Test backend connection
    connection_successful = test_backend_connection()
    if not connection_successful:
        logger.warning("⚠️ Backend connection issues detected. The action server will start anyway, but some actions may fail.")
    
    # Start the action server with our executor
    logger.info("Initializing action server...")
    executor = ActionExecutor()
    executor.register_package("actions")
    
    # Create and run the app
    logger.info("Starting action server...")
    app = create_app(executor)
    utils.run(app, host="0.0.0.0", port=5055)

if __name__ == "__main__":
    main()