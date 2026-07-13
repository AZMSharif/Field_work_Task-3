"""
LogiTrack AI - Security and Compliance Guardrails
"""
import re
from langgraph.prebuilt.chat_agent_executor import create_react_agent
from langchain_core.messages import HumanMessage
from langchain.agents.middleware import before_model
from logistics_data import FRAUD_HISTORY

def extract_email(text: str) -> str:
    """Extract an email address from the user's message, if present."""
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else None


@before_model
def fraud_and_policy_guard(messages: list) -> list:
    """
    Security middleware that intercepts messages before they reach the LLM.
    - Blocks prompt injection / roleplay attacks.
    - Checks the user's email against the Fraud History database.
    - Halts execution (`jump_to="end"`) if violations are found, saving LLM tokens.
    """
    if not messages:
        return messages

    last_msg = messages[-1]
    
    # Only inspect messages from the human user
    if not isinstance(last_msg, HumanMessage) or not isinstance(last_msg.content, str):
        return messages
    
    text = last_msg.content.lower()
    
    # 1. Prompt Injection Protection
    suspicious_phrases = [
        "ignore previous instructions", 
        "system prompt", 
        "you are now", 
        "reveal your instructions"
    ]
    if any(phrase in text for phrase in suspicious_phrases):
        # Mutate the message into a hard rejection and halt execution
        messages[-1] = HumanMessage(content="[PROMPT INJECTION DETECTED]")
        return [{"role": "assistant", "content": "I can only assist with logistics, shipment tracking, and order-related inquiries. I'm unable to process that request."}, {"jump_to": "end"}]
    
    # 2. Fraud Detection
    email = extract_email(last_msg.content)
    if email and email in FRAUD_HISTORY:
        record = FRAUD_HISTORY[email]
        if record["claims_this_quarter"] >= 3 or record["status"] == "restricted":
            # Block the request without querying the LLM
            block_reason = record.get("flagged_reason", "Excessive claims detected.")
            reply = f"I'm sorry, but this account has been flagged by our system ({block_reason}). Please contact our fraud department at 1-800-555-0199 for further assistance. I cannot process claims or reshipments for this account."
            
            messages[-1] = HumanMessage(content=f"[FRAUD DETECTED - {email}]")
            return [{"role": "assistant", "content": reply}, {"jump_to": "end"}]

    # If all checks pass, allow the message through to the LLM
    return messages
