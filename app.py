from rag import rag_database_initialisation
from rag import answer_policy_question
from router import route
# from rag import initialize_rag

vector_db = rag_database_initialisation()
# print(
#     answer_policy_question("Do you insure pets?", vector_db)
# )



while True:
    question = input("\n> ")
    if question.lower() == "exit":
        break
    answer = route(question, vector_db)
    print("\n", answer)