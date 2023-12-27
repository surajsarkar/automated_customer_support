from helpers import load_config, main_agent
from openai import OpenAI
def main():
    import os
    print("hello user")
    mail_for_urgent_notification = input("Enter your mail for urgent notifications: ")
    if mail_for_urgent_notification:
        os.environ["RECEIVERS_MAIL"] = mail_for_urgent_notification
    load_config()

    # while true keep on listining to the user, each query will have it's own response.
    client = OpenAI()
    while True:
        main_agent(client)

if __name__ == "__main__":
    main()