from ui.ui_messaga_bus import Event


class MessageType:
    INFO = 'I'
    WARN = 'W'


class ScreenIndex:
    MAIN = 0
    SCENARIO = 1
    EDITOR = 2


class EditorMode:
    CREATE_NEW = 0
    CREATE_FROM = 1
    LOAD = 2


class CrossWidgetEvents:
    change_screen_event = Event(int)
    clsoe_main_window_event = Event()
    load_scenario_event = Event(object, str, bool)
    show_message_event = Event(str, str, str)
    start_editor_event = Event(EditorMode, list)
    reload_scenarios_event = Event()
    locale_changed_event = Event()
    show_question_event = Event(str, str, object)

