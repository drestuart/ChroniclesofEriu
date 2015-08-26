'''
Created on Feb 14, 2014

@author: dstuart
'''

import os
import os.path
import Game as G

random = G.getRandom()

prefixes = []
suffixes = []

prefixfile = open(os.path.join("data", "names", "twprefix"), 'r')
suffixfile = open(os.path.join("data", "names", "twsuffix"), 'r')

for line in prefixfile.readlines():
    line = line.strip()
    if line:
        prefixes.append(line)

prefixfile.close()

for line in suffixfile.readlines():
    line = line.strip()
    if line:
        suffixes.append(line)

suffixfile.close()

def name():
    while True:
        prefix = random.choice(prefixes)
        suffix = random.choice(suffixes)
        
        if prefix.endswith('-') or suffix.startswith('-'):
            prefix = prefix.capitalize().strip('-')
            suffix = suffix.strip('-')
            if prefix.lower() != suffix:
                return prefix + suffix
        else:
            prefix = prefix.capitalize().strip('-')
            suffix = suffix.strip('-').capitalize()
            if prefix.lower() != suffix:
                return prefix + " " + suffix
        
        
def main():
    for i in range(10):
        print name()

if __name__ == '__main__':
    main()
    
    