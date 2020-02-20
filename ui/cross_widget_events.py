from ui.ui_messaga_bus import Event


class CrossWidgetEvents:
    change_screen_event = Event(int)
    load_scenario_event = Event(object, str, bool)
    show_message_event = Event(str, str, str)
