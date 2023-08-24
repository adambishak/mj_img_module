import requests
import json
import re
import time

    # should be able to run grab_prompt with only a prompt parameter,
    # this means the prompt should probably be and object with components: referenced_message, upscales, prompt_string etc
    # then, a class specific list of prompt objects that you can add to with 
    # a new function, add_prompt and execute with run_prompt(s), would be nice, each should be executed consecutively if the user
    # wants, or the ability to run a certain prompt on the list and then maybe move it to a completed prompt list idk
    # which probably means making the list a dictionary with a job id so the user can know what they are accessing
    # this is should be done later because its gonna get complicated and not completely fleshed out.

    # need to test what happens when a user submits the same prompt twice, whether thats because they want multiple results
    # or an accident, it should return those prompts without error which Im not sure if it will,

    # need to use regular expressions to remove all characters from prompts to avoid messing up grab prompt

    # I also want to make it so that grab_prompt is private within the function because its not something that the user
    # should interact with. 
    
    # I would also like to add the ability to change resolution, submit an image, pan and basically just
    # add other midjourney features. 
    
    # Ultimately it would be nice to make it so this whole proccess is routed through an api
    # and the user just adds a discord bot to their server, but Id like to complete the above features first.

class ImageBot:
    def __init__(self, prompt):
        with open("./params.json", "r") as params_file:
            params = json.load(params_file)
            self.authorization = {params['authorization']
            }
            self.channel_id=params['channelid']
            self.authorization=params['authorization']
            self.application_id = params['application_id']
            self.guild_id = params['guild_id']
            self.session_id = params['session_id']
            self.version = params['version']
            self.id = params['id']
            self.prompt = str(prompt)
            self.header = {'authorization': self.authorization}

    def grab_prompt(self, upscale, upscale_num, message_id):
        while True:
            r = requests.get(f"https://discord.com/api/v10/channels/{self.channel_id}/messages?limit={100}", headers= self.header)
            messages_json = json.loads(r.text)
            for message in messages_json:
                if message['author']['username'] == 'Midjourney Bot':
                    if not upscale and '%' not in message['content'] and len(message['attachments']) > 0:
                        print("line 31")
                        if self.prompt == message['content'].split('**')[1].split(' --')[0]:
                            return message
                    if upscale:
                        print("line 35" + upscale_num)
                        if 'message_reference' in message and message['message_reference']['message_id'] == message_id and str(upscale_num) == (re.search(r"Image #(\d+)", message['content'])).group(1):
                            return message
            time.sleep(5)

    def run_prompt(self, upscales):
        link_list = []
        self.post_interaction(self.get_payload(self.prompt))
        message = self.grab_prompt(False, 0, 0)
        if upscales == 'none':
            link_list.append(message['attachments'][0]['url'])
        else:
            component_id = message['components'][1]['components'][1]['custom_id']
            component_id = ''.join(component_id.split('::')[4])
            if re.search(r':', upscales):
                upscales = upscales.split(':')
                for i in range(int(upscales[0]), int(upscales[1]) + 1):
                    payload_upscale = self.get_payload_upscale(upscale_num = str(i + 1), message_id= message['id'] , 
                    component_id = component_id)
                    self.post_interaction(payload_upscale)
                    link_list.append(self.grab_prompt(True, str(i+1), message['id'])['attachments'][0]['url'])
            else:
                payload_upscale = self.get_payload_upscale(int(upscales) + 1, message['id'], component_id)
                self.post_interaction(payload_upscale)
                link_list.append(self.grab_prompt(True, str(i + 1), message['id'])['attachments'][0]['url'])
        return link_list

    def post_interaction(self, payload):
        requests.post('https://discord.com/api/v9/interactions', json=payload, headers=self.header)

    def get_payload_upscale(self, upscale_num, message_id, component_id):
        return {
            "type": 3,
            "guild_id": self.guild_id,
            "channel_id": self.channel_id,
            "message_id": message_id,
            "application_id": self.application_id,
            "session_id": self.session_id,
            "data": {
                "component_type": 2,
                "custom_id": "MJ::JOB::upsample::" + upscale_num + "::" + component_id
            }
        }

    def get_payload(self, prompt):
        return {'type': 2, 
        'application_id': self.application_id,
        'guild_id': self.guild_id,
        'channel_id': self.channel_id,
        'session_id': self.session_id,
        'data': {
            'version': self.version,
            'id': self.id,
            'name': 'imagine',
            'type': 1,
            'options': [{'type': 3, 'name': 'prompt', 'value': str(prompt) + ' ' + "--v 5"}],
            'attachments': []}
            }


#need to add a if __name__ == __main__ here 
bot = ImageBot(prompt="A photorealistic image of frank loyd wright style home in the woods")
upscales = "0:3"
result = bot.run_prompt(upscales)
print(result)