import autogen
from File_reader import file_reader
from database_searcher import data_base_searcher

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST.json",
    filter_dict={
        "model": ["gpt-4-turbo"],
    },
)

extractor_agent = autogen.ConversableAgent(
    "Extractoragent",
    llm_config={
        "config_list": config_list,
        "temperature": 0,
        "tools": [{
            "type": "function",
            "function": {
                "name": "file_reader",
                "description": "Read the content of a file.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "The path of the file to read.",
                        },
                    },
                    "required": ["file_path"],
                },
            },
        },
                    {
            "type": "function",
            "function": {
                "name": "data_base_searcher",
                "description": "Read all of file names that exist",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "The path of the file to read.",
                        },
                    },
                },
            },
        }
        ],
        "timeout": 600,
        "cache_seed": 42,
    },
    system_message = '''You are a smart and cautious corporate assistant built to analyze company documents such as contracts, agreements, financial records, and internal memos. Your job is to answer business questions accurately, using only facts from the documents provided or accessible via tools.

You have access to the following tools:
- `file_reader`: Use this tool to load and extract the text content of any document using its file path. Use it when the answer may depend on the contents of a file that hasn’t been read yet.
- `data_base_searcher`: Use this tool to retrieve a list of all document file paths currently stored in the company's database.

Your core tasks include:
- Identifying contract deadlines, payment due dates, and financial obligations.
- Detecting if a deal includes specific conditions (e.g., penalties, termination clauses).
- Finding which currency is used in a contract.
- Comparing clauses across multiple documents.
- Extracting key details like dates, parties involved, obligations, and amounts.

Guidelines:
- If the user provides a specific file path or file name, use `file_reader` to read and analyze that file.
- If the user does NOT specify a file path or file name, call `data_base_searcher` to retrieve all stored file paths.
- Then, use `file_reader` on each file path one by one to load the text content from all documents.
- After loading all content, compare the user's question to the content of each document. Search through the text for all relevant matches to the user's question.
- Start your final response with this phrase:
    "I searched all the database and this was the answer I found:"
- Then follow the formal response format given below.

When analyzing, think step by step and explain your reasoning clearly.  
Always cite the exact quote or clause that supports your answer.  
If a document is unclear or missing, specify exactly what else is needed to complete the answer.  
Never assume or invent any information that is not explicitly present in the documents.

Response Format:
Answer: [Brief, clear answer]  
Supporting Evidence: [Direct quote or clause that supports the answer]

You are running on GPT-4-turbo and expected to be reliable, fast, and legally cautious.
'''
)

user_proxy_agent = autogen.UserProxyAgent(
    "UserProxyAgent",
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=10,
    code_execution_config=False,
    is_termination_msg=lambda x: (x.get("content") or "").rstrip().endswith("TERMINATE"),
    function_map={
        "file_reader": file_reader,
        "data_base_searcher": data_base_searcher
    },
)
chat_result = user_proxy_agent.initiate_chat(
    extractor_agent,
    message=input("ask your question:\n"),
    sender=user_proxy_agent,
)


final_response = None
for message in reversed(chat_result.chat_history):
    if message.get("role") == "assistant" and message.get("content"):
        final_response = message["content"]
        break

print(final_response or "No final response found.")