from agents.base import Agent
from llama_cpp import Llama

class ItineraryAgent(Agent):
    def __init__(self, model_path):
        super().__init__("ItineraryAgent")
        self.llm = Llama(model_path=model_path, n_ctx=4096, temperature=0.7)

    def run(self, input_data):
        duration = input_data["duration"]
        destination = input_data["destination"]

        prompt = f"""
        Create a {duration}-day itinerary for {destination}
        in month {input_data['best_month']}.
        Hotel: {input_data['hotel']['name']}.
        """

        response = self.llm(prompt, max_tokens=600)

        return {"itinerary": response["choices"][0]["text"].strip()}