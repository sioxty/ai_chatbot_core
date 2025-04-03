from enum import Enum

class Model(Enum): 
    QWEN_QWQ_32B = "Qwen/QwQ-32B"
    LLAMA_3_2_90B_VISION_INSTRUCT = "meta-llama/Llama-3.2-90B-Vision-Instruct"
    DEEPSEEK_R1 = "deepseek-ai/DeepSeek-R1"
    DEEPSEEK_R1_DISTILL_LLAMA_70B = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B"
    DEEPSEEK_R1_DISTILL_QWEN_32B = "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B"
    LLAMA_3_3_70B_INSTRUCT = "meta-llama/Llama-3.3-70B-Instruct"
    QWEN2_VL_7B_INSTRUCT = "Qwen/Qwen2-VL-7B-Instruct"
    DBRX_INSTRUCT = "databricks/dbrx-instruct"
    MINISTRAL_8B_INSTRUCT_2410 = "mistralai/Ministral-8B-Instruct-2410"
    CONFUCIUS_O1_14B = "netease-youdao/Confucius-o1-14B"
    ACE_MATH_7B_INSTRUCT = "nvidia/AceMath-7B-Instruct"
    LLAMA_3_1_NEMOTRON_70B_INSTRUCT = "neuralmagic/Llama-3.1-Nemotron-70B-Instruct-HF-FP8-dynamic"
    MISTRAL_LARGE_INSTRUCT_2411 = "mistralai/Mistral-Large-Instruct-2411"
    MICROSOFT_PHI_4 = "microsoft/phi-4"
    DOBBY_MINI_UNHINGED_Llama_3_1_8B = "SentientAGI/Dobby-Mini-Unhinged-Llama-3.1-8B"
    WATT_TOOL_70B = "watt-ai/watt-tool-70B"
    BESPOKE_STRATOS_32B = "bespokelabs/Bespoke-Stratos-32B"
    SKY_T1_32B_PREVIEW = "NovaSky-AI/Sky-T1-32B-Preview"
    FALCON3_10B_INSTRUCT = "tiiuae/Falcon3-10B-Instruct"
    C4AI_COMMAND_R_PLUS_08_2024 = "CohereForAI/c4ai-command-r-plus-08-2024"
    GLM_4_9B_CHAT = "THUDM/glm-4-9b-chat"
    QWEN2_5_CODER_32B_INSTRUCT = "Qwen/Qwen2.5-Coder-32B-Instruct"
    AYA_EXPANSE_32B = "CohereForAI/aya-expanse-32b"
    READER_LM_V2 = "jinaai/ReaderLM-v2"
    MINI_CPM3_4B = "openbmb/MiniCPM3-4B"
    QWEN2_5_1_5B_INSTRUCT = "Qwen/Qwen2.5-1.5B-Instruct"
    OZONE_AI_0X_LITE = "ozone-ai/0x-lite"
    PHI_3_5_MINI_INSTRUCT = "microsoft/Phi-3.5-mini-instruct"
    GRANITE_3_1_8B_INSTRUCT = "ibm-granite/granite-3.1-8b-instruct" 
    
class Message():
    def __init__(self,content,role="user"):
        self.role = role
        self.content = content
        
    def get_content(self)-> dict:
        return {"role": self.role, "content": self.content}
    
class StartMessage(Message):
    def __init__(self, content=None):
        if content is None:
            content = "You are a helpful assistant."
        super().__init__(content, "system")
