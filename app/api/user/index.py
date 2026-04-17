from sqlalchemy.orm import Session
class UserController :
    def demo(self,db:Session):
        print("session started");
        return "hello demo"