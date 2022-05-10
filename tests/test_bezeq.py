#!/usr/bin/env python3


from bot_sivim import bezeq

def test_active():
    assert bezeq('תל אביב', 'מזא"ה', 60)

def test_in_active():
    assert bezeq('תל אביב', 'מזא"ה', 1) == False
