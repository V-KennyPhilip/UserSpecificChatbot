"""
This file contains helper functions to better handle bank-related queries.
"""
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import FollowupAction
import logging

logger = logging.getLogger(__name__)

class ActionHandleBankQuery(Action):
    """
    Custom action to handle generic bank-related queries and 
    redirect to the appropriate action based on the context.
    """
    
    def name(self) -> Text:
        return "action_handle_bank_query"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get the latest user message
        latest_message = tracker.latest_message.get('text', '').lower()
        
        # Check if we already have bank accounts information
        from .bank_context_helper import BankContextHelper
        bank_context = BankContextHelper()
        user_id = tracker.get_slot("user_id") or "1"
        
        has_banks_cached = user_id in bank_context.banks_cache and len(bank_context.banks_cache[user_id]) > 0
        
        # Check for specific bank in the message
        bank_name = bank_context.extract_bank_name_from_message(latest_message)
        
        # If we found a specific bank name and have banks cached
        if bank_name and has_banks_cached:
            # Try to get bank ID and show details
            bank_id = bank_context.get_bank_id_by_name(user_id, bank_name)
            if bank_id:
                logger.info(f"Found bank ID {bank_id} for '{bank_name}', showing details")
                # Return action to show bank details for this bank
                return [FollowupAction("action_fetch_bank_details")]
        
        # If asking for general bank info (list of banks)
        bank_list_patterns = [
            "bank accounts", "bank account", "linked banks", "my banks", 
            "linked bank", "list banks", "list bank", "view banks", 
            "show banks", "banks", "bank", "banking"
        ]
        
        if any(pattern in latest_message for pattern in bank_list_patterns):
            logger.info("General bank account query detected, showing linked banks")
            return [FollowupAction("action_fetch_linked_banks")]
            
        # If not enough context, show bank management options
        dispatcher.utter_message(
            text="I can help you with your bank accounts. What would you like to do?",
            buttons=[
                {"title": "View linked bank accounts", "payload": "/BANK_LINKED_NUMBER"},
                {"title": "Add new bank account", "payload": "/navigate_bank_add"}
            ]
        )
        
        return []