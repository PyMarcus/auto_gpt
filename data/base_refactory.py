import csv


class BaseRefactory:
    """
    Reescreve o novo csv
    """
    @staticmethod
    def run(path: str) -> None:
        with open(path, 'r') as f:
            ids = f.readlines()
        with open("removidos.csv", mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            data = [row for index, row in enumerate(reader) if row["id"]
                    in [id.strip().replace("\n", "") for id in ids] and index > 0]

        with open("filtered.csv", mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)


if __name__ == '__main__':
    BaseRefactory.run("ids.txt")
