import autogen
from File_reader import file_reader

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
        ],
        "timeout": 600,
        "cache_seed": 42,
    },
    system_message='''You are a smart and cautious corporate assistant built to analyze company documents such as contracts, agreements, financial records, and internal memos. Your job is to answer business questions accurately, using only facts from the documents provided or accessible via tools.
    You have access to the following tool:
    - `file_reader`: Use this tool to load and extract the text content of any document provided by the user. Use it when the answer may depend on the contents of a file that hasn’t been read yet.
    Your core tasks include:
    - Identifying contract deadlines, payment due dates, and financial obligations.
    - Detecting if a deal includes specific conditions (e.g., penalties, termination clauses).
    - Finding which currency is used in a contract.
    - Comparing clauses across multiple documents.
    - Extracting key details like dates, parties involved, obligations, and amounts.
    Guidelines:
    - Always use the `file_reader` tool when you are asked about a document that hasn't yet been read.
    - When analyzing, think step by step and explain your reasoning clearly.
    - Always cite the source text or clause that supports your answer.
    - If a document is unclear or missing, say exactly what else is needed to answer.
    - Never assume or invent information that isn't explicitly present.
    Response Format:
    Answer: [Brief, clear answer]  
    Supporting Evidence: [Direct quote or clause that supports the answer]
    You are running on GPT-4-turbo and expected to be reliable, fast, and legally cautious.
    ''')

user_proxy_agent = autogen.UserProxyAgent(
    "UserProxyAgent",
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=4,
    code_execution_config=False,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    function_map={
        "file_reader": file_reader
    },
)
chat_result = user_proxy_agent.initiate_chat(
    extractor_agent,
    message="Please analyze the contract 'Asset Purchase Agreement - SD Acquisition Inc. and Transgenomic Inc. - Sample Contracts and Business Forms.pdf'.",
    sender=extractor_agent,
)

final_response = chat_result.chat_history
if chat_result.chat_history and chat_result.chat_history[-1].get('content'):
    final_response = chat_result.chat_history[-1].get('content')
print(final_response)