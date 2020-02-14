from core.data_loader import DataLoader


def get_exercises(loader):
    exercises = []
    scen_name = input('scenario\n')
    scen = loader.scenarios[scen_name]
    opt_enb = True

    for m, bl in scen.get_data().items():
        mod = loader.modules[m].init
        print(mod.get_question_types())
        q_type = input('quest type:\n')
        exercises.extend(mod.get_exercises(bl, q_type, opt_enb))

    results = []

    for ex in exercises:
        ans = input(str(ex))
        if opt_enb:
            ans = int(ans) - 1
            results.append(ex.check_answer(ex.options_answers[ans]))
        else:
            results.append(ex.check_answer(ans))

    print(f'Results {sum(map(lambda x: x, results))}/{len(results)}')


def temp_control(loader):
    tasks = {
        'get_modules': lambda: print('\n'.join([f'{m.name} - {m.is_enabled}' for m in loader.modules.values()])),
        'get_scenarios': lambda: print('\n'.join([m.name for m in loader.scenarios.values()])),
        'activate_module': lambda: loader.activate_module(input('module name:\n')),
        'deactivate_module': lambda: loader.deactivate_module(input('module name:\n')),
        'get_quest_types': lambda: print(loader.modules[input('module name:\n')].init.get_question_types()),
        'get_exercises': lambda: get_exercises(loader)
    }

    while True:
        print('\n'.join(tasks.keys()))
        print('q - Exit')
        t = input('')
        if t.lower() == 'q':
            break
        try:
            tasks[t]()
        except Exception as ex:
            print(ex)
        print('-'*50)


def main():
    loader = DataLoader()
    temp_control(loader)
    pass


def main_ui():
    from PyQt5.QtWidgets import QApplication
    from ui.main.main_view import MainView
    from ui.main.main_model import MainModel
    from ui.main.main_controller import MainController

    app = QApplication([])

    model = MainModel()
    controller = MainController(model)
    view = MainView(model, controller)

    view.show()
    app.exec_()


if __name__ == '__main__':
    main_ui()
    # main()
