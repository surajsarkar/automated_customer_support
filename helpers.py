from openai import OpenAI


def get_query_response(client: OpenAI, message: str, user_id: str) -> str:
    response = get_response_for_query(client, message, "user", user_id)
    return response


def query_convays_urgency(client: OpenAI, message: str, user_id: str) -> bool:
    response = get_response_for_query(client, message, "user", user_id)
    if "yes" in response.lower():
        return True
    return False


def get_response_for_query(client: OpenAI, message: str, role: str, user_id: str) -> str:
    model = "gpt-3.5-turbo"
    message = {"role": role, "content": message}
    msg_history = update_msg_history(user_id, message)
    completion = client.chat.completions.create(model=model, messages=msg_history)
    return completion.choices[0].message.content

def get_message_history(user_id: str) -> list:
    import json
    import os

    if not os.path.exists(f"message_history_{user_id}.json"):
        with open(f"message_history_{user_id}.json", "w") as f:
            json.dump([], f)
        return []

    with open("message_history.json", "r") as f:
        msg_history = json.load(f)
    return msg_history

def update_msg_history(user_id: str, message: dict):
    import json
    msg_history = get_message_history(user_id)
    msg_history.append(message)
    with open(f"message_history_{user_id}.json", "w") as f:
        json.dump(msg_history, f)
    return msg_history


def notify_on_mail(message: str):
    import smtplib
    import os

    sender_mail = os.environ.get("SENDER_MAIL")
    sender_pass = os.environ.get("SENDER_PASS")
    receivers_mail = os.environ.get("RECEIVERS_MAIL")
    receivers_mail = [receiver_mail.strip() for receiver_mail in receivers_mail.split(",")]

    if not sender_mail or not sender_pass or not receivers_mail:
        print(
            "Please set the environment variables SENDER_MAIL, SENDER_PASS, RECEIVER_MAIL, for notification to work."
        )
        return
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_mail, sender_pass)
    for receiver_mail in receivers_mail:
        server.sendmail(sender_mail, receiver_mail, message)
    server.quit()



