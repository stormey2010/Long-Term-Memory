import re
from groq import Groq
from plugins.current_time import get_current_time
from memory.db import insert_item
from memory.config import GROQ_API, ASSISTANTNAME, NAME

def extract_memories(prompt_output):
    memories_str = re.findall(r'\[(.*?)\]', prompt_output, re.DOTALL)
    if not memories_str:
        return 0, []
    memories = []
    for memory_str in memories_str:
        parts = re.split(r'\],\s*', memory_str)
        for part in parts:
            if not part.endswith(']'):
                part += ']'
            part = re.sub(r'[()]', '', part)
            memories.append(part.strip())
    num_memories = len(memories)
    return num_memories, memories


def memory_set(text):
    client = Groq(api_key=GROQ_API)
    prompt = "You are an AI, named " + ASSISTANTNAME + ". Your role is to identify anything needed from the list below to answer the prompt provided, including setting long-term memory if necessary. If you think there's anything in this prompt that should be remembered long-term, such as important dates like birthdays I've mentioned, or a friend's name, etc., use common sense to choose what to add to long-term memory. If you believe nothing should be remembered long-term, just say 'False'. Do not say anything else. If it needs to be remembered, follow these steps: State the title of the memory. Describe what should be remembered in a detailed 2-sentence description. Include the current time and date from "+ get_current_time() +", mentioning the month, day, year, and time only if necessary. Rate its importance from 1 to 5. Include at least 7 keywords, each consisting of up to 3 words for easy retrieval. Provide the information in this format: 'Title | Description | Importance | Keywords'. Use pipes to separate each part. If saving multiple memories, put each in brackets [] and separate them with commas. Ensure not to include anything about the future since it may be saved for a long time. Avoid keywords like '" + NAME + ", today, Personal Experience,' etc., unless necessary (e.g., " + NAME + " if saving my name). Use common sense for selecting keywords. Do not include extra explanations, only the essential information as requested. Additionally: Never use vague keywords; keep everything simple. Do not save anything to long-term memory if it is not about me, someone else, or something I or someone else did. For example, do not save user info or the current time itself. Ignore general information about the AI's role, memory storage guidelines, decision processes, or the current time and date unless they are part of a specific, relevant event. Here's an example of a good response: '[Pet Loss | " + NAME + "'s dog passed away on Thursday, July 25, 2024, use this for date remembrance, etc. | 5 | (Dog Passing, July 25 2024, Sad Event, Pet Loss, Heartfelt Moment)]', note this is just an example never use the exact same example. Keep separate memories distinct and ensure their keywords do not overlap. For example, if I have memories like 'my dog died today' and 'I went shopping at The Grove,' create separate entries and do not combine keywords.  Here's the prompt for your decision:"
    

    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {
                "role": "user",
                "content": prompt + text
            }
        ],
        "stream": False,
        "stop": None
    }

    response = client.chat.completions.create(**data)
    response_content = response.choices[0].message.content
    # print(response_content)

    if not response_content:
        return "The generation failed."
    num_memories, memories = extract_memories(response_content)
    # print(f"Number of memories: {num_memories}")
    for memory in memories:
        parts = memory.strip('[]').split('|', 3)
        if len(parts) >= 4:
            title, description, importance, keywords = parts
            # print(f"Title: {title.strip()}")
            # print(f"Description: {description.strip()}")
            # print(f"Importance: {importance.strip()}")
            # print(f"Keywords: {keywords.strip()}")
            insert_item(title.strip(), description.strip(), importance.strip(), keywords.strip())
        else:
            # print(f"Invalid memory format: {memory}")
            break
    return response_content
