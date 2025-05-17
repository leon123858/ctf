import requests
import random
 
url = "http://127.0.0.1"
 
def register(username, password):
    """
    Register a new user.
    Args:
        username: str
        password: str
    Returns:
        dict: {'session': 'd4eb341a77b1b55b7b4e4d641692603a44311f89075c2adff946dfeeed373df6'}
    """
    while True:
        try:
            s = requests.session()
            _ = s.post(url+"/register", data={"username": username, "password":password})
            return s.cookies.get_dict()
        except (KeyError, requests.exceptions.ConnectionError):
            pass

def login(username, password):
    """
    Login to an existing user.
    Args:
        username: str
        password: str
    Returns:
        dict: {'session': 'd4eb341a77b1b55b7b4e4d641692603a44311f89075c2adff946dfeeed373df6'}
    """
    while True:
        try:
            s = requests.session()
            _ = s.post(url+"/login", data={"username": username, "password": password})
            return s.cookies.get_dict()
        except (KeyError, requests.exceptions.ConnectionError):
            pass

def get_session(username, password):
    """
    Get session cookies from login or register function.
    Args:
        username: str
        password: str
    Returns:
        dict: {'session': 'd4eb341a77b1b55b7b4e4d641692603a44311f89075c2adff946dfeeed373df6'}
    """
    cookies = login(username, password)
    if 'session' not in cookies:
        cookies = register(username, password)
        if 'session' not in cookies:
            return None
    return cookies['session']

def ECB_part_split(session):
    """
    Split the session into 128bit parts(32 hex chars).
    Args:
        session: str
    Returns:
       list: ['d4eb341a77b1b55b', '7b4e4d641692603a', ...]
    """
    return [session[i:i+32] for i in range(0, len(session), 32)]

def find_min_same_block(no_prt=False):
    """
    Find the minimum length of username that produces a collision in ECB mode.
    Returns:
        int: minimum length of username that produces a collision (2 sample).
    """
    for i in range(100):
        username = b'X'*i
        password = "password"
        session = get_session(username, password)
        if session is None:
            continue
        parts = ECB_part_split(session)
        if not no_prt:
            print(i, parts)
        if len(set(parts)) != len(parts):
            print(f"Collision found with username length {i}")
            return i
    return None

def try_collision(base_char,guessChar, knownString, name_len):
    """
    Try to find a collision by guessing the character at a specific position.

    Args:
        base_char (bytes): the base character to use for the username.
        guessChar (bytes): the guessed character at a specific position.
        knownString (bytes): the known string.
        name_len (int): the length of the username may create same block.

    Returns:
        bool: True if a collision is found, False otherwise.
    """
    known_len = len(knownString)
    # name_len - 1 = XX + 16 + 15
    reserveStr = base_char* (name_len - 1 - 16 -15)
    guessStr = base_char*(16- known_len - 1) + knownString + guessChar
    targetStr = base_char*(15 - known_len) + knownString
    username = reserveStr + guessStr + targetStr
    assert len(username) == name_len-1, f"Username length is not 45, it is {len(username)}"
    # print(username)
    session = get_session(username, 'password')
    if session is None:
        return False
    parts = ECB_part_split(session)
    print(parts)
    # meet same block
    if len(set(parts)) != len(parts):
        return True
    return False

def collision_test():
    baseChar = b'X'
    knownString = b''
    name_len = find_min_same_block(True)
    # 0-255 can cover all possible characters, use binary to confirm the result.
    for i in range(255):
        guessChar = bytes([i])
        if try_collision(baseChar, guessChar, knownString, name_len):
            print(f"Collision found with character: {guessChar}")
            return True
    return False

if __name__ == "__main__":
    # api wrapper
    # session = get_session(b'test', b'password')
    # if session is None:
    #     print("Failed to get session. Exiting.")
    #     exit(1)
    # parts = ECB_part_split(session)
    # print(parts)
    # try to find two same blocks in the session key.
    # find_min_same_block()
    collision_test()