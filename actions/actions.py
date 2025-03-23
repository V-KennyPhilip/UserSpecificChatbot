# from typing import Any, Text, Dict, List
# from rasa_sdk import Action, Tracker, FormValidationAction
# from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.events import SlotSet, FollowupAction, AllSlotsReset
# import logging
# import datetime
# from .session_manager import SessionManager
# from .global_response_formatter import ResponseFormatter

# # Configure logger
# logger = logging.getLogger(__name__)

# # Intent to Prompt ID mapping
# INTENT_TO_PROMPT_ID = {
#     "ACC_PROFILE": 4,
#     "ACC_KYC": 5,
#     "ACC_VIEW_SALARY": 8,
#     "ACC_UPDATE_SALARY": 10,
#     "ACC_CIBIL": 6,
#     "ACC_CONTACT": 12,
#     "LOAN_ACTIVE_NUMBER": 13,
#     "LOAN_ACTIVE_DETAILS": 14,
#     "LOAN_EMI_DETAILS": 15,
#     "LOAN_STATUS": 16,
#     "BANK_ADD": 20,
#     "BANK_UPDATE": 19,
#     "BANK_LINKED_NUMBER": 17,
#     "BANK_LINKED_DETAILS": 18
# }

# # Helper function to get prompt ID from intent
# def get_prompt_id_for_intent(intent_name):
#     """Get the corresponding prompt ID for a given intent name"""
#     return INTENT_TO_PROMPT_ID.get(intent_name, 0)

# # MoEngage Analytics Helper Function
# def log_to_mo_engage(user_id, event_name, properties=None):
#     """
#     Log events to MoEngage analytics
#     """
#     if properties is None:
#         properties = {}
    
#     try:
#         # Here you would integrate with MoEngage SDK/API
#         # This is a placeholder for the actual implementation
#         logger.info(f"MoEngage Event: {event_name} for user {user_id} with properties {properties}")
#         # In actual implementation, you would send this data to MoEngage
#     except Exception as e:
#         logger.error(f"Error logging to MoEngage: {str(e)}")

# class ActionSetContext(Action):
#     """Sets the conversation context for tracking purposes"""
    
#     def name(self) -> Text:
#         return "action_set_context"
        
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         current_intent = tracker.latest_message.get('intent', {}).get('name')
        
#         # Add prompt_id to response if available
#         prompt_id = get_prompt_id_for_intent(current_intent)
#         if prompt_id > 0:
#             dispatcher.utter_message(json_message={"prompt_id": prompt_id})
        
#         return [SlotSet("context_intent", current_intent)]

# class ActionResetSlots(Action):
#     """Resets all slots at the end of conversation"""
    
#     def name(self) -> Text:
#         return "action_reset_slots"
        
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         return [AllSlotsReset()]

# class ActionLogMoEngage(Action):
#     """Logs user interactions to MoEngage for analytics"""
    
#     def name(self) -> Text:
#         return "action_log_mo_engage"
        
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         user_id = tracker.get_slot("user_id") or "anonymous_user"
#         current_intent = tracker.latest_message.get('intent', {}).get('name')
        
#         # Get prompt ID for the current intent
#         prompt_id = get_prompt_id_for_intent(current_intent)
        
#         properties = {
#             "intent": current_intent,
#             "confidence": tracker.latest_message.get('intent', {}).get('confidence'),
#             "timestamp": datetime.datetime.now().isoformat(),
#             "context_intent": tracker.get_slot("context_intent"),
#             "message": tracker.latest_message.get('text'),
#             "prompt_id": prompt_id
#         }
        
#         log_to_mo_engage(user_id, "user_interaction", properties)
        
#         # Add prompt_id to the response for frontend integration
#         if prompt_id > 0:
#             dispatcher.utter_message(json_message={"prompt_id": prompt_id})
        
#         return []

# class ActionFetchProfile(Action):
#     """Fetches the user's profile details"""
    
#     def name(self) -> Text:
#         return "action_fetch_profile"
        
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         user_id = tracker.get_slot("user_id") or "1"
        
#         try:
#             # Initialize the session manager and get response from backend
#             session_manager = SessionManager()
#             prompt_id = get_prompt_id_for_intent("ACC_PROFILE")
#             response_text = session_manager.get_user_bot_response(prompt_id)
            
#             if response_text:
#                 # Ensure response_text is a string, not a dictionary
#                 if isinstance(response_text, dict):
#                     formatted_text = "**Your Profile Details**\n\n"
#                     for key, value in response_text.items():
#                         formatted_text += f"**{key.capitalize()}:** {value}\n"
#                     dispatcher.utter_message(text=formatted_text)
#                 else:
#                     dispatcher.utter_message(text=response_text)
                
#                 # Add prompt_id to response for frontend integration
#                 dispatcher.utter_message(json_message={"prompt_id": prompt_id})
                
#                 # Log successful API interaction to MoEngage
#                 log_to_mo_engage(user_id, "viewed_profile", {"success": True})
#             else:
#                 dispatcher.utter_message(text="I'm having trouble retrieving your profile information. Please try again later.")
                
#                 # Log failed API interaction to MoEngage
#                 log_to_mo_engage(user_id, "viewed_profile", {"success": False})
                
#         except Exception as e:
#             logger.error(f"Error fetching profile: {str(e)}")
#             dispatcher.utter_message(text="I'm having trouble connecting to the server. Please try again later.")
            
#             # Log error to MoEngage
#             log_to_mo_engage(user_id, "viewed_profile", {"success": False, "error": str(e)})
        
#         return []

# class ActionFetchKYC(Action):
#     """Fetches the user's KYC details"""
    
#     def name(self) -> Text:
#         return "action_fetch_kyc"
        
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         user_id = tracker.get_slot("user_id") or "1"
        
#         try:
#             # Initialize the session manager and get response from backend
#             session_manager = SessionManager()
#             prompt_id = get_prompt_id_for_intent("ACC_KYC")
#             response_text = session_manager.get_user_bot_response(prompt_id)
            
#             if response_text:
#                 dispatcher.utter_message(text=response_text)
                
#                 # Add prompt_id to response for frontend integration
#                 dispatcher.utter_message(json_message={"prompt_id": prompt_id})
                
#                 log_to_mo_engage(user_id, "viewed_kyc", {"success": True})
#             else:
#                 dispatcher.utter_message(text="I'm having trouble retrieving your KYC information. Please try again later.")
#                 log_to_mo_engage(user_id, "viewed_kyc", {"success": False})
                
#         except Exception as e:
#             logger.error(f"Error fetching KYC: {str(e)}")
#             dispatcher.utter_message(text="I'm having trouble connecting to the server. Please try again later.")
#             log_to_mo_engage(user_id, "viewed_kyc", {"success": False, "error": str(e)})
        
#         return []

# class ActionViewSalary(Action):
#     """Fetches the user's salary details"""
    
#     def name(self) -> Text:
#         return "action_view_salary"
        
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         user_id = tracker.get_slot("user_id") or "1"
        
#         try:
#             # Initialize the session manager and get response from backend
#             session_manager = SessionManager()
#             prompt_id = get_prompt_id_for_intent("ACC_VIEW_SALARY")
#             response_text = session_manager.get_user_bot_response(prompt_id)
            
#             if response_text:
#                 dispatcher.utter_message(text=response_text)
                
#                 # Add prompt_id to response for frontend integration
#                 dispatcher.utter_message(json_message={"prompt_id": prompt_id})
                
#                 log_to_mo_engage(user_id, "viewed_salary", {"success": True})
#             else:
#                 dispatcher.utter_message(text="I'm having trouble retrieving your salary information. Please try again later.")
#                 log_to_mo_engage(user_id, "viewed_salary", {"success": False})
                
#         except Exception as e:
#             logger.error(f"Error fetching salary: {str(e)}")
#             dispatcher.utter_message(text="I'm having trouble connecting to the server. Please try again later.")
#             log_to_mo_engage(user_id, "viewed_salary", {"success": False, "error": str(e)})
        
#         return []

# class ActionUpdateSalary(Action):
#     """Updates the user's salary"""
    
#     def name(self) -> Text:
#         return "action_update_salary"
        
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         user_id = tracker.get_slot("user_id") or "1"
#         salary_amount = tracker.get_slot("salary_amount")
        
#         if not salary_amount:
#             dispatcher.utter_message(text="Please provide your updated salary amount.")
#             return [SlotSet("requested_form_info", "salary_update")]
        
#         try:
#             # Initialize the session manager and get response from backend
#             session_manager = SessionManager()
#             prompt_id = get_prompt_id_for_intent("ACC_UPDATE_SALARY")
            
#             # For salary updates, we'd typically need to submit the data to the backend
#             # Since we're using the userbot API, we'll pass the salary as additional parameter
#             response_text = session_manager.get_user_bot_response(prompt_id, salary_amount)
            
#             if response_text:
#                 dispatcher.utter_message(text=response_text)
                
#                 # Add prompt_id to response for frontend integration
#                 dispatcher.utter_message(json_message={"prompt_id": prompt_id})
                
#                 log_to_mo_engage(user_id, "updated_salary", {"success": True, "new_salary": salary_amount})
#             else:
#                 dispatcher.utter_message(text="I'm having trouble updating your salary. Please try again later.")
#                 log_to_mo_engage(user_id, "updated_salary", {"success": False})
                
#         except Exception as e:
#             logger.error(f"Error updating salary: {str(e)}")
#             dispatcher.utter_message(text="I'm having trouble connecting to the server. Please try again later.")
#             log_to_mo_engage(user_id, "updated_salary", {"success": False, "error": str(e)})
        
#         return [SlotSet("salary_amount", None)]

# class ActionFetchCIBIL(Action):
#     """Fetches the user's CIBIL score"""
    
#     def name(self) -> Text:
#         return "action_fetch_cibil"
        
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         user_id = tracker.get_slot("user_id") or "1"
        
#         try:
#             # Initialize the session manager and get response from backend
#             session_manager = SessionManager()
#             prompt_id = get_prompt_id_for_intent("ACC_CIBIL")
#             response_text = session_manager.get_user_bot_response(prompt_id)
            
#             if response_text:
#                 dispatcher.utter_message(text=response_text)
                
#                 # Add prompt_id to response for frontend integration
#                 dispatcher.utter_message(json_message={"prompt_id": prompt_id})
                
#                 log_to_mo_engage(user_id, "viewed_cibil", {"success": True})
#             else:
#                 dispatcher.utter_message(text="I'm having trouble retrieving your CIBIL score. Please try again later.")
#                 log_to_mo_engage(user_id, "viewed_cibil", {"success": False})
                
#         except Exception as e:
#             logger.error(f"Error fetching CIBIL: {str(e)}")
#             dispatcher.utter_message(text="I'm having trouble connecting to the server. Please try again later.")
#             log_to_mo_engage(user_id, "viewed_cibil", {"success": False, "error": str(e)})
        
#         return []

# class ActionUpdateContact(Action):
#     """Updates the user's contact information"""
    
#     def name(self) -> Text:
#         return "action_update_contact"
        
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         user_id = tracker.get_slot("user_id") or "1"
#         phone_number = tracker.get_slot("phone_number")
#         address = tracker.get_slot("address")
        
#         if not phone_number and not address:
#             dispatcher.utter_message(text="Please provide your updated phone number and/or address.")
#             return [SlotSet("requested_form_info", "contact_update")]
        
#         try:
#             # Initialize the session manager and get response from backend
#             session_manager = SessionManager()
#             prompt_id = get_prompt_id_for_intent("ACC_CONTACT")
            
#             # Combine phone and address as additional info
#             additional_info = f"{phone_number}|{address}" if phone_number and address else phone_number or address
            
#             response_text = session_manager.get_user_bot_response(prompt_id, additional_info)
            
#             if response_text:
#                 dispatcher.utter_message(text=response_text)
                
#                 # Add prompt_id to response for frontend integration
#                 dispatcher.utter_message(json_message={"prompt_id": prompt_id})
                
#                 log_to_mo_engage(user_id, "updated_contact", {
#                     "success": True, 
#                     "updated_phone": bool(phone_number),
#                     "updated_address": bool(address)
#                 })
#             else:
#                 dispatcher.utter_message(text="I'm having trouble updating your contact information. Please try again later.")
#                 log_to_mo_engage(user_id, "updated_contact", {"success": False})
                
#         except Exception as e:
#             logger.error(f"Error updating contact: {str(e)}")
#             dispatcher.utter_message(text="I'm having trouble connecting to the server. Please try again later.")
#             log_to_mo_engage(user_id, "updated_contact", {"success": False, "error": str(e)})
        
#         return [SlotSet("phone_number", None), SlotSet("address", None)]

# class ActionFetchActiveLoans(Action):
#     """Fetches the user's active loans"""
    
#     def name(self) -> Text:
#         return "action_fetch_active_loans"
        
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         user_id = tracker.get_slot("user_id") or "1"
        
#         try:
#             # Initialize the session manager and get response from backend
#             session_manager = SessionManager()
#             prompt_id = get_prompt_id_for_intent("LOAN_ACTIVE_NUMBER")
#             response_text = session_manager.get_user_bot_response(prompt_id)
            
#             if response_text:
#                 dispatcher.utter_message(text=response_text)
                
#                 # Add prompt_id to response for frontend integration
#                 dispatcher.utter_message(json_message={"prompt_id": prompt_id})
                
#                 log_to_mo_engage(user_id, "viewed_active_loans", {"success": True})
#             else:
#                 dispatcher.utter_message(text="I'm having trouble retrieving your loan information. Please try again later.")
#                 log_to_mo_engage(user_id, "viewed_active_loans", {"success": False})
                
#         except Exception as e:
#             logger.error(f"Error fetching active loans: {str(e)}")
#             dispatcher.utter_message(text="I'm having trouble connecting to the server. Please try again later.")
#             log_to_mo_engage(user_id, "viewed_active_loans", {"success": False, "error": str(e)})
        
#         return []

# class ActionFetchActiveLoanDetails(Action):
#     """Fetches details of a specific active loan"""
    
#     def name(self) -> Text:
#         return "action_fetch_active_loan_details"
        
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         user_id = tracker.get_slot("user_id") or "1"
#         loan_id = tracker.get_slot("active_loan_id")
        
#         if not loan_id:
#             # Try to get loan_id from the latest entity
#             for entity in tracker.latest_message.get('entities', []):
#                 if entity['entity'] == 'loan_id':
#                     loan_id = entity['value']
#                     break
        
#         if not loan_id:
#             dispatcher.utter_message(text="Please select a specific loan to view its details.")
#             return []
        
#         try:
#             # Initialize the session manager and get response from backend
#             session_manager = SessionManager()
#             prompt_id = get_prompt_id_for_intent("LOAN_ACTIVE_DETAILS")
#             response_text = session_manager.get_user_bot_response(prompt_id, loan_id)
            
#             if response_text:
#                 dispatcher.utter_message(text=response_text)
                
#                 # Add prompt_id to response for frontend integration
#                 dispatcher.utter_message(json_message={"prompt_id": prompt_id})
                
#                 log_to_mo_engage(user_id, "viewed_loan_details", {
#                     "success": True, 
#                     "loan_id": loan_id
#                 })
#             else:
#                 dispatcher.utter_message(text="I'm having trouble retrieving the loan details. Please try again later.")
#                 log_to_mo_engage(user_id, "viewed_loan_details", {
#                     "success": False,
#                     "loan_id": loan_id
#                 })
                
#         except Exception as e:
#             logger.error(f"Error fetching loan details: {str(e)}")
#             dispatcher.utter_message(text="I'm having trouble connecting to the server. Please try again later.")
#             log_to_mo_engage(user_id, "viewed_loan_details", {"success": False, "error": str(e), "loan_id": loan_id})
        
#         return [SlotSet("active_loan_id", loan_id)]

# class ActionFetchEMIDetails(Action):
#     """Fetches EMI details for a specific loan"""
    
#     def name(self) -> Text:
#         return "action_fetch_emi_details"
        
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         user_id = tracker.get_slot("user_id") or "1"
#         loan_id = tracker.get_slot("active_loan_id")
        
#         if not loan_id:
#             # Try to get loan_id from the latest entity
#             for entity in tracker.latest_message.get('entities', []):
#                 if entity['entity'] == 'loan_id':
#                     loan_id = entity['value']
#                     break
        
#         if not loan_id:
#             dispatcher.utter_message(text="Please select a specific loan to view its EMI schedule.")
#             return []
        
#         try:
#             # Initialize the session manager and get response from backend
#             session_manager = SessionManager()
#             prompt_id = get_prompt_id_for_intent("LOAN_EMI_DETAILS")
#             response_text = session_manager.get_user_bot_response(prompt_id, loan_id)
            
#             if response_text:
#                 dispatcher.utter_message(text=response_text)
                
#                 # Add prompt_id to response for frontend integration
#                 dispatcher.utter_message(json_message={"prompt_id": prompt_id})
                
#                 log_to_mo_engage(user_id, "viewed_emi_details", {
#                     "success": True, 
#                     "loan_id": loan_id
#                 })
#             else:
#                 dispatcher.utter_message(text="I'm having trouble retrieving the EMI schedule. Please try again later.")
#                 log_to_mo_engage(user_id, "viewed_emi_details", {
#                     "success": False,
#                     "loan_id": loan_id
#                 })
                
#         except Exception as e:
#             logger.error(f"Error fetching EMI details: {str(e)}")
#             dispatcher.utter_message(text="I'm having trouble connecting to the server. Please try again later.")
#             log_to_mo_engage(user_id, "viewed_emi_details", {"success": False, "error": str(e), "loan_id": loan_id})
        
#         return [SlotSet("active_loan_id", loan_id)]

# class ActionFetchLoanStatus(Action):
#     """Fetches status of all loan applications"""
    
#     def name(self) -> Text:
#         return "action_fetch_loan_status"
        
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         user_id = tracker.get_slot("user_id") or "1"
        
#         try:
#             # Initialize the session manager and get response from backend
#             session_manager = SessionManager()
#             prompt_id = get_prompt_id_for_intent("LOAN_STATUS")
#             response_text = session_manager.get_user_bot_response(prompt_id)
            
#             if response_text:
#                 dispatcher.utter_message(text=response_text)
                
#                 # Add prompt_id to response for frontend integration
#                 dispatcher.utter_message(json_message={"prompt_id": prompt_id})
                
#                 log_to_mo_engage(user_id, "viewed_loan_status", {"success": True})
#             else:
#                 dispatcher.utter_message(text="I'm having trouble retrieving your loan application status. Please try again later.")
#                 log_to_mo_engage(user_id, "viewed_loan_status", {"success": False})
                
#         except Exception as e:
#             logger.error(f"Error fetching loan status: {str(e)}")
#             dispatcher.utter_message(text="I'm having trouble connecting to the server. Please try again later.")
#             log_to_mo_engage(user_id, "viewed_loan_status", {"success": False, "error": str(e)})
        
#         return []

# class ActionAddBank(Action):
#     """Adds a new bank account"""
    
#     def name(self) -> Text:
#         return "action_add_bank"
        
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         user_id = tracker.get_slot("user_id") or "1"
#         account_number = tracker.get_slot("account_number")
#         account_holder_name = tracker.get_slot("account_holder_name")
#         ifsc_code = tracker.get_slot("ifsc_code")
#         bank_name = tracker.get_slot("bank_name")
#         bank_account_type = tracker.get_slot("bank_account_type")
        
#         # Validate required fields
#         if not all([account_number, account_holder_name, ifsc_code, bank_name, bank_account_type]):
#             missing_fields = []
#             if not account_number:
#                 missing_fields.append("Account Number")
#             if not account_holder_name:
#                 missing_fields.append("Account Holder Name")
#             if not ifsc_code:
#                 missing_fields.append("IFSC Code")
#             if not bank_name:
#                 missing_fields.append("Bank Name")
#             if not bank_account_type:
#                 missing_fields.append("Bank Account Type")
            
#             dispatcher.utter_message(text=f"Please provide all required fields: {', '.join(missing_fields)}")
#             return [SlotSet("requested_form_info", "bank_add")]
        
#         # Validate bank account type
#         if bank_account_type not in ["SAVINGS", "CURRENT"]:
#             dispatcher.utter_message(text="Bank Account Type must be either SAVINGS or CURRENT.")
#             return [SlotSet("bank_account_type", None)]
        
#         try:
#             # Initialize the session manager and get response from backend
#             session_manager = SessionManager()
#             prompt_id = get_prompt_id_for_intent("BANK_ADD")
            
#             # Format bank details as a pipe-separated string for the additional parameter
#             bank_details = f"{account_number}|{account_holder_name}|{ifsc_code}|{bank_name}|{bank_account_type}"
            
#             response_text = session_manager.get_user_bot_response(prompt_id, bank_details)
            
#             if response_text:
#                 dispatcher.utter_message(text=response_text)
                
#                 # Add prompt_id to response for frontend integration
#                 dispatcher.utter_message(json_message={"prompt_id": prompt_id})
                
#                 log_to_mo_engage(user_id, "added_bank", {
#                     "success": True, 
#                     "bank_name": bank_name,
#                     "account_type": bank_account_type
#                 })
#             else:
#                 dispatcher.utter_message(text="I'm having trouble adding your bank account. Please try again later.")
                
#                 log_to_mo_engage(user_id, "added_bank", {
#                     "success": False,
#                     "bank_name": bank_name
#                 })
                
#         except Exception as e:
#             logger.error(f"Error adding bank account: {str(e)}")
#             dispatcher.utter_message(text="I'm having trouble connecting to the server. Please try again later.")
            
#             log_to_mo_engage(user_id, "added_bank", {
#                 "success": False, 
#                 "error": str(e),
#                 "bank_name": bank_name
#             })
        
#         return [
#             SlotSet("account_number", None),
#             SlotSet("account_holder_name", None),
#             SlotSet("ifsc_code", None),
#             SlotSet("bank_name", None),
#             SlotSet("bank_account_type", None)
#         ]

# class ActionUpdateBank(Action):
#     """Updates an existing bank account"""
    
#     def name(self) -> Text:
#         return "action_update_bank"
        
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         user_id = tracker.get_slot("user_id") or "1"
#         bank_id = tracker.get_slot("active_bank_id")
#         account_holder_name = tracker.get_slot("account_holder_name")
#         bank_account_type = tracker.get_slot("bank_account_type")
        
#         if not bank_id:
#             # Try to get bank_id from the latest entity
#             for entity in tracker.latest_message.get('entities', []):
#                 if entity['entity'] == 'bank_id':
#                     bank_id = entity['value']
#                     break
        
#         if not bank_id:
#             dispatcher.utter_message(text="Please select a specific bank account to update.")
#             return []
        
#         # Validate required fields
#         if not account_holder_name and not bank_account_type:
#             dispatcher.utter_message(text="Please provide at least one field to update: Account Holder Name or Bank Account Type.")
#             return [SlotSet("requested_form_info", "bank_update")]
        
#         # Validate bank account type if provided
#         if bank_account_type and bank_account_type not in ["SAVINGS", "CURRENT"]:
#             dispatcher.utter_message(text="Bank Account Type must be either SAVINGS or CURRENT.")
#             return [SlotSet("bank_account_type", None)]
        
#         try:
#             # Initialize the session manager and get response from backend
#             session_manager = SessionManager()
#             prompt_id = get_prompt_id_for_intent("BANK_UPDATE")
            
#             # Format bank update details for the additional parameter
#             # Include blank placeholders for values that aren't being updated
#             update_details = f"{bank_id}|{account_holder_name or ''}|{bank_account_type or ''}"
            
#             response_text = session_manager.get_user_bot_response(prompt_id, update_details)
            
#             if response_text:
#                 dispatcher.utter_message(text=response_text)
                
#                 # Add prompt_id to response for frontend integration
#                 dispatcher.utter_message(json_message={"prompt_id": prompt_id})
                
#                 log_to_mo_engage(user_id, "updated_bank", {
#                     "success": True, 
#                     "bank_id": bank_id,
#                     "updated_name": bool(account_holder_name),
#                     "updated_type": bool(bank_account_type)
#                 })
#             else:
#                 dispatcher.utter_message(text="I'm having trouble updating your bank account information. Please try again later.")
                
#                 log_to_mo_engage(user_id, "updated_bank", {
#                     "success": False,
#                     "bank_id": bank_id
#                 })
                
#         except Exception as e:
#             logger.error(f"Error updating bank account: {str(e)}")
#             dispatcher.utter_message(text="I'm having trouble connecting to the server. Please try again later.")
            
#             log_to_mo_engage(user_id, "updated_bank", {
#                 "success": False, 
#                 "error": str(e),
#                 "bank_id": bank_id
#             })
        
#         return [
#             SlotSet("active_bank_id", bank_id),
#             SlotSet("account_holder_name", None),
#             SlotSet("bank_account_type", None)
#         ]

# class ActionFetchLinkedBanks(Action):
#     """Fetches user's linked bank accounts"""
    
#     def name(self) -> Text:
#         return "action_fetch_linked_banks"
        
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         user_id = tracker.get_slot("user_id") or "1"
        
#         try:
#             # Initialize the session manager and get response from backend
#             session_manager = SessionManager()
#             prompt_id = get_prompt_id_for_intent("BANK_LINKED_NUMBER")
            
#             # Add caching for faster response
#             response_text = session_manager.get_user_bot_response(prompt_id)
            
#             if response_text:
#                 # Store bank information in context helper for future reference
#                 from .bank_context_helper import BankContextHelper
#                 bank_context = BankContextHelper()
#                 bank_context.store_banks_info(user_id, response_text)
                
#                 dispatcher.utter_message(text=response_text)
                
#                 # Add prompt_id to response for frontend integration
#                 dispatcher.utter_message(json_message={"prompt_id": prompt_id})
                
#                 log_to_mo_engage(user_id, "viewed_linked_banks", {"success": True})
#             else:
#                 dispatcher.utter_message(text="I'm having trouble retrieving your bank account information. Please try again later.")
                
#                 log_to_mo_engage(user_id, "viewed_linked_banks", {"success": False})
                
#         except Exception as e:
#             logger.error(f"Error fetching linked banks: {str(e)}")
#             dispatcher.utter_message(text="I'm having trouble connecting to the server. Please try again later.")
            
#             log_to_mo_engage(user_id, "viewed_linked_banks", {
#                 "success": False, 
#                 "error": str(e)
#             })
        
#         return []

# class ActionFetchBankDetails(Action):
#     """Fetches details of a specific bank account"""
    
#     def name(self) -> Text:
#         return "action_fetch_bank_details"
        
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         user_id = tracker.get_slot("user_id") or "1"
#         bank_id = tracker.get_slot("active_bank_id")
        
#         # Get the latest user message
#         latest_message = tracker.latest_message.get('text', '')
        
#         if not bank_id:
#             # Try to get bank_id from the latest entity
#             for entity in tracker.latest_message.get('entities', []):
#                 if entity['entity'] == 'bank_id':
#                     bank_id = entity['value']
#                     break
            
#             # If still no bank_id, try to extract bank name from message
#             if not bank_id and latest_message:
#                 from .bank_context_helper import BankContextHelper
#                 bank_context = BankContextHelper()
                
#                 # Extract bank name from message
#                 bank_name = bank_context.extract_bank_name_from_message(latest_message)
                
#                 # If a bank name was found, try to get its ID
#                 if bank_name:
#                     bank_id = bank_context.get_bank_id_by_name(user_id, bank_name)
#                     if bank_id:
#                         logger.info(f"Found bank ID {bank_id} for bank name '{bank_name}' from message context")
        
#         if not bank_id:
#             dispatcher.utter_message(text="Please select a specific bank account or mention the bank name to view its details.")
#             return []
        
#         try:
#             # Initialize the session manager and get response from backend
#             session_manager = SessionManager()
#             prompt_id = get_prompt_id_for_intent("BANK_LINKED_DETAILS")
            
#             # Add a cache check here for faster response
#             response_text = session_manager.get_user_bot_response(prompt_id, bank_id)
            
#             if response_text:
#                 dispatcher.utter_message(text=response_text)
                
#                 # Add prompt_id to response for frontend integration
#                 dispatcher.utter_message(json_message={"prompt_id": prompt_id})
                
#                 log_to_mo_engage(user_id, "viewed_bank_details", {
#                     "success": True, 
#                     "bank_id": bank_id
#                 })
#             else:
#                 dispatcher.utter_message(text="I'm having trouble retrieving the bank account details. Please try again later.")
                
#                 log_to_mo_engage(user_id, "viewed_bank_details", {
#                     "success": False,
#                     "bank_id": bank_id
#                 })
                
#         except Exception as e:
#             logger.error(f"Error fetching bank details: {str(e)}")
#             dispatcher.utter_message(text="I'm having trouble connecting to the server. Please try again later.")
            
#             log_to_mo_engage(user_id, "viewed_bank_details", {
#                 "success": False, 
#                 "error": str(e),
#                 "bank_id": bank_id
#             })
        
#         return [SlotSet("active_bank_id", bank_id)]
# actions.py
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction, AllSlotsReset
from rasa_sdk.types import DomainDict

import logging
import json
import re
from .session_manager import SessionManager

# Configure logger
logger = logging.getLogger(__name__)

# Intent to Prompt ID mapping
INTENT_TO_PROMPT_ID = {
    "ACC_PROFILE": 4,
    "ACC_KYC": 5,
    "ACC_VIEW_SALARY": 8,
    "ACC_UPDATE_SALARY": 10,
    "ACC_CIBIL": 6,
    "ACC_CONTACT": 12,
    "LOAN_ACTIVE_NUMBER": 13,
    "LOAN_ACTIVE_DETAILS": 14,
    "LOAN_EMI_DETAILS": 15,
    "LOAN_STATUS": 16,
    "BANK_ADD": 20,
    "BANK_UPDATE": 19,
    "BANK_LINKED_NUMBER": 17,
    "BANK_LINKED_DETAILS": 18
}

# Helper function to get prompt ID from intent
def get_prompt_id_for_intent(intent_name):
    """Get the corresponding prompt ID for a given intent name"""
    return INTENT_TO_PROMPT_ID.get(intent_name, 0)

class ActionCheckAuthenticated(Action):
    """
    Modified to assume the user is always authenticated with hardcoded credentials
    """
    
    def name(self) -> Text:
        return "action_check_authenticated"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Verify that SessionManager is authenticated
        if not SessionManager._authenticated:
            # Try to authenticate
            success = SessionManager.initialize()
            if not success:
                # If we still can't authenticate, inform the user
                dispatcher.utter_message(text="I'm having trouble connecting to your account information. Please try again later.")
                return []
        
        # Always proceed with the conversation - we've either authenticated successfully or reported an error
        return []

# class ActionDirectLogin(Action):
#     """Handles login directly without using forms"""
    
#     def name(self) -> Text:
#         return "action_direct_login"
        
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         # Extract email and password directly from message
#         message = tracker.latest_message.get('text', '').lower()
        
#         # Try to extract email from the message
#         email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', message)
#         email = email_match.group(0) if email_match else None
        
#         # Try to extract password - look for patterns like:
#         # - "password is X" or "pass is X" or "pwd is X"
#         # - "with password X" or "with pass X" or "with pwd X"
#         # - just try to get text after the email
#         password = None
        
#         # First try to find password after specific keywords
#         pwd_patterns = [
#             r'password\s+(?:is|:)?\s+([^\s]+)',
#             r'pass\s+(?:is|:)?\s+([^\s]+)',
#             r'pwd\s+(?:is|:)?\s+([^\s]+)',
#             r'with\s+password\s+([^\s]+)',
#             r'with\s+pass\s+([^\s]+)',
#             r'with\s+pwd\s+([^\s]+)'
#         ]
        
#         for pattern in pwd_patterns:
#             pwd_match = re.search(pattern, message, re.IGNORECASE)
#             if pwd_match:
#                 password = pwd_match.group(1)
#                 break
        
#         # If email was found but password wasn't found using patterns,
#         # try to extract whatever text comes after the email
#         if email and not password:
#             # Get text after the email
#             after_email = message.split(email)[1] if len(message.split(email)) > 1 else ""
#             # Try to extract the first word after some connecting words
#             pwd_after_email = re.search(r'(?:and|with|using|,)\s+(\S+)', after_email, re.IGNORECASE)
#             if pwd_after_email:
#                 password = pwd_after_email.group(1)
        
#         # If we couldn't extract either email or password, ask for them explicitly
#         if not email or not password:
#             if not email:
#                 dispatcher.utter_message(json_message={
#                     "message": "Please provide your email address to login.",
#                     "auth_required": True
#                 })
#                 return []
#             elif not password:
#                 dispatcher.utter_message(json_message={
#                     "message": "Please provide your password to login.",
#                     "auth_required": True
#                 })
#                 return []
        
#         # Log what we extracted (for debugging, remove in production)
#         logger.info(f"Extracted email: {email}, password: [REDACTED]")
        
#         # Try to login with the extracted credentials
#         login_success = SessionManager.login(email, password)
        
#         if login_success:
#             dispatcher.utter_message(json_message={
#                 "message": "Login successful! How can I help you today?",
#                 "auth_success": True,
#                 "options": [
#                     {"title": "Account Information", "payload": "/navigate_account_info"},
#                     {"title": "Loan Portfolio", "payload": "/navigate_loan_portfolio"},
#                     {"title": "Bank Account Management", "payload": "/navigate_bank_management"}
#                 ]
#             })
            
#             return [
#                 SlotSet("email", None),  # Clear for security
#                 SlotSet("password", None),  # Clear for security
#                 SlotSet("is_authenticated", True)
#             ]
#         else:
#             dispatcher.utter_message(json_message={
#                 "message": "Login failed. Please check your credentials and try again.",
#                 "auth_failed": True,
#                 "options": [
#                     {"title": "Try Again", "payload": "/login"}
#                 ]
#             })
            
#             return [SlotSet("is_authenticated", False)]

class ActionSetContext(Action):
    """Sets the conversation context for tracking purposes"""
    
    def name(self) -> Text:
        return "action_set_context"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        current_intent = tracker.latest_message.get('intent', {}).get('name')
        
        # Add prompt_id to response if available
        prompt_id = get_prompt_id_for_intent(current_intent)
        if prompt_id > 0:
            dispatcher.utter_message(json_message={"prompt_id": prompt_id})
        
        return [SlotSet("context_intent", current_intent)]

class ActionResetSlots(Action):
    """Resets all slots at the end of conversation"""
    
    def name(self) -> Text:
        return "action_reset_slots"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        return [AllSlotsReset()]

class ActionShowMainMenu(Action):
    """Shows the main menu options"""
    
    def name(self) -> Text:
        return "action_show_main_menu"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get the buttons from domain's utter_main_menu response
        dispatcher.utter_message(json_message={
            "message": "What would you like to do next?",
            "options": [
                {"title": "Account Information", "payload": "/navigate_account_info"},
                {"title": "Loan Portfolio", "payload": "/navigate_loan_portfolio"},
                {"title": "Bank Account Management", "payload": "/navigate_bank_management"}
            ]
        })
        
        return []

class ActionResetAllForms(Action):
    """Resets all active forms"""
    
    def name(self) -> Text:
        return "action_reset_all_forms"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        return [SlotSet("requested_form_info", None)]

class ActionFetchProfile(Action):
    """Fetches the user's profile details"""
    
    def name(self) -> Text:
        return "action_fetch_profile"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            # Initialize the session manager and get response from backend
            session_manager = SessionManager()
            prompt_id = get_prompt_id_for_intent("ACC_PROFILE")
            response_data = session_manager.get_user_bot_response(prompt_id)
            
            if response_data:
                # Return the complete response data as JSON
                dispatcher.utter_message(json_message={
                    "message": "Here are your profile details:",
                    "prompt_id": prompt_id,
                    "data": response_data
                })
            else:
                dispatcher.utter_message(json_message={
                    "message": "Failed to retrieve profile information",
                    "prompt_id": prompt_id
                })
                
        except Exception as e:
            logger.error(f"Error fetching profile: {str(e)}")
            dispatcher.utter_message(json_message={
                "message": "Error connecting to server",
                "error": str(e)
            })
        
        return []

class ActionFetchKYC(Action):
    """Fetches the user's KYC details"""
    
    def name(self) -> Text:
        return "action_fetch_kyc"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            # Initialize the session manager and get response from backend
            session_manager = SessionManager()
            prompt_id = get_prompt_id_for_intent("ACC_KYC")
            response_data = session_manager.get_user_bot_response(prompt_id)
            
            if response_data:
                # Return the complete response data as JSON
                dispatcher.utter_message(json_message={
                    "message": "Here are your KYC details:",
                    "prompt_id": prompt_id,
                    "data": response_data
                })
            else:
                dispatcher.utter_message(json_message={
                    "message": "Failed to retrieve KYC information",
                    "prompt_id": prompt_id
                })
                
        except Exception as e:
            logger.error(f"Error fetching KYC: {str(e)}")
            dispatcher.utter_message(json_message={
                "message": "Error connecting to server",
                "error": str(e)
            })
        
        return []

class ActionViewSalary(Action):
    """Fetches the user's salary details"""
    
    def name(self) -> Text:
        return "action_view_salary"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            # Initialize the session manager and get response from backend
            session_manager = SessionManager()
            prompt_id = get_prompt_id_for_intent("ACC_VIEW_SALARY")
            response_data = session_manager.get_user_bot_response(prompt_id)
            
            if response_data:
                # Return the complete response data as JSON
                dispatcher.utter_message(json_message={
                    "message": "Here is your salary information:",
                    "prompt_id": prompt_id,
                    "data": response_data
                })
            else:
                dispatcher.utter_message(json_message={
                    "message": "Failed to retrieve salary information",
                    "prompt_id": prompt_id
                })
                
        except Exception as e:
            logger.error(f"Error fetching salary: {str(e)}")
            dispatcher.utter_message(json_message={
                "message": "Error connecting to server",
                "error": str(e)
            })
        
        return []

class ActionUpdateSalary(Action):
    """Updates the user's salary"""
    
    def name(self) -> Text:
        return "action_update_salary"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        salary_amount = tracker.get_slot("salary_amount")
        
        if not salary_amount:
            dispatcher.utter_message(json_message={
                "message": "Please provide your updated salary amount.",
                "request_slot": "salary_amount"
            })
            return [SlotSet("requested_form_info", "salary_update")]
        
        try:
            # Initialize the session manager and get response from backend
            session_manager = SessionManager()
            prompt_id = get_prompt_id_for_intent("ACC_UPDATE_SALARY")
            
            # For salary updates, we'd typically need to submit the data to the backend
            response_data = session_manager.get_user_bot_response(prompt_id, salary_amount)
            
            if response_data:
                # Return the complete response data as JSON
                dispatcher.utter_message(json_message={
                    "message": "Salary updated successfully!",
                    "prompt_id": prompt_id,
                    "data": response_data
                })
            else:
                dispatcher.utter_message(json_message={
                    "message": "Failed to update salary information",
                    "prompt_id": prompt_id
                })
                
        except Exception as e:
            logger.error(f"Error updating salary: {str(e)}")
            dispatcher.utter_message(json_message={
                "message": "Error connecting to server",
                "error": str(e)
            })
        
        return [SlotSet("salary_amount", None)]

class ActionFetchCIBIL(Action):
    """Fetches the user's CIBIL score"""
    
    def name(self) -> Text:
        return "action_fetch_cibil"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            # Initialize the session manager and get response from backend
            session_manager = SessionManager()
            prompt_id = get_prompt_id_for_intent("ACC_CIBIL")
            response_data = session_manager.get_user_bot_response(prompt_id)
            
            if response_data:
                # Return the complete response data as JSON
                dispatcher.utter_message(json_message={
                    "message": "Here is your CIBIL score information:",
                    "prompt_id": prompt_id,
                    "data": response_data
                })
            else:
                dispatcher.utter_message(json_message={
                    "message": "Failed to retrieve CIBIL information",
                    "prompt_id": prompt_id
                })
                
        except Exception as e:
            logger.error(f"Error fetching CIBIL: {str(e)}")
            dispatcher.utter_message(json_message={
                "message": "Error connecting to server",
                "error": str(e)
            })
        
        return []

class ActionUpdateContact(Action):
    """Updates the user's contact information"""
    
    def name(self) -> Text:
        return "action_update_contact"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        phone_number = tracker.get_slot("phone_number")
        address = tracker.get_slot("address")
        
        if not phone_number and not address:
            dispatcher.utter_message(json_message={
                "message": "Please provide your updated phone number and/or address.",
                "request_slots": ["phone_number", "address"]
            })
            return [SlotSet("requested_form_info", "contact_update")]
        
        try:
            # Initialize the session manager and get response from backend
            session_manager = SessionManager()
            prompt_id = get_prompt_id_for_intent("ACC_CONTACT")
            
            # Combine phone and address as additional info
            additional_info = f"{phone_number}|{address}" if phone_number and address else phone_number or address
            
            response_data = session_manager.get_user_bot_response(prompt_id, additional_info)
            
            if response_data:
                # Return the complete response data as JSON
                dispatcher.utter_message(json_message={
                    "message": "Contact information updated successfully!",
                    "prompt_id": prompt_id,
                    "data": response_data
                })
            else:
                dispatcher.utter_message(json_message={
                    "message": "Failed to update contact information",
                    "prompt_id": prompt_id
                })
                
        except Exception as e:
            logger.error(f"Error updating contact: {str(e)}")
            dispatcher.utter_message(json_message={
                "message": "Error connecting to server",
                "error": str(e)
            })
        
        return [SlotSet("phone_number", None), SlotSet("address", None)]

class ActionFetchActiveLoans(Action):
    """Fetches the user's active loans"""
    
    def name(self) -> Text:
        return "action_fetch_active_loans"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            # Initialize the session manager and get response from backend
            session_manager = SessionManager()
            prompt_id = get_prompt_id_for_intent("LOAN_ACTIVE_NUMBER")
            response_data = session_manager.get_user_bot_response(prompt_id)
            
            if response_data:
                # Check if we have loan options to present
                loan_options = []
                if 'extraAction' in response_data and 'loans' in response_data['extraAction']:
                    loans = response_data['extraAction']['loans']
                    for loan in loans:
                        if 'loan_id' in loan and 'type' in loan:
                            loan_options.append({
                                "title": f"{loan['type']} - {loan.get('loan_id')}",
                                "payload": f"/LOAN_ACTIVE_DETAILS{{\"loan_id\":\"{loan['loan_id']}\"}}"
                            })
                
                # Return the complete response data as JSON
                dispatcher.utter_message(json_message={
                    "message": "Here are your active loans:",
                    "prompt_id": prompt_id,
                    "data": response_data,
                    "options": loan_options
                })
            else:
                dispatcher.utter_message(json_message={
                    "message": "Failed to retrieve active loans",
                    "prompt_id": prompt_id
                })
                
        except Exception as e:
            logger.error(f"Error fetching active loans: {str(e)}")
            dispatcher.utter_message(json_message={
                "message": "Error connecting to server",
                "error": str(e)
            })
        
        return []

class ActionFetchActiveLoanDetails(Action):
    """Fetches details of a specific active loan"""
    
    def name(self) -> Text:
        return "action_fetch_active_loan_details"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        loan_id = tracker.get_slot("active_loan_id")
        
        if not loan_id:
            # Try to get loan_id from the latest entity
            for entity in tracker.latest_message.get('entities', []):
                if entity['entity'] == 'loan_id':
                    loan_id = entity['value']
                    break
        
        if not loan_id:
            dispatcher.utter_message(json_message={
                "message": "Please select a specific loan to view its details.",
                "request_slot": "active_loan_id"
            })
            return []
        
        try:
            # Initialize the session manager and get response from backend
            session_manager = SessionManager()
            prompt_id = get_prompt_id_for_intent("LOAN_ACTIVE_DETAILS")
            response_data = session_manager.get_user_bot_response(prompt_id, loan_id)
            
            if response_data:
                # Return the complete response data as JSON
                dispatcher.utter_message(json_message={
                    "message": "Here are the details of your selected loan:",
                    "prompt_id": prompt_id,
                    "loan_id": loan_id,
                    "data": response_data,
                    "options": [
                        {"title": "View EMI Schedule", "payload": f"/LOAN_EMI_DETAILS{{\"loan_id\":\"{loan_id}\"}}"} 
                    ]
                })
            else:
                dispatcher.utter_message(json_message={
                    "message": "Failed to retrieve loan details",
                    "prompt_id": prompt_id,
                    "loan_id": loan_id
                })
                
        except Exception as e:
            logger.error(f"Error fetching loan details: {str(e)}")
            dispatcher.utter_message(json_message={
                "message": "Error connecting to server",
                "error": str(e)
            })
        
        return [SlotSet("active_loan_id", loan_id)]

class ActionFetchEMIDetails(Action):
    """Fetches EMI details for a specific loan"""
    
    def name(self) -> Text:
        return "action_fetch_emi_details"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        loan_id = tracker.get_slot("active_loan_id")
        
        if not loan_id:
            # Try to get loan_id from the latest entity
            for entity in tracker.latest_message.get('entities', []):
                if entity['entity'] == 'loan_id':
                    loan_id = entity['value']
                    break
        
        if not loan_id:
            dispatcher.utter_message(json_message={
                "message": "Please select a specific loan to view its EMI schedule.",
                "request_slot": "active_loan_id"
            })
            return []
        
        try:
            # Initialize the session manager and get response from backend
            session_manager = SessionManager()
            prompt_id = get_prompt_id_for_intent("LOAN_EMI_DETAILS")
            response_data = session_manager.get_user_bot_response(prompt_id, loan_id)
            
            if response_data:
                # Return the complete response data as JSON
                dispatcher.utter_message(json_message={
                    "message": "Here is the EMI schedule for your selected loan:",
                    "prompt_id": prompt_id,
                    "loan_id": loan_id,
                    "data": response_data
                })
            else:
                dispatcher.utter_message(json_message={
                    "message": "Failed to retrieve EMI schedule",
                    "prompt_id": prompt_id,
                    "loan_id": loan_id
                })
                
        except Exception as e:
            logger.error(f"Error fetching EMI details: {str(e)}")
            dispatcher.utter_message(json_message={
                "message": "Error connecting to server",
                "error": str(e)
            })
        
        return [SlotSet("active_loan_id", loan_id)]

class ActionFetchLoanStatus(Action):
    """Fetches status of all loan applications"""
    
    def name(self) -> Text:
        return "action_fetch_loan_status"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            # Initialize the session manager and get response from backend
            session_manager = SessionManager()
            prompt_id = get_prompt_id_for_intent("LOAN_STATUS")
            response_data = session_manager.get_user_bot_response(prompt_id)
            
            if response_data:
                # Return the complete response data as JSON
                dispatcher.utter_message(json_message={
                    "message": "Here is the status of your loan applications:",
                    "prompt_id": prompt_id,
                    "data": response_data
                })
            else:
                dispatcher.utter_message(json_message={
                    "message": "Failed to retrieve loan application status",
                    "prompt_id": prompt_id
                })
                
        except Exception as e:
            logger.error(f"Error fetching loan status: {str(e)}")
            dispatcher.utter_message(json_message={
                "message": "Error connecting to server",
                "error": str(e)
            })
        
        return []

class ActionAddBank(Action):
    """Adds a new bank account"""
    
    def name(self) -> Text:
        return "action_add_bank"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        account_number = tracker.get_slot("account_number")
        account_holder_name = tracker.get_slot("account_holder_name")
        ifsc_code = tracker.get_slot("ifsc_code")
        bank_name = tracker.get_slot("bank_name")
        bank_account_type = tracker.get_slot("bank_account_type")
        
        # Validate required fields
        if not all([account_number, account_holder_name, ifsc_code, bank_name, bank_account_type]):
            missing_fields = []
            if not account_number:
                missing_fields.append("Account Number")
            if not account_holder_name:
                missing_fields.append("Account Holder Name")
            if not ifsc_code:
                missing_fields.append("IFSC Code")
            if not bank_name:
                missing_fields.append("Bank Name")
            if not bank_account_type:
                missing_fields.append("Bank Account Type")
            
            dispatcher.utter_message(json_message={
                "message": f"Please provide all required fields: {', '.join(missing_fields)}",
                "missing_fields": missing_fields
            })
            return [SlotSet("requested_form_info", "bank_add")]
        
        # Validate bank account type
        if bank_account_type not in ["SAVINGS", "CURRENT"]:
            dispatcher.utter_message(json_message={
                "message": "Bank Account Type must be either SAVINGS or CURRENT.",
                "invalid_field": "bank_account_type"
            })
            return [SlotSet("bank_account_type", None)]
        
        try:
            # Initialize the session manager and get response from backend
            session_manager = SessionManager()
            prompt_id = get_prompt_id_for_intent("BANK_ADD")
            
            # Format bank details as a pipe-separated string for the additional parameter
            bank_details = f"{account_number}|{account_holder_name}|{ifsc_code}|{bank_name}|{bank_account_type}"
            
            response_data = session_manager.get_user_bot_response(prompt_id, bank_details)
            
            if response_data:
                # Return the complete response data as JSON
                dispatcher.utter_message(json_message={
                    "message": "Bank account added successfully!",
                    "prompt_id": prompt_id,
                    "data": response_data
                })
            else:
                dispatcher.utter_message(json_message={
                    "message": "Failed to add bank account",
                    "prompt_id": prompt_id
                })
                
        except Exception as e:
            logger.error(f"Error adding bank account: {str(e)}")
            dispatcher.utter_message(json_message={
                "message": "Error connecting to server",
                "error": str(e)
            })
        
        return [
            SlotSet("account_number", None),
            SlotSet("account_holder_name", None),
            SlotSet("ifsc_code", None),
            SlotSet("bank_name", None),
            SlotSet("bank_account_type", None)
        ]

class ActionUpdateBank(Action):
    """Updates an existing bank account"""
    
    def name(self) -> Text:
        return "action_update_bank"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        bank_id = tracker.get_slot("active_bank_id")
        account_holder_name = tracker.get_slot("account_holder_name")
        bank_account_type = tracker.get_slot("bank_account_type")
        
        if not bank_id:
            # Try to get bank_id from the latest entity
            for entity in tracker.latest_message.get('entities', []):
                if entity['entity'] == 'bank_id':
                    bank_id = entity['value']
                    break
        
        if not bank_id:
            dispatcher.utter_message(json_message={
                "message": "Please select a specific bank account to update.",
                "request_slot": "active_bank_id"
            })
            return []
        
        # Validate required fields
        if not account_holder_name and not bank_account_type:
            dispatcher.utter_message(json_message={
                "message": "Please provide at least one field to update: Account Holder Name or Bank Account Type.",
                "request_slots": ["account_holder_name", "bank_account_type"]
            })
            return [SlotSet("requested_form_info", "bank_update")]
        
        # Validate bank account type if provided
        if bank_account_type and bank_account_type not in ["SAVINGS", "CURRENT"]:
            dispatcher.utter_message(json_message={
                "message": "Bank Account Type must be either SAVINGS or CURRENT.",
                "invalid_field": "bank_account_type"
            })
            return [SlotSet("bank_account_type", None)]
        
        try:
            # Initialize the session manager and get response from backend
            session_manager = SessionManager()
            prompt_id = get_prompt_id_for_intent("BANK_UPDATE")
            
            # Format bank update details for the additional parameter
            # Include blank placeholders for values that aren't being updated
            update_details = f"{bank_id}|{account_holder_name or ''}|{bank_account_type or ''}"
            
            response_data = session_manager.get_user_bot_response(prompt_id, update_details)
            
            if response_data:
                # Return the complete response data as JSON
                dispatcher.utter_message(json_message={
                    "message": "Bank account updated successfully!",
                    "prompt_id": prompt_id,
                    "data": response_data
                })
            else:
                dispatcher.utter_message(json_message={
                    "message": "Failed to update bank account",
                    "prompt_id": prompt_id,
                    "bank_id": bank_id
                })
                
        except Exception as e:
            logger.error(f"Error updating bank account: {str(e)}")
            dispatcher.utter_message(json_message={
                "message": "Error connecting to server",
                "error": str(e)
            })
        
        return [
            SlotSet("active_bank_id", bank_id),
            SlotSet("account_holder_name", None),
            SlotSet("bank_account_type", None)
        ]

class ActionFetchLinkedBanks(Action):
    """Fetches user's linked bank accounts"""
    
    def name(self) -> Text:
        return "action_fetch_linked_banks"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            # Initialize the session manager and get response from backend
            session_manager = SessionManager()
            prompt_id = get_prompt_id_for_intent("BANK_LINKED_NUMBER")
            
            response_data = session_manager.get_user_bot_response(prompt_id)
            
            if response_data:
                # Check if we have bank options to present
                bank_options = []
                if 'extraAction' in response_data and 'bankDetails' in response_data['extraAction']:
                    banks = response_data['extraAction']['bankDetails']
                    for bank in banks:
                        if 'bankId' in bank and 'bankName' in bank:
                            bank_options.append({
                                "title": f"{bank['bankName']} - {bank.get('accountNumber', 'N/A')}",
                                "payload": f"/BANK_LINKED_DETAILS{{\"bank_id\":\"{bank['bankId']}\"}}"
                            })
                
                # Return the complete response data as JSON
                dispatcher.utter_message(json_message={
                    "message": "Here are your linked bank accounts:",
                    "prompt_id": prompt_id,
                    "data": response_data,
                    "options": bank_options
                })
            else:
                dispatcher.utter_message(json_message={
                    "message": "Failed to retrieve linked banks",
                    "prompt_id": prompt_id
                })
                
        except Exception as e:
            logger.error(f"Error fetching linked banks: {str(e)}")
            dispatcher.utter_message(json_message={
                "message": "Error connecting to server",
                "error": str(e)
            })
        
        return []

class ActionFetchBankDetails(Action):
    """Fetches details of a specific bank account"""
    
    def name(self) -> Text:
        return "action_fetch_bank_details"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        bank_id = tracker.get_slot("active_bank_id")
        
        if not bank_id:
            # Try to get bank_id from the latest entity
            for entity in tracker.latest_message.get('entities', []):
                if entity['entity'] == 'bank_id':
                    bank_id = entity['value']
                    break
        
        if not bank_id:
            dispatcher.utter_message(json_message={
                "message": "Please select a specific bank account to view its details.",
                "request_slot": "active_bank_id"
            })
            return []
        
        try:
            # Initialize the session manager and get response from backend
            session_manager = SessionManager()
            prompt_id = get_prompt_id_for_intent("BANK_LINKED_DETAILS")
            
            response_data = session_manager.get_user_bot_response(prompt_id, bank_id)
            
            if response_data:
                # Return the complete response data as JSON
                dispatcher.utter_message(json_message={
                    "message": "Here are the details of your selected bank account:",
                    "prompt_id": prompt_id,
                    "bank_id": bank_id,
                    "data": response_data,
                    "options": [
                        {"title": "Update Bank Details", "payload": f"/navigate_bank_update{{\"bank_id\":\"{bank_id}\"}}"} 
                    ]
                })
            else:
                dispatcher.utter_message(json_message={
                    "message": "Failed to retrieve bank account details",
                    "prompt_id": prompt_id,
                    "bank_id": bank_id
                })
                
        except Exception as e:
            logger.error(f"Error fetching bank details: {str(e)}")
            dispatcher.utter_message(json_message={
                "message": "Error connecting to server",
                "error": str(e)
            })
        
        return [SlotSet("active_bank_id", bank_id)]

class ActionHandleBankQuery(Action):
    """General handler for bank-related queries"""
    
    def name(self) -> Text:
        return "action_handle_bank_query"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # This is a general handler that routes to the appropriate bank action
        # Provide a menu of bank options
        dispatcher.utter_message(json_message={
            "message": "I can help you with your bank accounts. What would you like to do?",
            "options": [
                {"title": "View linked bank accounts", "payload": "/BANK_LINKED_NUMBER"},
                {"title": "Add new bank account", "payload": "/navigate_bank_add"}
            ]
        })
        
        return []

class ValidateUpdateSalaryForm(FormValidationAction):
    """Validates the update_salary_form"""
    
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
                "message": "Please enter a valid salary amount.",
                "request_slot": "salary_amount"
            })
            return {"salary_amount": None}
        
        # Try to convert to a number and validate
        try:
            # Remove any non-numeric characters except decimal point
            cleaned_value = re.sub(r'[^\d.]', '', str(slot_value))
            salary = float(cleaned_value)
            
            if salary <= 0:
                dispatcher.utter_message(json_message={
                    "message": "Salary amount must be greater than zero.",
                    "request_slot": "salary_amount"
                })
                return {"salary_amount": None}
            
            return {"salary_amount": str(salary), "requested_form_info": "salary_updated"}
            
        except ValueError:
            dispatcher.utter_message(json_message={
                "message": "Please provide a valid numeric salary amount.",
                "request_slot": "salary_amount"
            })
            return {"salary_amount": None}

class ValidateUpdateContactForm(FormValidationAction):
    """Validates the update_contact_form"""
    
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
        
        # Validate phone number format (simple validation for India)
        if not re.match(r'^[6-9]\d{9}$', str(slot_value)):
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

class ValidateAddBankForm(FormValidationAction):
    """Validates the add_bank_form"""
    
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
        
        # Simple validation for account number
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
        
        # Basic validation for name
        if len(str(slot_value).split()) < 2:
            dispatcher.utter_message(json_message={
                "message": "Please provide full name with at least first and last name.",
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
        
        # IFSC code validation for India
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
        
        # Basic validation for bank name
        if len(str(slot_value)) < 2:
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

class ValidateUpdateBankForm(FormValidationAction):
    """Validates the update_bank_form"""
    
    def name(self) -> Text:
        return "validate_update_bank_form"
        
    def validate_account_holder_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate account_holder_name value."""
        
        # This is optional if bank_account_type is provided
        bank_account_type = tracker.get_slot("bank_account_type")
        if not slot_value and bank_account_type:
            return {"account_holder_name": None}
        
        if not slot_value:
            return {"account_holder_name": None}
        
        # Basic validation for name
        if len(str(slot_value).split()) < 2:
            dispatcher.utter_message(json_message={
                "message": "Please provide full name with at least first and last name.",
                "request_slot": "account_holder_name"
            })
            return {"account_holder_name": None}
        
        return {"account_holder_name": slot_value}
    
    def validate_bank_account_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate bank_account_type value."""
        
        # This is optional if account_holder_name is provided
        account_holder_name = tracker.get_slot("account_holder_name")
        if not slot_value and account_holder_name:
            return {"bank_account_type": None, "requested_form_info": "bank_updated"}
        
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
        
        return {"bank_account_type": str(slot_value).upper(), "requested_form_info": "bank_updated"}