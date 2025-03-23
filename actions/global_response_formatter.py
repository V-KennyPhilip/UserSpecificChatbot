"""
This module provides global formatting for responses to ensure consistency
and prevent common formatting errors.
"""
from typing import Any, Dict, List, Optional, Text
import logging

logger = logging.getLogger(__name__)

class ResponseFormatter:
    """
    Class to provide consistent formatting for responses across actions.
    """
    
    @staticmethod
    def format_button_payload(payload: str) -> str:
        """
        Format button payloads to ensure they're valid and don't cause errors.
        
        Args:
            payload: The original payload string
            
        Returns:
            The formatted payload string
        """
        # Remove any JSON-like parameters that cause parsing errors
        if '{' in payload and '}' in payload:
            # Extract just the intent part before the JSON
            payload = payload.split('{')[0]
        
        return payload
    
    @staticmethod
    def format_buttons(buttons: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Format a list of buttons to ensure payloads are valid.
        
        Args:
            buttons: List of button dictionaries
            
        Returns:
            List of formatted button dictionaries
        """
        formatted_buttons = []
        
        for button in buttons:
            if 'payload' in button:
                formatted_buttons.append({
                    'title': button['title'],
                    'payload': ResponseFormatter.format_button_payload(button['payload'])
                })
            else:
                formatted_buttons.append(button)
        
        return formatted_buttons
    
    @staticmethod
    def create_feedback_buttons() -> List[Dict[str, str]]:
        """
        Create properly formatted feedback buttons.
        
        Returns:
            List of formatted feedback button dictionaries
        """
        return [
            {'title': '👍 Yes', 'payload': '/affirm'},
            {'title': '👎 No', 'payload': '/deny'}
        ]

def patch_dispatcher():
    """
    Patch the CollectingDispatcher class to automatically format buttons.
    This should be called at the start of your action server.
    """
    from rasa_sdk.executor import CollectingDispatcher
    
    # Store the original utter_message method
    original_utter_message = CollectingDispatcher.utter_message
    
    # Define the patched method
    def patched_utter_message(self, *args, **kwargs):
        if 'buttons' in kwargs:
            kwargs['buttons'] = ResponseFormatter.format_buttons(kwargs['buttons'])
        return original_utter_message(self, *args, **kwargs)
    
    # Replace the original method with our patched version
    CollectingDispatcher.utter_message = patched_utter_message
    
    logger.info("CollectingDispatcher.utter_message has been patched for consistent button formatting")

# Apply the patch immediately when this module is imported
patch_dispatcher()