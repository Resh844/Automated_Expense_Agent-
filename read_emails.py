import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# The only scope needed is to read Gmail.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def main():
    """
    This is a simple test script to check your Gmail connection.
    It prints the subject lines of your last 10 emails.
    """
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("gmail", "v1", credentials=creds)
        
        results = service.users().messages().list(userId="me", maxResults=10).execute()
        messages = results.get("messages", [])

        if not messages:
            print("No messages found.")
            return

        print("Your 10 most recent emails:")
        for message in messages:
            msg = service.users().messages().get(userId="me", id=message["id"]).execute()
            headers = msg["payload"]["headers"]
            subject = next((header['value'] for header in headers if header['name'] == 'Subject'), None)
            print(f"- {subject}")

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()