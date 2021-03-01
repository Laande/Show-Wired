import sys
from g_python.gextension import Extension
from g_python.hmessage import Direction, HMessage

extension_info = {
    "title": "Show Wireds",
    "description": "Allow you to see the wireds",
    "version": "2.0",
    "author": "Lande"
}

ext = Extension(extension_info, sys.argv)
ext.start()


list_wireds = []
on = False


def hide_wired(message):
    if on:
        message.is_blocked = True
        (id_furni, boolean, int1, int2) = message.packet.read("sBii")
        list_wireds.append([id_furni, boolean, int1, int2])


def re_send(j):
    pack = '{l}{h:2703}'
    for i in j:
        if isinstance(i, bool):
            pack += '{b:'+str(i)+'}'
        elif isinstance(i, int):
            pack += '{i:'+str(i)+'}'
        else:
            pack += '{s:"'+i+'"}'
    ext.send_to_client(pack)


def speech(message):
    global on

    (text, color, index) = message.packet.read('sii')
    if text == ":wshow on":
        message.is_blocked = True
        if on:
            ext.send_to_client('{l}{h:1446}{i:0}{s:"[ Show Wired => Already on ]"}{i:0}{i:1}{i:0}{i:0}')
        else:
            on = True
            ext.send_to_client('{l}{h:1446}{i:0}{s:"[ Show Wired => On ]"}{i:0}{i:1}{i:0}{i:0}')

    elif text == ":wshow off":
        message.is_blocked = True
        if not on:
            ext.send_to_client('{l}{h:1446}{i:0}{s:"[ Show Wired => Already off ]"}{i:0}{i:1}{i:0}{i:0}')
        else:
            on = False
            ext.send_to_client('{l}{h:1446}{i:0}{s:"[ Show Wired => Off ]"}{i:0}{i:1}{i:0}{i:0}')

    if text == ":wshow hide":
        message.is_blocked = True
        if list_wireds:
            count = 0
            print(len(list_wireds))
            for i in list_wireds:
                re_send(i)
                count += 1
            list_wireds.clear()
            ext.send_to_client('{l}{h:1446}{i:0}{s:"[ Show Wired => '+str(count)+' wired'+("s" if count > 1 else "")+' hide ]"}{i:0}{i:1}{i:0}{i:0}')
        else:
            ext.send_to_client('{l}{h:1446}{i:0}{s:"[ Show Wired => No wireds to hide ]"}{i:0}{i:1}{i:0}{i:0}')


def clear_user(message):
    list_wireds.clear()


ext.intercept(Direction.TO_CLIENT, hide_wired, 2703)
ext.intercept(Direction.TO_SERVER, speech, 1314)
ext.intercept(Direction.TO_CLIENT, clear_user, 1301)
