from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()      # Reads OPENAI_API_KEY from .env
client = OpenAI()  # Create a connection to OpenAI services.

# older version
# response = client.chat.completions.create(
#     model='gpt-4o-mini',
#     messages=[{'role':'user','content':'Say OK'}]
# )

# print(response.choices[0].message.content)

# modern API
response = client.responses.create(
    model="gpt-5-mini",
    input="Say OK"
)

print(response.output_text)