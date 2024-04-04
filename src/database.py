import os


class Database:
    def __init__(self):
        self.results = {}
        self.results_file = 'result.txt'
        self.load_last_results()

    def load_last_results(self):
        if not os.path.exists(self.results_file):
            self.results = {}
        else:
            with open(self.results_file, 'r') as f:
                for row in f:
                    keys = row.rstrip('\n').split(':')
                    self.results[keys[0]] = int(keys[1])
            self.results = dict(sorted(self.results.items(), key=lambda item: item[1], reverse=True))

    def safe_result(self, username: str, result: int):
        if self.results.get(username, 0) < result:
            self.results[username] = result
        try:
            with open(self.results_file, 'w') as f:
                for name, result in self.results.items():
                    f.write(f'{name}:{result}\n')
        except Exception:
            print(self.results)
