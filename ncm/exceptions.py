class NcmDownloadException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"Error: API not return 200 with the message {self.message}"
