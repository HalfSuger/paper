# -*- encoding: utf-8 -*-
from os.path import join, getsize, abspath
from os import walk
from prettytable import PrettyTable


class CodeLinesCounter(object):
    SIZES = [('B', 1), ('KB', 1024), ('MB', 1024 ** 2), ('GB', 1024 ** 3), ('TB', 1024 ** 4)]

    def __init__(self, languages):
        self._languages = languages
        self._results = {suffix: (0, 0, 0) for suffix in languages}
        self._successful = self._error = 0

    def scan(self, directory, log=False):
        if log: print('Scanning', directory)
        try:
            for root, _, files in walk(abspath(directory)):
                for filename in files:
                    suffix = filename[filename.rfind('.') + 1:]
                    filename = join(root, filename)
                    if suffix in self._results:
                        lines, size, numFiles = self._results[suffix]
                        numFiles += 1
                        size += getsize(filename)
                        try:
                            ln = 0
                            with open(filename, 'r', encoding='utf-8') as f:
                                for line in f:
                                    if line and not line.isspace():
                                        ln += 1
                        except UnicodeDecodeError:  # Try 'gbk' encoding
                            try:
                                ln = 0
                                with open(filename, 'r', encoding='gbk') as f:
                                    for line in f:
                                        if line and not line.isspace():
                                            ln += 1
                            except:
                                print(filename, '[Error: unknown encoding]')
                                self._error += 1
                            else:
                                lines += ln
                        except Exception as e:
                            print(filename, '[Unknown error: %s]' % e)
                            self._error += 1
                            continue
                        lines += ln
                        if log: print(f'{filename} [{ln}]')
                        self._successful += 1
                        self._results[suffix] = (lines, size, numFiles)
                    elif log:
                        print(filename, '[None]')
        except KeyboardInterrupt:
            print('\nUser stopped operation')
        else:
            if log: print('Scan finished')

    def report(self):
        table = PrettyTable(['Language', 'Lines', 'Size', 'Files'],
                            title=f'Scan result (OK {self._successful}, Error {self._error})')
        for suffix, (lines, size, files) in sorted(self._results.items(), key=lambda x: x[1], reverse=True):
            table.add_row([self._languages[suffix], lines, self.__format_size(size), files])
        print(table)

    def __format_size(self, bytes):
        for suffix, size in self.SIZES:
            if bytes < size * 1024:
                return '%.2f %s' % (bytes / size, suffix)
        return '%.2f %s' % (bytes / self.SIZES[-1][1], 2, self.SIZES[-1][0])


counter = CodeLinesCounter(
    languages={'py': 'Python', 'c': 'C', 'cpp': 'C++', 'java': 'Java', 'js': 'JavaScript', 'html': 'HTML', 'css': 'CSS',
               'txt': 'Plain text'})
counter.scan('C:/Users/Administrator/PycharmProjects/flaskProject')
counter.report()
