import subprocess, requests, time

class Linux:

    def __init__(self,bot_token, chat_id) -> None:
#        self.bot_token = bot_token
        self.chat_id = chat_id
        self._base_url = f"https://api.telegram.org/bot{bot_token}"

    def send_message(self, text):
        url = f"{self._base_url}/sendMessage"
        params = {"chat_id": self.chat_id, "text": text, "parse_mode": "Markdown"}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to send message: {e}")

    def execute_command(self, command):

        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, timeout=10)
            response = f"Command executed successfully:\n```\n{output.decode('utf-8')}\n```"
        except subprocess.CalledProcessError as e:
            response = f"Command failed with error:\n```\n{e.output.decode('utf-8')}\n```"
        except subprocess.TimeoutExpired:
            response = "Command timed out."
        return response

    def handle_message(self, command):
        # Execute the command received from the user
        response = self.execute_command(command)
        # Send the response back to the user
        self.send_message(response)

    def main(self):
        # Run the bot indefinitely, listening for messages

        welcome_mess = "Welcome My Friend. You can control Linux Server using Command. Any time you can exit by typing 100"
        self.send_message(welcome_mess)
        epoch_time = int(time.time())
        old_messege_id = 0
        while True:
            try:
                update = requests.get(f"{self._base_url}/getUpdates").json()
                messege_id = update["result"][-1]["message"]["message_id"]
                if update["ok"] and update["result"]:
                    if update["result"][-1]["message"]["date"] > epoch_time:
                        if messege_id != old_messege_id:
                            # print(update["result"])
                            # print(update["result"][-1]["message"]["date"])
                            # print(update["result"][-1]["message"]["text"])
                            self.chat_id = update["result"][-1]["message"]["chat"]["id"]
                            old_messege_id = messege_id
                            # print(messege_id, old_messege_id)
                            # chat_id = update["message"]["chat"]["id"]
                            command = update["result"][-1]["message"]["text"].strip()
                            # print("command is ", command)
                            actualcommand = command[0].lower()+ command[1:]
                            print("Typed command is--> ", actualcommand)
                            if actualcommand == "100":
                                last_messege = "Thank you for using these services. Bye Have a good day"
                                self.send_message(last_messege)
                                exit("Thank you for using this services")
                            # print(chat_id)
                            self.handle_message(actualcommand)
            except Exception as e:
                print(f"Error occurred: {e}")

            time.sleep(1)


if __name__ == '__main__':
    # Start the main loop
    bot_token = "74856399735:ARTDC465Rsrrjcf4dREpo8H5xV5UiEH8"  # tpye here correct bot token this is a sample only
    chat_id = 2187455192    # tpye here correct chat id this is a sample only
    Linux(bot_token, chat_id).main()


# This takes command from telegram and excecutes in linux terminal 