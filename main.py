import requests
import random
import json
from PIL import Image
from Crypto.PublicKey import RSA
import argparse

url = "https://api.random.org/json-rpc/1/invoke"
n = "1"
minInt = "0"
maxInt = "256"
payload = "{\"jsonrpc\": \"2.0\",\n    \"method\": \"generateIntegers\",\n    \"params\": {\n        \"apiKey\": \"f13cae90-1f4d-4904-b9fe-64e33ef5ebdd\",\n        \"n\": " + n + ",\n        \"min\": " + minInt + ",\n        \"max\": " + maxInt + ",\n        \"replacement\": true\n    },\n    \"id\": 42\n}"
headers = { 'content-type': "application/json" }

# parse command line args
parser = argparse.ArgumentParser()
parser.add_argument('-b', '--bitmap', default=False, action='store_true')
parser.add_argument('-k', '--keypair', default=False, action='store_true')
args = parser.parse_args()

# performs a request to get one random number. Random.org
# imposes a fairly low limit on requests/day, so we will
# get one number at a time and seed the python pseudo-random
# number generator with it
def getRandom():
    response = requests.request("POST", url, data=payload, headers=headers)
    body = json.loads(response.text)

    # if the API key has exceeded limits
    # we may get an error here
    if (not hasattr(body, u'result')):
        print body[u'error']
        exit(1)

    result = body[u'result']
    random = result[u'random']
    number = random[u'data']

    return number[0]

# generate n pseudo-random numbers from a seed
def generateRandoms(seed, n, min=0, max=256):
    randoms = [seed]
    random.seed(seed)

    for i in range(n):
        # seed with the last random number
        randoms.append(random.randint(min, max))

    return randoms

# generate a string of n random bytes
def generateRandomBytes(seed, n):
    random.seed(seed)
    return random.getrandbits(n * 8)

# generate a bitmap image with randomized RGB pixels
def generateBitmap(width=128, height=128):
    # PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]
    img = Image.new( 'RGB', (width, height), "black") # create a new black image
    pixels = img.load() # create the pixel map
    randoms = generateRandoms(getRandom(), width * height * 3)
    index = 0

    for i in range(width):    # for every col:
        for j in range(height):    # For every row
            r = randoms[index]
            index += 1
            g = randoms[index]
            index += 1
            b = randoms[index]
            index += 1

            pixels[i, j] = (r, g, b)

    return img

# generate an RSA key pair seeded with a random
# number
def generateRSAKeypair():
    # accept a length n of bytes and return
    # a random string with n chars
    def randfunc(n):
        return str(generateRandomBytes(getRandom(), n))

    # rsa generate progress function
    def progress(msg):
        print 'generating ' + msg

    # generate rsa keypair from using randfunc
    keypair = RSA.generate(2048, randfunc=randfunc, progress_func=progress)
    pem = keypair.exportKey('PEM')
    public = keypair.publickey().exportKey()

    with open('key.pem', 'w') as f:
        f.write(pem)
        f.close()

    with open('public', 'w') as f:
        f.write(public)
        f.close()

# perform actions based on command
# line flags
if args.bitmap:
    print 'generating random bitmap...'
    generateBitmap().save('out.bmp')
    print 'done'
if args.keypair:
    print 'generating random rsa keypair'
    generateRSAKeypair()
    print 'done'
