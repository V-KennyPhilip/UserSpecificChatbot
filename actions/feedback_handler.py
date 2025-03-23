"""
Module to handle user feedback in a more robust way, 
fixing the common errors with the feedback buttons.
"""
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import FollowupAction, SlotSet

class ActionUtterFeedback(Action):
    """
    Custom action to provide feedback options without using slots in payloads.
    This fixes the "KeyError: 'feedback_response': true" errors.
    """
    
    def name(self) -> Text:
        return "action_utter_feedback"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Use clean button payloads without JSON parameters
        dispatcher.utter_message(
            text="Was this response helpful to you?",
            buttons=[
                {"title": "👍 Yes", "payload": "/affirm"},
                {"title": "👎 No", "payload": "/deny"}
            ]
        )
        
        return []

class ActionProcessFeedback(Action):
    """
    Custom action to process feedback from the user.
    """
    
    def name(self) -> Text:
        return "action_process_feedback"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get the intent that triggered this action
        intent = tracker.latest_message.get('intent', {}).get('name')
        
        if intent == "affirm":
            # Positive feedback
            dispatcher.utter_message(text="I'm glad that was helpful! Is there anything else you'd like to do?")
            return [SlotSet("feedback_received", True), FollowupAction("action_show_main_menu")]
        elif intent == "deny":
            # Negative feedback
            dispatcher.utter_message(text="I'm sorry to hear that. How can I improve my assistance?")
            return [SlotSet("feedback_received", False), FollowupAction("utter_help")]
        
        # Default fallback
        return [FollowupAction("action_show_main_menu")]

class ActionShowMainMenu(Action):
    """
    Custom action to show the main menu.
    """
    
    def name(self) -> Text:
        return "action_show_main_menu"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(
            text="What would you like to do next?",
            buttons=[
                {"title": "Account Information", "payload": "/navigate_account_info"},
                {"title": "Loan Portfolio", "payload": "/navigate_loan_portfolio"},
                {"title": "Bank Account Management", "payload": "/navigate_bank_management"}
            ]
        )
        
        return []