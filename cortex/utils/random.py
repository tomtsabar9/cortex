import random
import string

def random_string(stringLength=16):
	"""
	Return random string of legnth <stringLength>
	"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))