import re


class Analyser:
    def __init__(self, text):
        self.text = []
        self.idents = {}
        self.id_idents = 1
        self.kws = {}
        self.id_kws = 1
        self.remove_comments(text.split('\n'))
        self.table = []
        self.keywords = ['if', 'then', 'else']
        self.compare = ['>', '<', '=']
        self.equal = ':='
        self.sep = ';'
        self.identif = r'[A-Za-z]{1,16}'
        self.number = r'[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?'

    def analyse(self):
        if len(self.text) == 0:
            return
        else:
            head = []
            tail = self.text.copy()
            for word in self.text:
                if word not in self.keywords:
                    head.append(word)
                    tail.pop(0)
                else:
                    break
            if len(head) != 0:
                self.basic_cycle(head)
            if len(tail) != 0:
                self.text = self.if_then_cycle(tail)
            else:
                self.text = []
            self.analyse()

    def basic_cycle(self, text):
        first, second, third = 0, 1, 2
        while first != len(text):
            try:
                assert re.fullmatch(self.identif, text[first])
                if text[first] not in self.idents.keys():
                    self.idents[text[first]] = self.id_idents
                self.id_idents += 1
                self.table.append(text[first]+';Идентификатор;'+str(self.idents[text[first]]))
            except AssertionError:
                self.handle(text[first])
            try:
                assert text[second] == self.equal
                self.table.append(text[second] + ';Знак присваивания')
            except AssertionError:
                print('Invalid symbol: '+text[second]+', `:=` expected')
            try:
                assert re.fullmatch(self.identif, text[third]) or re.fullmatch(self.number, text[third])
                if re.fullmatch(self.identif, text[third]):
                    if text[third] not in self.idents.keys():
                        self.idents[text[third]] = self.id_idents
                    self.id_idents += 1
                    self.table.append(text[third] + ';Идентификатор;' + str(self.idents[text[third]]))
                else:
                    self.table.append(text[third] + ';Вещественная константа;' + text[third])
            except AssertionError:
                self.handle(text[third])
            first += 3
            second += 3
            third += 3

    def if_then_cycle(self, text):
        def extract_base():
            base = []
            w = text.pop(0)
            while w[-1] != ';':
                base.append(w)
                w = text.pop(0)
            base.append(w[:-1])
            self.basic_cycle(base)

        word = text.pop(0)
        try:
            assert word == 'if'
            if word not in self.kws.keys():
                self.kws[word] = self.id_kws
            self.id_kws += 1
            self.table.append(word + ';Ключевое слово;Х' + str(self.kws[word]))
        except AssertionError:
            print('Invalid keyword: '+word+', `if` expected')
        word = text.pop(0)
        try:
            assert re.fullmatch(self.identif, word)
            if word not in self.idents.keys():
                self.idents[word] = self.id_idents
            self.id_idents += 1
            self.table.append(word + ';Идентификатор;' + str(self.idents[word]))
        except AssertionError:
            self.handle(word)
        word = text.pop(0)
        try:
            assert word in self.compare
            self.table.append(word + ';Оператор сравнения')
        except AssertionError:
            print('Invalid symbol: '+word+', comparison expected')
        word = text.pop(0)
        try:
            assert re.fullmatch(self.identif, word) or re.fullmatch(self.number, word)
            if re.fullmatch(self.identif, word):
                if word not in self.idents.keys():
                    self.idents[word] = self.id_idents
                self.id_idents += 1
                self.table.append(word + ';Идентификатор;' + str(self.idents[word]))
            else:
                self.table.append(word + ';Вещественная константа;' + word)
        except AssertionError:
            self.handle(word)
        word = text.pop(0)
        try:
            assert word == 'then'
            if word not in self.kws.keys():
                self.kws[word] = self.id_kws
            self.id_kws += 1
            self.table.append(word + ';Ключевое слово;Х' + str(self.kws[word]))
        except AssertionError:
            print('Invalid keyword: '+word+', `then` expected')
        extract_base()
        if text[0] != 'else':
            return text
        else:
            word = text.pop(0)
            if word not in self.kws.keys():
                self.kws[word] = self.id_kws
            self.id_kws += 1
            self.table.append(word + ';Ключевое слово;Х' + str(self.kws[word]))
            extract_base()
        return text

    def remove_comments(self, text):
        indexes = []
        for i in range(len(text)):
            if '#' in text[i]:
                indexes.append(i)
        numb_pop = 0
        for i in indexes:
            text.pop(i - numb_pop)
            numb_pop += 1
        for line in text:
            for item in line.split():
                self.text.append(item)

    def handle(self, word):
        if len(word) >= 16:
            print('Invalid identifier: '+word+', line too long')
        elif re.match(r'[0-9]', word):
            print('Invalid identifier: '+word+', line contains invalid symbols')

    def get_table(self):
        return self.table
