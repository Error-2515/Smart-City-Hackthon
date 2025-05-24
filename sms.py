from twilio.rest import Client

# Your Twilio credentials (get these from your Twilio account)
account_sid = ''#enter your twilio account sid
auth_token = ''#enter your authorization token

# Initialize the Twilio client
client = Client(account_sid, auth_token)

# Function to send SMS
def send_sms(to_phone_number, message):
    from_phone_number = ''  # Your Twilio phone number

    # Sending the message
    message = client.messages.create(
        body=message,
        from_=from_phone_number,
        to=to_phone_number
    )

    return message.sid

# Example usage
if __name__ == "__main__":
    to_phone_number =int('')#enter twilio verified phone number
    message = "This is a test message from Twilio!"
    
    # Send the SMS and print the message SID
    message_sid = send_sms(to_phone_number, message)
    print(f"Message sent successfully with SID: {message_sid}")
