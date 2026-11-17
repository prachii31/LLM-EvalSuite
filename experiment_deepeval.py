
from deepeval.models import OllamaModel
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase

model = OllamaModel(
    model="qwen2.5:7b",
    base_url="http://localhost:11434",
    temperature=0
)

metric = AnswerRelevancyMetric(
    model=model,
    threshold=0.7,
    verbose_mode=True,
    async_mode=False
)

case = LLMTestCase(
    input="What is the daily ATM withdrawal limit?",
    actual_output="The daily ATM withdrawal limit is Rs. 25,000."
)

metric.measure(case)

print("Score:", metric.score)
print("Reason:", metric.reason)

