from openai import OpenAI


def get_query_response(client: OpenAI, message: str,) -> str:
    response = get_response_for_query(client, message, "user",)
    return response


def query_convays_urgency(client: OpenAI, message: str,) -> bool:
    response = get_response_for_query(client, message, "user",)
    if "yes" in response.lower():
        return True
    return False


def get_response_for_query(client: OpenAI, message: str, role: str,) -> str:
    model = "gpt-3.5-turbo"
    message = {"role": role, "content": message}
    msg_history = update_msg_history(message)
    completion = client.chat.completions.create(model=model, messages=msg_history)
    return completion.choices[0].message.content

def get_message_history() -> list:
    import json
    import os

    if not os.path.exists(f"message_history.json"):
        with open("message_history.json", "w") as f:
            json.dump([], f)
        return []

    with open("message_history.json", "r") as f:
        msg_history = json.load(f)
    return msg_history

def update_msg_history(message: dict):
    import json
    msg_history = get_message_history()
    msg_history.append(message)
    with open("message_history.json", "w") as f:
        json.dump(msg_history, f)
    return msg_history


def notify_on_mail(message: str):
    import smtplib
    import os

    sender_mail = os.environ.get("SENDER_MAIL")
    sender_pass = os.environ.get("SENDER_PASS")
    receivers_mail = os.environ.get("RECEIVERS_MAIL")

    if not sender_mail or not sender_pass or not receivers_mail:
        print(
            "Please set the environment variables SENDER_MAIL, SENDER_PASS, RECEIVER_MAIL, for notification to work."
        )
        return
    receivers_mail = [receiver_mail.strip() for receiver_mail in receivers_mail.split(",")]
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_mail, sender_pass)
    for receiver_mail in receivers_mail:
        server.sendmail(sender_mail, receiver_mail, message)
    server.quit()


def load_config():
    import json
    import os

    with open("config.json", "r") as f:
        config = json.load(f)
    for key, value in config.items():
        os.environ[key.strip()] = value.strip() if isinstance(value, str) else value
