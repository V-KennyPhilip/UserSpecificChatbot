# """
# Enhanced form handling for the chatbot, handling common form issues.
# """
# from typing import Any, Dict, List, Text, Optional
# from rasa_sdk import Action, Tracker, FormValidationAction
# from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.events import SlotSet, FollowupAction, Form, ActiveLoop

# class ActionResetAllForms(Action):
#     """Action to reset all active forms and clear related slots"""
    
#     def name(self) -> Text:
#         return "action_reset_all_forms"
        
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         # List of all form-related slots
#         form_slots = [
#             "salary_amount", 
#             "phone_number", 
#             "address",
#             "account_number", 
#             "account_holder_name", 
#             "ifsc_code", 
#             "bank_name", 
#             "bank_account_type"
#         ]
        
#         # Clear all form slots
#         events = [SlotSet(slot, None) for slot in form_slots]
        
#         # Reset any active form
#         events.append(ActiveLoop(None))
        
#         # No feedback to user as utter_out_of_scope will follow this action
#         return events

# class ActionValidateSalaryForm(FormValidationAction):
#     """Form validation action for salary updates"""
    
#     def name(self) -> Text:
#         return "validate_update_salary_form"
    
#     def validate_salary_amount(
#         self,
#         slot_value: Any,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> Dict[Text, Any]:
#         """Validate salary_amount value."""
        
#         # Clean up the input to extract just the number
#         import re
#         if isinstance(slot_value, str):
#             # Extract numbers from text like "87000 will be my new salary"
#             numbers = re.findall(r'\d+', slot_value)
#             if numbers:
#                 # Use the first number found
#                 cleaned_value = numbers[0]
#                 dispatcher.utter_message(text=f"I'll update your salary to {cleaned_value}.")
#                 return {"salary_amount": cleaned_value}
        
#         # If no number was found or value isn't a string
#         if not slot_value:
#             dispatcher.utter_message(text="Please enter a valid salary amount as a number.")
#             return {"salary_amount": None}
            
#         return {"salary_amount": slot_value}

# class ActionValidateContactForm(FormValidationAction):
#     """Form validation action for contact updates"""
    
#     def name(self) -> Text:
#         return "validate_update_contact_form"
    
#     def validate_phone_number(
#         self,
#         slot_value: Any,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> Dict[Text, Any]:
#         """Validate phone_number value."""
        
#         import re
#         if isinstance(slot_value, str):
#             # Check if it's a valid phone number (10 digits)
#             if re.match(r'^\d{10}$', slot_value):
#                 return {"phone_number": slot_value}
#             else:
#                 dispatcher.utter_message(text="Please enter a valid 10-digit phone number.")
#                 return {"phone_number": None}
        
#         return {"phone_number": slot_value}
    
#     def validate_address(
#         self,
#         slot_value: Any,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> Dict[Text, Any]:
#         """Validate address value."""
        
#         # Address validation is more flexible
#         if isinstance(slot_value, str) and len(slot_value) > 5:
#             return {"address": slot_value}
#         elif slot_value:
#             # If there's any value, accept it but note it's short
#             dispatcher.utter_message(text="That address seems quite short, but I'll accept it.")
#             return {"address": slot_value}
        
#         return {"address": slot_value}

# class ActionValidateBankAddForm(FormValidationAction):
#     """Form validation action for adding bank accounts"""
    
#     def name(self) -> Text:
#         return "validate_add_bank_form"
    
#     def validate_account_number(
#         self,
#         slot_value: Any,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> Dict[Text, Any]:
#         """Validate account_number value."""
        
#         import re
#         if isinstance(slot_value, str):
#             # Clean up and extract just the number
#             cleaned_value = re.sub(r'[^0-9]', '', slot_value)
            
#             if len(cleaned_value) >= 9 and len(cleaned_value) <= 18:
#                 # Valid account number length
#                 return {"account_number": cleaned_value}
#             else:
#                 dispatcher.utter_message(text="Please enter a valid account number (9-18 digits).")
#                 return {"account_number": None}
        
#         return {"account_number": slot_value}
from typing import Any, Text, Dict, List
from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet
import logging
import re

# Configure logger
logger = logging.getLogger(__name__)

class ActionResetAllForms(FormValidationAction):
    """Reset all forms in the conversation."""
    
    def name(self) -> Text:
        return "action_reset_all_forms"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        return [SlotSet("requested_form_info", None)]

class ActionValidateSalaryForm(FormValidationAction):
    """Validate the update_salary_form."""
    
    def name(self) -> Text:
        return "validate_update_salary_form"
    
    def validate_salary_amount(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate salary_amount value."""
        
        if not slot_value:
            dispatcher.utter_message(json_message={
                "message": "Please provide your updated salary amount.",
                "request_slot": "salary_amount"
            })
            return {"salary_amount": None}
        
        # Try to convert to a number and validate
        try:
            # Remove any commas and non-numeric characters except decimal point
            cleaned_value = re.sub(r'[^\d.]', '', str(slot_value))
            salary = float(cleaned_value)
            
            if salary <= 0:
                dispatcher.utter_message(json_message={
                    "message": "Salary amount must be greater than zero.",
                    "request_slot": "salary_amount"
                })
                return {"salary_amount": None}
            
            # Convert back to string for storage
            return {"salary_amount": str(salary), "requested_form_info": "salary_updated"}
            
        except ValueError:
            dispatcher.utter_message(json_message={
                "message": "Please provide a valid numeric salary amount.",
                "request_slot": "salary_amount"
            })
            return {"salary_amount": None}

class ActionValidateContactForm(FormValidationAction):
    """Validate the update_contact_form."""
    
    def name(self) -> Text:
        return "validate_update_contact_form"
    
    def validate_phone_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate phone_number value."""
        
        # Phone is optional if address is provided
        address = tracker.get_slot("address")
        if not slot_value and address:
            return {"phone_number": None}
        
        if not slot_value:
            return {"phone_number": None}
        
        # Validate phone number format (simple 10-digit validation for India)
        # In a real application, you'd want more sophisticated validation
        if not re.match(r'^\d{10}$', str(slot_value)):
            dispatcher.utter_message(json_message={
                "message": "Please provide a valid 10-digit phone number.",
                "request_slot": "phone_number"
            })
            return {"phone_number": None}
        
        return {"phone_number": slot_value}
    
    def validate_address(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate address value."""
        
        # Address is optional if phone is provided
        phone = tracker.get_slot("phone_number")
        if not slot_value and phone:
            return {"address": None, "requested_form_info": "contact_updated"}
        
        if not slot_value:
            return {"address": None}
        
        # Basic validation for address length
        if len(str(slot_value)) < 5:
            dispatcher.utter_message(json_message={
                "message": "Please provide a more detailed address.",
                "request_slot": "address"
            })
            return {"address": None}
        
        return {"address": slot_value, "requested_form_info": "contact_updated"}

class ActionValidateBankAddForm(FormValidationAction):
    """Validate the add_bank_form."""
    
    def name(self) -> Text:
        return "validate_add_bank_form"
    
    def validate_account_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate account_number value."""
        
        if not slot_value:
            return {"account_number": None}
        
        # Simple validation for account number (numeric, between 9-18 digits)
        # In a real application, you'd want more sophisticated validation based on bank rules
        if not re.match(r'^\d{9,18}$', str(slot_value)):
            dispatcher.utter_message(json_message={
                "message": "Please provide a valid account number (9-18 digits).",
                "request_slot": "account_number"
            })
            return {"account_number": None}
        
        return {"account_number": slot_value}
    
    def validate_account_holder_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate account_holder_name value."""
        
        if not slot_value:
            return {"account_holder_name": None}
        
        # Basic validation for name (at least two words, alphabetic)
        if not re.match(r'^[A-Za-z]+(\s[A-Za-z]+)+$', str(slot_value)):
            dispatcher.utter_message(json_message={
                "message": "Please provide a valid full name with at least first and last name.",
                "request_slot": "account_holder_name"
            })
            return {"account_holder_name": None}
        
        return {"account_holder_name": slot_value}
    
    def validate_ifsc_code(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate ifsc_code value."""
        
        if not slot_value:
            return {"ifsc_code": None}
        
        # IFSC code validation for India (11 characters: 4 alphabets representing bank, 
        # 5th character is 0, and last 6 characters are alphanumeric)
        if not re.match(r'^[A-Z]{4}0[A-Z0-9]{6}$', str(slot_value).upper()):
            dispatcher.utter_message(json_message={
                "message": "Please provide a valid IFSC code (e.g., SBIN0123456).",
                "request_slot": "ifsc_code"
            })
            return {"ifsc_code": None}
        
        return {"ifsc_code": str(slot_value).upper()}
    
    def validate_bank_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate bank_name value."""
        
        if not slot_value:
            return {"bank_name": None}
        
        # Basic validation for bank name (at least 2 characters, alphabetic)
        if not re.match(r'^[A-Za-z\s]{2,}$', str(slot_value)):
            dispatcher.utter_message(json_message={
                "message": "Please provide a valid bank name.",
                "request_slot": "bank_name"
            })
            return {"bank_name": None}
        
        return {"bank_name": slot_value}
    
    def validate_bank_account_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate bank_account_type value."""
        
        if not slot_value:
            return {"bank_account_type": None}
        
        # Validate account type (must be either SAVINGS or CURRENT)
        valid_types = ["SAVINGS", "CURRENT"]
        if str(slot_value).upper() not in valid_types:
            dispatcher.utter_message(json_message={
                "message": "Bank Account Type must be either SAVINGS or CURRENT.",
                "request_slot": "bank_account_type",
                "valid_options": valid_types
            })
            return {"bank_account_type": None}
        
        return {"bank_account_type": str(slot_value).upper(), "requested_form_info": "bank_added"}