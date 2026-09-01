import asyncio
from typing import AsyncGenerator, List, Dict
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage
from app.core.config import settings
from app.services.retriever import get_retriever
from app.services.memory import get_history, add_message

llm = ChatOllama(
    model="llama3.2",
    temperature=0.7,
)

def _build_messages(history: List[Dict[str, str]], context: str, user_message: str) -> List:
    system_prompt = f"""You are a helpful customer-support assistant.
Use the following context to answer the user's question. If the answer is not in the context, say you don't know.

Context:
{context}"""

    messages = [HumanMessage(content=system_prompt)]
    for item in history:
        if item["role"] == "human":
            messages.append(HumanMessage(content=item["content"]))
        else:
            messages.append(AIMessage(content=item["content"]))
    messages.append(HumanMessage(content=user_message))
    return messages

async def generate_answer(session_id: str, user_message: str) -> AsyncGenerator[str, None]:
    # 1. Load history
    history = await get_history(session_id)

    # 2. Retrieve relevant documents (run in thread to avoid blocking)
    retriever = get_retriever()
    docs = await asyncio.to_thread(retriever.invoke, user_message)  # <-- fixed
    context = "\n\n".join([doc.page_content for doc in docs])

    # 3. Build messages
    messages = _build_messages(history, context, user_message)

    # 4. Store user message BEFORE streaming
    await add_message(session_id, "human", user_message)

    # 5. Stream response
    full_answer = ""
    async for chunk in llm.astream(messages):
        full_answer += chunk.content
        yield chunk.content

    # 6. Store AI response after streaming completes
    await add_message(session_id, "ai", full_answer)