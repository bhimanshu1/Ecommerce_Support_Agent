import re
from tools import get_order
from rag import answer_policy_question


def extract_order_id(question: str):
    match = re.search(r"ORD\d+", question.upper())
    if match:
        return match.group()
    return None

def route(question, vector_db):
    order_id = extract_order_id(question)
    if order_id is None:
        return answer_policy_question(question, vector_db)
    
    question = question.lower()
    combined_keywords = [
        "return",
        "refund",
        "replace",
        "exchange",
        "eligible"
    ]

    for word in combined_keywords:
        if word in question:
            order = get_order(order_id)
            if order is None:
                return "Invalid order ID."
            
            combined_question = f"""
            Return policy for {order['category']}
            Customer asked:
            {question}
            Status:
            {order['status']}
            """
            return answer_policy_question(combined_question, vector_db)

    order = get_order(order_id) 
    if order == None:
        return "Product Not Found" 
    return order