import requests
import hashlib
import sys

def request_api_data(query):
    url = 'https://api.pwnedpasswords.com/range/' + query
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code},check the API and try again')
    return  res

def get_passwrod_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(password):
    sha1passwrord = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1passwrord[:5],sha1passwrord[5:]
    response = request_api_data(first5_char)
    return get_passwrod_leaks_count(response, tail)

def main():
    args = input('Enter the password to check: ')
    count = pwned_api_check(args)
    if count:
        print(f'{args} was found {count} times...you must change your password :(')
    else:
        print(f'{args} was not found.....you are still safe')
    return  'done!'

main()