class AccountNotFound(Exception):
    """
    Exception for when a user searches for a RR account that doesn't exist
    """
    
    def __init__(self):
        super().__init__("Could not find the Rec Room account you were looking for.")