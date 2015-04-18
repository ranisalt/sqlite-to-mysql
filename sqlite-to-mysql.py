import sys


def main():
    ignored_heads = {
        'PRAGMA', 'BEGIN TRANSACTION;', 'COMMIT;',
        'DELETE FROM sqlite_sequence;', 'INSERT INTO "sqlite_sequence"',
    }

    replacements = {
        'AUTOINCREMENT': 'AUTO_INCREMENT',
        "DEFAULT 't'": "DEFAULT '1'",
        "DEFAULT 'f'": "DEFAULT '0'",
        ",'t'": ",'1'",
        ",'f'": ",'0'",
    }

    print("SET sql_mode='NO_BACKSLASH_ESCAPES';", file=sys.stdout)

    def parse_line(line, in_string):
        for i in replacements:
            query.replace(i, replacements[i])

        new_query = []
        for c in query:
            if not in_string:
                if c == "'":
                    in_string = True
                elif c == '"':
                    c = '`'
            elif c == "'":
                in_string = False
            new_query.append(c)

        print(''.join(new_query), file=sys.stdout)
        return in_string

    in_string = False
    for query in sys.stdin:
        if not any(query.startswith(i) for i in ignored_heads):
            in_string = parse_line(query, in_string)


if __name__ == '__main__':
    main()
