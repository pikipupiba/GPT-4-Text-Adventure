import json
from typing import List, Tuple
from loguru import logger

class LLM:
    def build_openai_history_array(self, raw_history):
        
        history_openai_format = []

        # Convert history to OpenAI format
        for human, assistant in raw_history:
            if human != None: history_openai_format.append({"role": "user", "content": human })
            if assistant != None: history_openai_format.append({"role": "assistant", "content":assistant})

        return history_openai_format


    def build_openai_system_message(self, system_message: str = None):



        system_message_openai_format = {
            "role": "system",
            "content": complete_system_message
        }

        return system_message_openai_format

    def predict(self, model, system_message, example_history, history):
        
        messages_openai_format = []

        # Append system message to history
        messages_openai_format.append(self.build_openai_system_message(system_message))
        messages_openai_format += self.build_openai_history_array(history, example_history)

        # OpenAI API call
        response = openai.ChatCompletion.create(
            model=model,
            messages= messages_openai_format,         
            temperature=1.0,
            stream=True
        )
        

        # Variables to capture JSON objects in the response
        inside_json=False
        json_string=""
        found_json_schema=None

        # Parse the response one chunk at a time
        self.history[-1][1] = ""
        self.raw_history[-1][1] = ""
        for chunk in response:
            if len(chunk["choices"][0]["delta"]) == 0:
                break

            # print(self.raw_history[-1][1])
            # See what model the api actually used. This is important for tracking tokens.
            real_model = chunk.get("model", model)
            # if len(chunk["choices"][0]["delta"]) != 0:
            content = chunk["choices"][0]["delta"]["content"]

            # Add everything to raw history
            self.raw_history[-1][1] += content
            # Don't add chunks to the chatbot if they are part of a JSON object
            # Continue until the JSON object is complete
            if inside_json:
                json_string += content

                try:
                    new_json = json.loads(json_string)
                    if "Stats_Schema" in new_json:
                        self.stats = new_json
                        self.history[-1][1] += " COMPLETE!!!\n\n"
                    elif "Combat_Schema" in new_json:
                        self.combat = new_json
                        if self.combat["Combat_Schema"]["success"] == True:
                            self.history[-1][1] += " SUCCESS!!!\n\n"
                        else:
                            self.history[-1][1] += " FAILURE!!!\n\n"
                    logger.info(new_json)

                    inside_json=False
                    json_string=""
                    found_json_schema=None
                        
                except json.JSONDecodeError:
                
                    if found_json_schema == None:
                        if "Stats_Schema" in json_string:
                            logger.info("Found Stats_Schema!")
                            found_json_schema="Stats_Schema"
                            self.history[-1][1] += " Calculating stats "
                        elif "Combat_Schema" in json_string:
                            logger.info("Found Combat_Schema!")
                            found_json_schema="Combat_Schema"
                            self.history[-1][1] += " Calculating combat "
                    else:
                        if len(json_string)%5 == 0:
                            self.history[-1][1] += "-"
            else:
                # Found the start of a JSON object
                if content == "{\"":
                    inside_json=True
                    json_string += content
                    self.history[-1][1] += "\n\n---"
                # Send response chunks to the chatbot
                else:
                    # print(content)
                    self.history[-1][1] += content
                
            yield self.history

        # print(self.raw_history[-1][1])
        # Calculate streaming token usage
        self.token_trackers[real_model].add_from_stream(real_model, messages_openai_format, self.raw_history[-1][1])

        # logger.info(f"~~--------~~ {model} ~~--------~~")
        # self.token_trackers[real_model].print()