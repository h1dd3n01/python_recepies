def counter():
    from collections import Counter
    list = ['a', 'b', 'c', 'd', 'e', 'e', 'a']

    c = Counter(list)
    # ---------------- Find all duplicates ---------------
    # for k ,v in c.items():
    #     if v > 1:
    #         print('Found {} "{}" elements'.format(v ,k))

    # ---------------- List unique elements --------------
    # print(sorted(c))

    # ---------------- Print most common -----------------
    # print(c.most_common(2))


def sort_dict():
    from operator import itemgetter
    rows = [{'first_name': 'John', 'last_name': 'Bob', 'address': 'some_address 5-12'},
            {'first_name': 'Jane', 'last_name': 'Janeth', 'address': 'another_address 9-33'},
            {'first_name': 'Robert', 'last_name': 'Sinser', 'address': 'third_address 1-99'},
            {'first_name': 'Ron', 'last_name': 'Leiut', 'address': 'fourth_address 8-55'}]

    # ------------------------------ Explanation --------------------------------------------

    # In this example we insert our row into sorted function which has a named key parameter
    # Key argument has to be a callable which accepts one element of rows and returns
    # found key from row which will be used for the sort

    # ------------------------------------------------------------------------------------------

    # Function operator.itemgetter takes in indexes as arguments which are used for extracting
    # the correct element from the row. It can be dictionary key, number of element in the list
    # or any other provided value that can be fed to method __getitem__()

    # ------------------------------------------------------------------------------------------

    rows_by_first_name = sorted(rows, key=itemgetter('first_name'))
    rows_by_last_name = sorted(rows, key=itemgetter('last_name'))
    rows_by_address = sorted(rows, key=itemgetter('address'))
    rows_by_first_last_name = sorted(rows, key=itemgetter('first_name', 'last_name'))
    # print(rows_by_first_name)
    # print(rows_by_last_name)
    print(rows_by_address)


class User:
    def __init__(self, user_id, user_name):
        self.user_id = user_id
        self.user_name = user_name

    def __repr__(self):
        return '{}, {}'.format(str(self.user_id), self.user_name)


def sort_object():
    from operator import attrgetter
    usr_list = [User(i, 'name#{}'.format(i)) for i in range(10)]

    # ------------------------ Explanation ------------------------
    # Good to sort out objects of a class if it doesn't support comparison
    # You can also use lambda functions instead of attrgetter, its a matter of tase
    # in most cases attrgetter is faster than lambda and it supports extraction of
    # multiple fields at once

    print(sorted(usr_list, key=attrgetter('user_name')))
    print(sorted(usr_list, key=attrgetter('user_id'), reverse=True))


def group_items():
    from itertools import groupby
    from operator import itemgetter

    # ------------------------ Usecase ------------------------
    # You have a list of dicts or other key-value paired elements and you want to
    # iterate through a specific keyword for example date

    rows = [
        {'address': '5412 N CLARK', 'date': '04/11/2018'},
        {'address': '5148 N CLARK', 'date': '07/23/2018'},
        {'address': '5800 E 58TH', 'date': '01/04/2018'},
        {'address': '2122 N CLARK', 'date': '02/15/2017'},
        {'address': '5645 N RAVESWOOD', 'date': '01/01/2019'},
        {'address': '1060 W ADDISON', 'date': '01/02/2020'},
        {'address': '4810 W BOARDWAY', 'date': '07/23/2018'},
        {'address': '1039 N BROADWAY', 'date': '07/23/2018'},
        {'address': '2811 W GRANVILLE', 'date': '01/01/2019'},
    ]

    # Let's say that you also want to iterate trough key pairs
    # that have similar date.

    # First sort by needed field
    print('Before')
    print('-' * 10)
    print(rows)
    print('-' * 10)
    rows.sort(key=itemgetter('date'))
    print('After')
    print('-' * 10)
    print(rows)
    print('-' * 10)
    # Iterate by groups
    for date, items in groupby(rows, key=itemgetter('date')):
        print(date)
        for i in items:
            print('', i)


def group_items_second_example():
    from itertools import groupby
    from operator import itemgetter

    input = [
        {'dept': '001', 'sku': 'foo', 'transId': 'uniqueId1', 'qty': 100},
        {'dept': '001', 'sku': 'bar', 'transId': 'uniqueId2', 'qty': 200},
        {'dept': '001', 'sku': 'foo', 'transId': 'uniqueId3', 'qty': 300},
        {'dept': '002', 'sku': 'baz', 'transId': 'uniqueId4', 'qty': 400},
        {'dept': '002', 'sku': 'baz', 'transId': 'uniqueId5', 'qty': 500},
        {'dept': '002', 'sku': 'qux', 'transId': 'uniqueId6', 'qty': 600},
        {'dept': '003', 'sku': 'foo', 'transId': 'uniqueId7', 'qty': 700}
    ]

    # 1) Get output based on aggregation
    # 2) Get output based on average

    grouped = itemgetter('dept', 'sku')
    aggregation_result = []
    average_result = []
    # -------------------- Aggregation --------------
    for key, group in groupby(sorted(input, key=grouped), grouped):
        temp_dict = dict(zip(['dept', 'sku'], key))
        temp_dict['qty'] = sum(item['qty'] for item in group)
        aggregation_result.append(temp_dict)
        # print(i for i in aggregation_result)
    # --------------------- Average ------------------
    for key, group in groupby(sorted(input, key=grouped), grouped):
        temp_dict = dict(zip(['depth', 'sku'], key))
        temp_list = [item['qty'] for item in group]
        temp_dict['avg'] = sum(temp_list) / len(temp_list)
        average_result.append(temp_dict)
        # print(i for i in temp_dict)


def chain_dict():
    from collections import ChainMap
    d1 = {'first': 'first', 'second': 'second', 'third': 'third', 'fourth': 'fourth'}
    d2 = {'fifth': 'fifth', 'sixth': 'sixth', 'seventh': 'seventh', 'eight': 'eight'}

    # ------------------------ Usecase ---------------------------------------------
    # If you need to iterate through some dictionaries looking for a specific value,
    # ChainMap is the perfect solution, it is same as Chain for lists, it accepts
    # n iterables, and goes through each one until it finds the value that you need

    c = ChainMap(d2, d1)
    for i in c:
        if c[i] == 'third':
            print('found third')
            print(c[i])


def text_search():
    # ------------------- Usecase --------------------------
    # you need to check if a certaing text or file starts or ends with a specific character
    filename = 'spam.txt'
    print('Does filename end with text = {}'.format(filename.endswith('.txt')))
    print('Does filename start with text = {}'.format(filename.startswith('file:')))
    url = 'http://python.org'
    print('Does url start with http = {}'.format(url.startswith('http')))

    # To check multiple files / items starts/endswith can be passed inside iterable
    import os

    filenames = os.listdir('.')
    print(filenames)
    print([name for name in filenames if name.endswith('.py')])


def round_values():
    print('Basevalue is 1.33, rounded is {}'.format(round(1.33)))
    print('Basevalue is 1.53, rounded is {}'.format(round(1.53)))


def partial():
    from functools import partial
    # -------------------------- Usecase --------------------------
    # You have a callable that you want to use, but it accepts too many arguments
    # and throws a exception. If you need to limit the amount of arguments of your callable
    # use functools.partial. Partial allows you to declare a fixed amount of arguments
    # that a callable can recieve
    def spam(a, b, c, d):
        print(a, b, c, d)

    s1 = partial(spam, 1)
    s2 = partial(spam, d=42)
    s3 = partial(spam, 1, 2, d=42)
    s1(2, 3, 4)
    s2(4, 5, 5)
    s3(5)
    print(s1(2, 3, 4))
    print(s2(1, 2, 3))
    print(s3(3))


if __name__ == '__main__':
    pass
    # counter()             1
    # print(sort_dict())    2
    # sort_object()         3
    # group_items()         4
    # group_items_second_example()  5
    # chain_dict()          6
    # text_search()         7
    # round_values()        8
    # partial()             9
