from core.data_loader import DataLoader


def temp_control(loader):
    tasks = {
        'get_modules': lambda: print('\n'.join([m.name for m in loader.modules])),
        'get_scenarios': lambda: print('\n'.join([m.name for m in loader.scenarios])),
    }

    while True:
        print('\n'.join(tasks.keys()))
        print('q - Exit')
        t = input('')
        if t.lower() == 'q':
            break
        try:
            tasks[t]()
        except:
            pass
        print('-'*50)


def main():
    loader = DataLoader()
    temp_control(loader)
    pass


if __name__ == '__main__':
    main()
