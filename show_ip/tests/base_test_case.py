import pytest
import os
import csv


class BaseCSVTestCase:
    @pytest.fixture()
    def load_csv(self):
        path = os.path.abspath('test.csv')
        with open(path, mode='w') as employee_file:
            employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            employee_writer.writerow(["www.example.com", "tak"])
            employee_writer.writerow(["www.example2.com"])
        yield path
        os.remove(path)

    @pytest.fixture()
    def load_empty_csv(self):
        path = os.path.abspath('test.csv')
        with open(path, mode='w') as employee_file:
            csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        yield path
        os.remove(path)

    @pytest.fixture()
    def load_random_file(self):
        path = os.path.abspath('test.txt')
        with open(path, mode='w') as employee_file:
            employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            employee_writer.writerow(["www.example.com", "tak"])
        yield path
        os.remove(path)
