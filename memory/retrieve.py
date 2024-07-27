import re
from memory.db import search_items
from groq import Groq
from memory.config import GROQ_API

def retrive(text):
    client = Groq(api_key=GROQ_API)
    prompt = "You are an AI. Your role is to identify anything needed from the list below to answer the prompt provided. This includes long-term memory retrieval, short term memory retrieval, and command retrieval. Do not include any other text other than what I ask you to say below. Remember You can ask for multiple files and memory items, but only request what you need, and place each item in brackets no matter how many requests you're putting in, separated by a comma. If there is nothing to retrieve then just respond with “no-retrieval”. Make sure keywords are simple and get right to the point. For each thing you're retrieving, wrap it in [] separated by a coma. Here's what you need to know: Memory Retrieval: Memory Retrieval is for you to retrieve long term or short term memory. You get to decide whether or not you want to retrieve long term or short term so think wisely, if you are really unsure you can check both using all-memory-retrieval. Long term memory is for you to get personal things about me so use keywords that i would put into my long term memory. Only retrieve what you need, you don’t need to request anything if it's not important, remember to use at least 7 key words so it’s easier for me to retrieve it. Long-Term: Retrieve data such as important dates, personal preferences, personal goals, smart home devices, etc. When you request long-term memory, use this format, don’t change anything about this format, keep all brackets and parentheses, everything: [Long-Term-Memory: (7 Keywords)]. File Retrieval: Retrieve commands such as controlling smart home devices by turning them on or off. Use common sense to decide for example if i say turn on fan light if that has anything to do with commands, if it does don’t say it's a long-term-memory and just retrieve the command. When you request long-term memory, use this format, don’t change anything about this format, keep all brackets and parentheses, everything: [File-Retrieval: (file-name)]. Use the following file names for command retrieval: smarthome.py tts.py To request a file or memory, use this format, don’t change anything about this format, keep all brackets and parentheses, everything: [file-retrieval: (file name)] or [Long-Term-Memory: (7 Keywords)]. You can ask for multiple files and memory items, but only request what you need, and place each new item in brackets, no matter what, separated by a comma. Include at least 7 keywords for everything. Keep everything very specific, no vague keywords. Make sure to only request what you need! Prompt:"
    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {
                "role": "user",
                "content": prompt +  text
            }
        ],
        "temperature": 1,
        "max_tokens": 1024,
        "top_p": 1,
        "stream": False,
        "stop": None
    }

    response = client.chat.completions.create(**data)
    response_content = response.choices[0].message.content

    if not response_content:
        return "The generation failed."
    output = process_prompt(response_content)
    # print(output)
    return output

def classify_memory_type(response):
    response = response.lower()
    if "long-term-memory" in response:
        return "long-term-memory"
    elif "file-retrieval" in response:
        return "file-retrieval"
    else:
        return "unknown"

def extract_keywords(response):
    keywords = re.findall(r'\((.*?)\)', response)
    if keywords:
        return [keyword.strip() for keyword in keywords[0].split(',')]
    return []

def process_prompt(prompt):
    responses = re.findall(r'\[.*?\]', prompt)
    response_count = len(responses)
    processed_responses = []
    for response in responses:
        memory_type = classify_memory_type(response)
        keywords = extract_keywords(response)
        processed_responses.append({
            "type": memory_type,
            "keywords": keywords
        })
    output = f"Total Responses: {response_count}\n"
    for idx, res in enumerate(processed_responses, start=1):
        output += f"Response {idx}:\n"
        output += f"  Type: {res['type']}\n"
        output += f"  Keywords: {', '.join(res['keywords'])}\n"
        if res['keywords']:
            try:
                results = search_items(res['keywords'])
                output += f"  Results: {results}\n"
            except Exception as e:
                output += f"  Error in search: {str(e)}\n"
        else:
            output += "  No keywords to search.\n"
    
    return output


# retrive("whats my dogs birthday")