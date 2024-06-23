from openai import OpenAI

from ps_api.config import CFG

client = OpenAI(
    # This is the default and can be omitted
    api_key=CFG.OPENAI_API_KEY,
)


def generate_greeting(username, service_name=CFG.APP_NAME):
    prompt = f"Generate a unique greeting message for the user named {username} from the service {service_name}."

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
        ],
    )

    greeting_message = completion.choices[0].message.content
    return greeting_message
