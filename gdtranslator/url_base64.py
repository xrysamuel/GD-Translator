import base64

def url_safe_base64_encode(data):
    encoded = base64.urlsafe_b64encode(data.encode('utf-8')).rstrip(b'=')
    return encoded.decode('utf-8')

def url_safe_base64_decode(encoded):
    padded_encoded = encoded + '=' * (4 - len(encoded) % 4)
    decoded = base64.urlsafe_b64decode(padded_encoded.encode('utf-8'))
    return decoded.decode('utf-8')