import hashlib

def make_pswd_hash(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_pswd_hash(password, hash):
	if make_pswd_hash(password)==hash:
		return True

	return False
