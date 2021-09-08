from generator import Generator

def alert(*args):
    return Generator().call('alert', args)

def prompt(*args):
    return Generator().call('prompt', args)

def confirm(*args):
    return Generator().call('confirm', args)