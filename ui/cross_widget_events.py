from ui.ui_messaga_bus import Event


class MessageType:
    INFO = 'I'
    WARN = 'W'


class CrossWidgetEvents:
    change_screen_event = Event(int)
    load_scenario_event = Event(object, str, bool)
    show_message_event = Event(str, str, str)
