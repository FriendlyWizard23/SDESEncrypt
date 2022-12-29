# SDESEncrypt
This python script will help you understand the mechanism of S-DES algorithm.
## What is S-DES
S-DES is nothing more than a Simplified version of DES.
This script works best with the default configuration that it is set on, which is 
- Key Length: 9 bit
- Number of rounds: 3
- plaintext chunks: 12 bit

You may also try to change it and see how it behaves yet i do not guarantee the proper execution of the algorithm!
It took me around 1h to code it so it does not have many features yet i hope it will help students around the world understanding it better.
## How to use it
It's not that much complicated. Clone this repo then execute it via python3 / python (both versions should be ok even if i only tested it with python3).
## Block Encryption Technique
As block encryption technique, this script uses ECB because it's the easiest one.
As per ECB's Mode then, the 9bit key you input will be used for the whole plaintext.
The plaintext is later divided in n-bit chunks (default is 12) and in case the plaintext size is not a divider of 12, the script will set up a padding.
