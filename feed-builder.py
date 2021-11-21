import sys
import os

def feed_builder(target_dir):
    '''Entry point, builds the feed, baby!'''
    stream = os.popen('git pull origin')
    output = stream.read();
    print(output)

    if not 'files changed' in output:
        return
    
    for root, dirs, files in os.walk(target_dir):
        print('root: ' + root)
        print(files)

    print('Did that shit')




if __name__ == '__main__':
    target_dir = sys.argv[1]
    feed_builder(target_dir)

