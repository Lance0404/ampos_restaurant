# these are endpoint related errors
class QuantityBelowZero(Exception):
    pass

class RequiredKeyMissing(Exception):
    pass


'''
Example:

class InvalidUsage(Exception):

    # example from
    # http://flask.pocoo.org/docs/1.0/patterns/apierrors/
    
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.messages
        return rv

'''