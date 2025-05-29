from openai import OpenAI
import autogen
 
config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4-turbo"],
    },
)
metis_api_key = "tpsg-ZNJvTm228gzSX45f6HjplQVjl4P3e4H"
client = OpenAI(api_key = metis_api_key, base_url="https://api.metisai.ir/openai/v1")
 
 