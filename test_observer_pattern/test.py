from core.descriptors import NotifyProperty


class Foo:
    _prop = NotifyProperty('prop')

    @property
    def prop(self):
        return self._prop.get()

    @prop.setter
    def prop(self, value):
        self._prop.set(value)

    def sub(self, func):
        self._prop += func

    def unsub(self, func):
        self._prop -= func


def main():
    foo = Foo()
    watcher = lambda x: print(f'Watcher: value updated! prop = {x}')

    foo.sub(watcher)
    foo.prop = 1
    print(f'foo.prop = {foo.prop}')
    foo.prop = 2
    print(f'foo.prop = {foo.prop}')

    foo.unsub(watcher)
    foo.prop = 0
    print(f'foo.prop = {foo.prop}')


if __name__ == '__main__':
    main()
