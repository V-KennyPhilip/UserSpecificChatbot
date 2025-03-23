# """
# Bank context management helper module to maintain contextual information
# about bank accounts between conversation turns.
# """
# import logging
# import re
# import json
# from typing import Dict, List, Optional, Any

# logger = logging.getLogger(__name__)

# class BankContextHelper:
#     """Helper class to manage bank context in conversations"""
    
#     _instance = None
    
#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super(BankContextHelper, cls).__new__(cls)
#             cls._instance.banks_cache = {}  # user_id -> list of bank details
#             cls._instance.last_api_responses = {}  # To cache API responses temporarily
#         return cls._instance
    
#     def store_banks_info(self, user_id: str, bank_data: Any) -> None:
#         """
#         Stores bank information for a user from API response
        
#         Args:
#             user_id: The user ID
#             bank_data: The bank data from API (could be string or dict)
#         """
#         try:
#             # Clear previous cache for this user
#             self.banks_cache[user_id] = []
            
#             # Store the original response for debugging
#             self.last_api_responses[user_id] = bank_data
            
#             # Handle different response formats
#             if isinstance(bank_data, str):
#                 # Try to extract bank information from formatted string
#                 # Look for a list of banks in the string
#                 banks_match = re.search(r"'bankdetails':\s*(\[.*?\])", bank_data, re.DOTALL)
#                 if banks_match:
#                     try:
#                         # Try to parse the bank details JSON
#                         banks_str = banks_match.group(1).replace("'", '"')
#                         # Fix JSON format issues
#                         banks_str = re.sub(r'(\w+):', r'"\1":', banks_str)
#                         banks = json.loads(banks_str)
#                         self.banks_cache[user_id] = banks
#                         logger.info(f"Parsed {len(banks)} banks from string response for user {user_id}")
#                     except json.JSONDecodeError as e:
#                         logger.error(f"Failed to parse banks JSON: {e}")
            
#             elif isinstance(bank_data, dict) and "extraAction" in bank_data:
#                 # Handle structured response with extraAction
#                 if "bankdetails" in bank_data["extraAction"]:
#                     self.banks_cache[user_id] = bank_data["extraAction"]["bankdetails"]
#                     logger.info(f"Stored {len(self.banks_cache[user_id])} banks for user {user_id}")
            
#             logger.debug(f"Stored banks for user {user_id}: {self.banks_cache[user_id]}")
#         except Exception as e:
#             logger.error(f"Error storing banks info: {str(e)}")
    
#     def get_bank_id_by_name(self, user_id: str, bank_name: str) -> Optional[str]:
#         """
#         Finds a bank ID based on a bank name for a specific user
        
#         Args:
#             user_id: The user ID
#             bank_name: Full or partial bank name to search for
            
#         Returns:
#             The bank ID if found, None otherwise
#         """
#         if user_id not in self.banks_cache or not self.banks_cache[user_id]:
#             logger.warning(f"No cached banks found for user {user_id}")
#             return None
        
#         # Normalize the bank name for case-insensitive comparison
#         bank_name_lower = bank_name.lower()
        
#         for bank in self.banks_cache[user_id]:
#             # Check if this is a dictionary with bankName and bankId
#             if isinstance(bank, dict) and "bankName" in bank and "bankId" in bank:
#                 if bank_name_lower in bank["bankName"].lower():
#                     logger.info(f"Found bank ID {bank['bankId']} for bank name '{bank_name}'")
#                     return str(bank["bankId"])
        
#         logger.warning(f"No matching bank found for name '{bank_name}'")
#         return None
    
#     def extract_bank_name_from_message(self, message_text: str) -> Optional[str]:
#         """
#         Extracts a bank name from a user message
        
#         Args:
#             message_text: The user's message text
            
#         Returns:
#             The extracted bank name, or None if no bank name found
#         """
#         # Common patterns for requesting bank details
#         patterns = [
#             # Direct mention of a bank name
#             r"(?:my|the)\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)\s+(?:bank|account)",
#             # "details of X bank"
#             r"details\s+of\s+(?:my|the)?\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)\s+bank",
#             # "X bank details"
#             r"([A-Za-z]+(?:\s+[A-Za-z]+)?)\s+bank\s+details",
#             # "check X bank" 
#             r"check\s+(?:my|the)?\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)\s+bank"
#         ]
        
#         for pattern in patterns:
#             match = re.search(pattern, message_text, re.IGNORECASE)
#             if match:
#                 bank_name = match.group(1)
#                 logger.info(f"Extracted bank name '{bank_name}' from message")
#                 return bank_name
        
#         logger.info("No bank name extracted from message")
#         return None
import logging
import re
from typing import Dict, List, Any, Optional, Union

# Configure logger
logger = logging.getLogger(__name__)

class BankContextHelper:
    """
    Helper class to manage bank context during conversations
    """
    
    def __init__(self):
        # In-memory cache for bank information
        self._banks_cache = {}
    
    def store_banks_info(self, user_id: str, bank_data: Union[str, dict]) -> None:
        """
        Store bank information in memory for a user
        
        Args:
            user_id: The user identifier
            bank_data: Bank information from the API
        """
        if isinstance(bank_data, str):
            # If bank_data is a string, we might need to parse it
            logger.info(f"Storing bank string data for user {user_id}")
            self._banks_cache[user_id] = bank_data
        else:
            # If it's already a dict or JSON object, store directly
            logger.info(f"Storing bank JSON data for user {user_id}")
            
            # If the API response follows the example format with extraAction containing bank data
            if "extraAction" in bank_data and isinstance(bank_data["extraAction"], dict):
                banks = bank_data["extraAction"].get("banks", [])
                if banks:
                    self._banks_cache[user_id] = banks
            else:
                # Store the whole data object if structure is different
                self._banks_cache[user_id] = bank_data
    
    def extract_bank_name_from_message(self, message: str) -> Optional[str]:
        """
        Try to extract a bank name from the user message
        
        Args:
            message: The user message text
            
        Returns:
            Extracted bank name or None if not found
        """
        # Common Indian bank names to look for
        common_banks = [
            "SBI", "State Bank of India", 
            "HDFC", "HDFC Bank",
            "ICICI", "ICICI Bank",
            "Axis", "Axis Bank",
            "Kotak", "Kotak Mahindra",
            "PNB", "Punjab National Bank",
            "Bank of Baroda",
            "Canara Bank",
            "Union Bank",
            "Yes Bank",
            "IndusInd",
            "Federal Bank"
        ]
        
        # Check if any of the common bank names are in the message
        message = message.lower()
        for bank in common_banks:
            bank_lower = bank.lower()
            if bank_lower in message:
                logger.info(f"Extracted bank name '{bank}' from message")
                return bank
        
        return None
    
    def get_bank_id_by_name(self, user_id: str, bank_name: str) -> Optional[str]:
        """
        Get bank ID by name from the cached bank data
        
        Args:
            user_id: The user identifier
            bank_name: The bank name to look for
            
        Returns:
            Bank ID if found, None otherwise
        """
        # Check if we have cached banks for this user
        if user_id not in self._banks_cache:
            logger.warning(f"No cached banks found for user {user_id}")
            return None
        
        bank_data = self._banks_cache[user_id]
        bank_name_lower = bank_name.lower()
        
        # If bank_data is a list of bank objects
        if isinstance(bank_data, list):
            for bank in bank_data:
                if "name" in bank and bank["name"].lower() == bank_name_lower:
                    logger.info(f"Found bank ID {bank.get('id')} for bank name '{bank_name}'")
                    return str(bank.get("id"))
        
        # If we have a string representation, try to parse it
        elif isinstance(bank_data, str):
            # This is a simple pattern matching approach
            # In a real implementation, you'd want proper parsing based on the actual data format
            match = re.search(fr"bank.*?id.*?(\d+).*?name.*?{re.escape(bank_name_lower)}", bank_data.lower())
            if match:
                bank_id = match.group(1)
                logger.info(f"Extracted bank ID {bank_id} for bank name '{bank_name}' from string data")
                return bank_id
        
        logger.warning(f"Could not find bank ID for bank name '{bank_name}'")
        return None