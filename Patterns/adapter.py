import json
from abc import ABC, abstractmethod

CSV = "Название;Color;Weight;\nКот;Редкий окрас (скумбрия на снегу);3\nПес;Черный;15\nЧерепаха;Серый;0.2"
JSON = '{"items":[{"Название":"Bear","Color":"Brown", "Weight":150}, {"Название":"Fox","Color":"Red", "Weight":"7"}]}'


class Adapter(ABC):
    @abstractmethod
    def get_data(self, source) -> dict:
        pass


class CSVReader(Adapter):
    def get_data(self, source):
        lines = self._split_lines(source)
        headers, data = self._split_headers_with_data(lines)
        return self._format_result(headers, data)

    def _split_lines(self, source) -> list:
        return source.split("\n")

    def _split_headers_with_data(self, lines) -> tuple:
        return lines[0].split(";"), [x.split(";") for x in lines[1:]]

    def _format_result(self, headers, data) -> list:
        items = []
        for line in data:
            items.append(dict(zip(headers, line)))
        return items


class JSONReader(Adapter):
    def get_data(self, source):
        return json.loads(source)["items"]


class Printer:
    def __init__(self, adapter: Adapter):
        self.adapter = adapter
        self.data = None

    def _get_data(self, source):
        self.data = self.adapter.get_data(source)

    def print(self, source):
        self._get_data(source)
        for line in self.data:
            print(
                f"*We can offer you: {line['Название']}.\nColor - {line['Color']}\nWeight - {line['Weight']}"
            )
        print("That's all, folks!\n__________________________________________")


# csv_printer = Printer(adapter=CSVReader())

# csv_printer.print(CSV)

# Printer(adapter=JSONReader()).print(JSON)
