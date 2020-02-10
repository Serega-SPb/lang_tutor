import sqlite3

CREATE_TABLE = 'CREATE TABLE IF NOT EXISTS <TBL> (<COLUMNS>);'
COL_TYPES = {
    int: 'INTERGER',
    str: 'VARCHAR'
}
PK_COL = ', PRIMARY KEY (<PK>)'


def gen_create_string(tbl_name, cols, pk):
    cols_str = ', '.join([f'"{c[1]}" {COL_TYPES[c[0]]}' for c in cols])
    cols_str += PK_COL.replace('<PK>', pk)
    return CREATE_TABLE.replace('<TBL>', tbl_name).replace('<COLUMNS>', cols_str)


def main():
    db_name = 'test_database.db'
    kanji_tbl = (
        'kanji',
        [(int, 'id'), (int, 'key'), (str, 'value'), (int, 'dash_count'),
         (str, 'on'), (str, 'kun'), (str, 'translate')],
        'id'
    )

    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.executescript(gen_create_string(*kanji_tbl))


if __name__ == '__main__':
    main()
