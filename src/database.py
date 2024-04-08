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
                    metrics = [int(val) for val in keys[1].split(',')]
                    self.results[keys[0]] = metrics
            self.results = dict(sorted(self.results.items(), key=lambda item: item[1], reverse=True))

    def safe_result(self, username: str, result: int, total_keys: int, accuracy: int):
        metrics = [result, total_keys, accuracy]
        user_result = self.results.get(username, [-1, -1, -1])
        if user_result[0] < result or user_result[1] < total_keys or user_result[2] < accuracy:
            self.results[username] = metrics
            with open(self.results_file, 'w') as f:
                for name, result in self.results.items():
                    result = [str(val) for val in result]
                    f.write(f'{name}:{",".join(result)}\n')
