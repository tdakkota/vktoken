import getpass
import json
import sys
import requests
import pyperclip
import vktoken


def main():
    arguments = vktoken.ArgumentParser().parse_args()
    app = vktoken.App(name=arguments.app)

    if not arguments.password:
        arguments.password = getpass.getpass("Enter your password: ")

    try:
        response = requests.get(
            "https://oauth.vk.com/token"
            "?grant_type=password"
            f"&client_id={app.client_id}"
            f"&client_secret={app.client_secret}"
            f"&username={arguments.login}"
            f"&password={arguments.password}"
        ).json()
    except requests.exceptions.ConnectionError:
        print("Unable to send request. Please check your internet connection")
        sys.exit(-1)

    except json.JSONDecodeError:
        print(f"Invalid response of the server")
        sys.exit(-1)    

    access_token = response.get("access_token")
    
    if access_token:
        print(f"Access token: {access_token}")

        if arguments.copy:
            pyperclip.copy(access_token)
            print("Access token has been copied to the clipboard")

    else:
        error_description = response.get("error_description")

        if error_description:
            print(f"Error: {error_description}")

        else:
            print(f"Error: {response.get('error')}")
