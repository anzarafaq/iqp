from utils import session
from models import User, Organization

from werkzeug.wrappers import Request
from werkzeug.utils import cached_property
from werkzeug.contrib.securecookie import SecureCookie

# you could just use
# os.urandom(20) to get something random
SECRET_KEY = '\xc9\xd5+\xe7U\x8f\xef\r\xa60\xed\xf4\x1cp\xf7tA\xed\x9f\xd1'
#SECRET_KEY = os.urandom(20)

class CustomRequest(Request):

    @cached_property
    def client_session(self):
        return SecureCookie.load_cookie(self, secret_key=SECRET_KEY)

    @cached_property
    def client_user_object(self):
        if 'user_id' not in self.client_session:
            return None
        else:
            user_id = self.client_session['user_id']
            user_result = session.query(User).filter(User.user_id==user_id).all()
            user_object = None
            for user in user_result:
                user_object = user
            if not user_object:
                del self.client_session["user_id"]
                self.client_session.modified
                return None
            else:
                return user_object

    @cached_property
    def client_organization_object(self):
        if not self.client_user_object:
            return None
        else:
            org_id = self.client_user_object.user_organization_id
            org_result = session.query(Organization).filter(Organization.organization_id==org_id).all()
            org_object = None
            for org in org_result:
                org_object = org
            return org_object
