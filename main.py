from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
import os

icon_path = 'images/icon.png'
commands = {"area":         "xfce4-screenshooter -r",
            "fullscreen":   "xfce4-screenshooter -f",
            "window":       "xfce4-screenshooter -w -d 2"}

class SnipExtension(Extension):

    def __init__(self):
        super(SnipExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        # self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        options = ['area',"select", 'full',"all",'window']
        fullquery = event.query.split(" ")
        items = []

        if len(fullquery) == 1:
            items.append(get_area_snip())
            items.append(get_screen_snip())
            items.append(get_window_snip()) # default delay of 2 seconds
            return RenderResultListAction(items)
        else:
            '''fullquery has a space'''
            opt1 = fullquery[1]
            included = []

            for option in options:
                if opt1 in option:
                    if option in ['area', 'select'] and "area" not in included:
                        items.append(get_area_snip())
                        included.append("area")
                    elif option in ['full','all'] and 'full' not in included:
                        items.append(get_screen_snip())
                        included.append("full")
                    elif option in ['window'] and "window" not in included:
                        if len(fullquery) >= 3 and fullquery[2].isdigit():
                            cmd = commands["window"][:-1]+fullquery[2]
                            items.append(get_window_snip(cmd))
                        else:
                            items.append(get_window_snip())
                        included.append("window")
            return RenderResultListAction(items)





def get_area_snip():
    return ExtensionResultItem(icon=icon_path,
                               name="snip area",
                               description="copy selected area to clipboard",
                               on_enter=RunScriptAction(commands["area"], None))

def get_screen_snip():
    return ExtensionResultItem(icon=icon_path,
                               name="snip screen",
                               description = "copy full screen to clipboard",
                               on_enter=RunScriptAction(commands["fullscreen"], None))

def get_window_snip(command=commands["window"]):
    return ExtensionResultItem(icon=icon_path,
                               name="snip window",
                               description = "copy focused window to clipboard",
                               on_enter=RunScriptAction(command, None))


if __name__ == '__main__':
    SnipExtension().run()

