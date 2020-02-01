from core.data_loader import DataLoader


def get_exercises(loader):
    exercises = []
    scen_name = input('scenario\n')
    scen = loader.scenarios[scen_name]

    for m, bl in scen.data.items():
        mod = loader.modules[m].init
        print(mod.get_question_types())
        q_type = input('quest type:\n')
        exercises.extend(mod.get_exercises(bl, q_type))

    results = []

    for ex in exercises:
        ans = int(input(str(ex))) - 1
        results.append(ex.check_answer(ex.options_answers[ans]))

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


if __name__ == '__main__':
    main()
