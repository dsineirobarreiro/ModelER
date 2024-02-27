from llama_cpp import Llama
from typing import Optional
from llama_cpp import LogitsProcessorList
from lmformatenforcer import CharacterLevelParser
from lmformatenforcer.integrations.llamacpp import build_llamacpp_logits_processor
from lmformatenforcer import JsonSchemaParser
from pydantic import BaseModel, Field
from typing import List

model_path = 'C:/Users/dsine/Documents/Models/llama-2-7b-chat.Q5_K_M.gguf'
llm = Llama(model_path, n_gpu_layers=8, n_ctx=4096)

# Define your desired data structure.
class Entity(BaseModel):
    name: str = Field(description="entity name from the case scenario")
    attributes: Optional[List[str]] = Field(description="colection of attributes from the entity")

class Relation(BaseModel):
    name: str = Field(description='name of the relation')
    source: str = Field(description='source entity of the relation')
    target: str = Field(description='target entity of the relation')

class Main(BaseModel):
    entities: List[Entity] = Field("Entity from the case scenario")
    relations: Optional[List[Relation]] = Field(description="colection of relations from the entities")

DEFAULT_SYSTEM_PROMPT = """\
You are a helpful assitant that extracts entities with its attributes and relations for ER modeling.
"""

def get_prompt(message: str, system_prompt: str = DEFAULT_SYSTEM_PROMPT, start: bool = True) -> str:
    return f'<s>[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n{message} [/INST]' if start else f'<s>[INST] {message} [/INST]'

def llamacpp_with_character_level_parser(text: str, llm: Llama = llm, character_level_parser: Optional[CharacterLevelParser] = JsonSchemaParser(Main.schema())) -> str:
    logits_processors: Optional[LogitsProcessorList] = None
    if character_level_parser:
        logits_processors = LogitsProcessorList([build_llamacpp_logits_processor(llm, character_level_parser)])
    
    prompt = text + 'You MUST answer using the following json schema:'
    prompt_with_schema = f'{prompt}\n{Main.schema()}\nThe entities, attributes and relations in the text are:'
    output = llm(get_prompt(prompt_with_schema.strip()), logits_processor=logits_processors, max_tokens=-1)
    text: str = output['choices'][0]['text']
    return text
