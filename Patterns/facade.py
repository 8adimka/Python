import json

from adapter import CSVReader, JSONReader


class Facade:
    def __init__(self):
        self.csv_reader = CSVReader()
        self.json_reader = JSONReader()

    def get_data(self, source):
        try:
            file = self.json_reader.get_data(source)
            return file

        except json.JSONDecodeError:
            try:
                file = self.csv_reader.get_data(source)
                return file

            except Exception:
                pass

        return None


class Printer:
    def __init__(self):
        self.facade = Facade()

    def print(self, source):
        data = self.facade.get_data(source)
        if data is None:
            print("\nNo valid data found!\n__________________________________________")
            return

        for line in data:
            print(
                f"\n*We can offer you: {line['Название']}.\nColor - {line['Color']}\nWeight - {line['Weight']}"
            )
        print("\nThat's all, folks!\n__________________________________________")


CSV = "Название;Color;Weight;\nКот;Редкий окрас (скумбрия на снегу);3\nПес;Черный;15\nЧерепаха;Серый;0.2"
JSON = '{"items":[{"Название":"Bear","Color":"Brown", "Weight":150}, {"Название":"Fox","Color":"Red", "Weight":"7"}]}'

printer = Printer()

printer.print(CSV)
printer.print(JSON)
