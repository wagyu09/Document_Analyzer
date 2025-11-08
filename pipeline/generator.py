import ollama
import prompts, config
class Generator:
    def __init__(self, model_name = 'gpt-oss:20b', options = None):
        self.model_name = model_name
        if options == None:
            self.options = config.DEFAULT_OLLAMA_OPTIONS
        else:
            self. options = options
        self.prompt_template = prompts.SYSTEM_PROMPT
        self.prompt = ''

    def generate(self, retrieved_data, query):
        self.prompt = self.prompt_template.format(retrieved_data = retrieved_data, query = query)
        response = ollama.chat(
        model = self.model_name,
        messages = [
            {'role' : 'user', 'content' : self.prompt}
        ],
        options = self.options,
        )
        outputs = response['message']['content']

        return outputs

      
