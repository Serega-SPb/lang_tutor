import sqlite3

from modules.module_kanji.kanji import Kanji


class BaseMapper:

    TABLE = ''
    FIELDS = ['id', ]

    def __init__(self, connection):
        self._last_row_id = -1
        self.connection = connection
        self.cursor = self.connection.cursor()

    @property
    def last_row_id(self):
        if self._last_row_id == -1:
            self.__update_last_row_id()
        return self._last_row_id

    def __update_last_row_id(self):
        self.cursor.execute(f'SELECT max(id) FROM {self.TABLE}')
        f_one = self.cursor.fetchone()[0]
        self._last_row_id = int(f_one) if f_one else 0

    def __where_str_parse(self, where_dict):
        if not all([x in self.FIELDS for x in where_dict.keys()]):
            raise Exception('Incorrect WHERE columns')
        return ' AND '.join([f'{f} = ?' for f, _ in where_dict.items()])

    def _base_select(self, select_fields, **where):
        if select_fields != '*':
            if not all([x in self.FIELDS for x in select_fields]):
                raise Exception('Incorrect SELECT columns')
            select_fields = ', '.join(map(lambda x: f'"{x}"', select_fields))

        where_block = self.__where_str_parse(where)
        command = f'SELECT {select_fields} FROM {self.TABLE} WHERE {where_block};'
        self.cursor.execute(command, list(where.values()))

        headers = list(map(lambda x: x[0], self.cursor.description))
        data = self.cursor.fetchall()
        if data:
            return [headers, *data]
            # return {headers[i]: list(map(lambda x: x[i], data)) for i in range(len(headers))}
        return None

    def _base_insert(self, columns, data):
        if not all([x in self.FIELDS for x in columns]):
            raise Exception('Incorrect INSERT columns')
        i_vars = "?" * len(columns)
        columns = ', '.join(map(lambda x: f'"{x}"', columns))
        command = f'INSERT INTO {self.TABLE} ({columns}) VALUES ({", ".join(i_vars)})'
        self.cursor.execute(command, data)
        try:
            self.connection.commit()
        except Exception:
            pass
        else:
            self.__update_last_row_id()

    def _base_update(self, set_pairs, **where):
        if not all([x in self.FIELDS for x in set_pairs.keys()]):
            raise Exception('Incorrect SET columns')
        set_block = ', '.join([f'"{k}" = ?' for k in set_pairs.keys()])
        where_block = self.__where_str_parse(where)

        command = f'UPDATE {self.TABLE} SET {set_block} WHERE {where_block}'
        self.cursor.execute(command, (*list(set_pairs.values()), *list(where.values())))
        try:
            self.connection.commit()
        except Exception:
            pass
        else:
            self.__update_last_row_id()

    def _base_delete(self, **where):

        where_block = self.__where_str_parse(where)

        command = f'DELETE FROM {self.TABLE} WHERE {where_block}'
        self.cursor.execute(command, list(where.values()))
        try:
            self.connection.commit()
        except Exception:
            pass


class KanjiModel:
    __slots__ = ['id', *Kanji.__slots__]

    def __init__(self, **kwargs):
        for s in self.__slots__:
            if s in kwargs.keys():
                setattr(self, s, kwargs[s])

    @classmethod
    def from_kanji(cls, kanji):
        instance = cls(**{a: getattr(kanji, a) for a in cls.__slots__[1:]})
        return instance

    def to_kanji(self):
        kanji = Kanji(*[getattr(self, a) for a in Kanji.INIT_ATTRS])
        [setattr(kanji, a, getattr(self, a).split(', ')) for a in Kanji.__slots__ if a not in Kanji.INIT_ATTRS]
        return kanji

    def __repr__(self):
        return f'KanjiModel({", ".join([f"{a} = {getattr(self, a)}" for a in self.__slots__])})'


class KanjiMapper(BaseMapper):

    TABLE = 'kanji'
    MODEL = KanjiModel
    FIELDS = list(KanjiModel.__slots__)

    @staticmethod
    def __convert_list_to_str(val):
        if isinstance(val, list):
            val = ','.join([str(x) for x in val])
        return val

    def select(self, **where):
        base_result = super()._base_select(KanjiModel.__slots__, **where)
        if not base_result:
            return
        attrs = base_result.pop(0)
        result = []
        for res in base_result:
            m_kan = KanjiModel(**{a: res[i] for i, a in enumerate(attrs)})
            result.append(m_kan)
        return result

    def insert(self, kanji_model):
        kanji_model.id = self.last_row_id + 1
        col_data = [self.__convert_list_to_str(getattr(kanji_model, f)) for f in self.FIELDS]
        self._base_insert(self.FIELDS, col_data)

    def update(self, kanji_model):
        set_pairs = {a: self.__convert_list_to_str(getattr(kanji_model, a)) for a in kanji_model.__slots__[1:]}
        self._base_update(set_pairs, id=kanji_model.id)

    def delete(self, kanji_model):
        self._base_delete(id=kanji_model.id)
        del kanji_model


def main():
    db_name = 'test_database.db'
    con = sqlite3.connect(db_name)
    k_mapper = KanjiMapper(con)

    k = Kanji(2, 'ni', 2)
    k.on.append('ni')
    k.kun.append('futatsu')
    k.translate.append('two')
    k_mod = KanjiModel.from_kanji(k)
    k_mapper.insert(k_mod)

    select_test = k_mapper.select(id=1)
    print(select_test)
    if select_test:
        select_test_k = select_test[0].to_kanji()
        print(select_test_k)

    k_mod.dash_count += 1
    k_mapper.update(k_mod)
    select_test_2 = k_mapper.select(id=1)
    print(select_test_2)

    k_mapper.delete(k_mod)
    select_test_3 = k_mapper.select(id=1)
    print(select_test_3)
    pass


if __name__ == '__main__':
    main()
