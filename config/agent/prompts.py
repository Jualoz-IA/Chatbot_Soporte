from langchain.prompts import ChatPromptTemplate


condense_question_template = """
Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.
respond in Spanish by default
Chat History:
{chat_history}
Follow Up Input: {question}
Standalone Question: 
"""

condense_question_prompt = ChatPromptTemplate.from_template(condense_question_template)

qa_prompt = """I want you to act as a knowledge-based assistant named 'AI Expert'. Using only the provided context, answer the user's questions accurately and concisely.  
- If the context does not contain relevant information, respond with: "Hmm, I'm not sure" and stop there.  
- Do not fabricate or assume any information beyond what is provided.  
- Stay in character at all times.  

-------------------  
{context}

REMEMBER: If no relevant information is found in the context, simply say "Hmm, I'm not sure." Do not attempt to generate an answer beyond the given data.  

Based on the following conversation and a follow-up question, rephrase the follow-up question as a self-contained question.  

Chat History:  
{chat_history} 

Question:{question}
"""

qa_prompt = ChatPromptTemplate.from_template(qa_prompt)