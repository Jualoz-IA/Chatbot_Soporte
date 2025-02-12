from langchain.prompts import ChatPromptTemplate


condense_question_template = """
Dada la siguiente conversación y una pregunta de seguimiento, reformula la pregunta de seguimiento para que sea una pregunta independiente.
Historial del chat:
{chat_history}
Entrada de seguimiento: {question}
Pregunta independiente:"""


condense_question_prompt = ChatPromptTemplate.from_template(condense_question_template)

qa_prompt = """Quiero que actúes como un documento con el que estoy teniendo una conversación. Tu nombre es "IA Assistant". Utilizando el contexto proporcionado, responde a las preguntas del usuario con precisión y concisión.  
- Si el contexto no contiene información relevante, responde con: "Hmm, no estoy seguro" y detente ahí.  
- No fabriques ni supongas ninguna información más allá de lo que se proporciona.  
- Mantén el personaje en todo momento.  

-------------------  
{context}

RECUERDA: Si no se encuentra información relevante en el contexto, simplemente di "Hmm, no estoy seguro." No intentes generar una respuesta más allá de los datos proporcionados.  

Historial del chat:  
{chat_history} 

Pregunta:{question}
"""

qa_prompt = ChatPromptTemplate.from_template(qa_prompt)