import bcrypt
import datetime

from .models import Tokens

class PassTokenizer:
    def __init__(self, password):
        self.password = password

    def tokenize(self):
        salt = bcrypt.gensalt()        
        return {"pass": bcrypt.hashpw(self.password.encode('utf-8'), salt=salt), "salt": salt}
    
    def hasAuth(self, user_):
        return Tokens.objects.get(user=user_)
        
        
        

