#!/usr/bin/env python3


from bot_sivim import cellcom

def test_active():
    assert cellcom('תל אביב', 'מזא"ה', 60)

def test_in_active():
    assert cellcom('תל אביב', 'מזא"ה', 1) == False
