# UnifyIDCodingChallenge

author: Benjamin Newcomer

description: This directory contains the source code and test results for the UnifyID coding challenge. main.py is a script that contains the logic for creating a random bitmap and for generating a random RSA keypair. Unfortunately I do not have time to implement the WAV challenge because my computer is about to die and I am without a charger close by. I chose to save that challenge for last because I am least familiar with audio programming. See below for usage. Enjoy!

I ran into some problems with the API limits for the new random.org API. I was not able to request the number of random bits needed to produce a completely random bitmap image because it exceeds the number of bits allowed per day for the new beta API. 

To remedy this I am requesting only one random number per image and using it to seed the python pseudo-random number generator. I think this demonstrates the same knowledge as generating all numbers using the API, but it allowed me to use the newer technology, which I typically prefer for ease of use and code lifespan.

To generate RSA keypairs I am using the Crypto.RSA module, which accepts a random number generating function. This function uses the same single number request to generate a list of bits. However, it looks like the Crypto.RSA.generate function is calling this function more than once, resulting in the depletion of my allowed requests per day. I have included test results, but to run the code yourselves, you may need to wait a day or use a different API key. Thanks for your understanding!

usage: python main.py [-h] [-b] [-k]

optional arguments:
  -h, --help     show this help message and exit
  -b, --bitmap   flag to produce a random bitmap image
  -k, --keypair  flag to produce a random rsa keypair
