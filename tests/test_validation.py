from dotenv import load_dotenv
from agent.validation_agent import ValidationAgent
load_dotenv()
validation_agent=ValidationAgent()
relation={
    "source":"chest pain",
    "relationship":"RELATED_TO",
    "target":"myocardial infarction"
}
result=validation_agent.classify_with_reason(
    relation
)
print(result)