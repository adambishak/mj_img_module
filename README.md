# MidJourney Image Module

This repository is meant to simply allow developers to implement midjourney image generation in their projects

This of course, is purely for research and definitely not for use, since it is against Midjourney TOS to automate this process:
You may not use the Services for competitive research. You may not reverse engineer the Services or the Assets. You may not use automated tools to access, interact with, or generate Assets through the Services. Only one user may use the Services per registered account. Each user of the Services may only have one account.

Installation:
1. Create a discord server and add the midjourney bot to it, test the commands.

2. Go to your new server, assuming you use chrome, press F12 to access dev tools, navigate to the network tab towards the top and click it to open.

3. Now generate a prompt in your server using /imagine, after you enter and send, you are going to see a lot of activity with titles like "ack" and "science" find the request titled "interactions". then find the header tab of this request, scroll until you find "Authorization:" and copy the token. Open params.json and paste it in the quotation marks following "authorization":

4. still under your interaction request, navigate to the payload tab and copy the whole thing into a file. Now for every parameter in the params.json file of this repo, you need to find the respective value in the interaction request and paste it into the quotation marks.

5. save the jsonn folder and the script is now good to go if you were to hypothetically use it. The prompt is a parameter for the Class ImageBot, at the bottom of ImageBot.py there is an example of how to use it.

This script needs some work and improvement and I am looking for people interested in helping. If so, email me at adambishak@gmail.com or message me on discord at adamb_b.
