import copy
import os


class Database:
    def __init__(self):
        self.results = {}
        self._results_file = 'result.txt'
        self._load_last_results()
        # in order to remove duplicates and create correct table
        self._dump_results()

    def _load_last_results(self):
        if not os.path.exists(self._results_file):
            self.results = {}
        else:
            with open(self._results_file, 'r') as f:
                for row in f:
                    if not row:
                        continue
                    keys = row.rstrip('\n').split(':')
                    metrics = [int(val) for val in keys[1].split(',')]
                    if keys[0] in self.results and metrics < self.results[keys[0]]:
                        continue
                    self.results[keys[0]] = metrics
            self.results = dict(sorted(self.results.items(), key=self._sorter, reverse=True))

    def safe_result(self, username: str, result: int, total_keys: int, accuracy: int):
        metrics = [result, total_keys, accuracy]
        user_result = self.results.get(username, [-1, -1, -1, 0])
        metrics.append(user_result[-1])

        if user_result[0] < result or user_result[1] < total_keys or user_result[2] < accuracy:
            self.results[username] = metrics
        self.results[username][-1] += 1
        self._dump_results()

    def _dump_results(self):
        with open(self._results_file, 'w') as f:
            for name, result in self.results.items():
                result = [str(val) for val in result]
                f.write(f'{name}:{",".join(result)}\n')

    def _sorter(self, results: tuple[str, list]) -> list:
        results = copy.copy(results[1])
        results[-1] = 1 / results[-1]
        return results

    def get_table_results(self, number_of_results: int = 20):
        table_results = {}
        for idx, (name, res) in enumerate(self.results.items()):
            if idx >= number_of_results:
                break
            table_results[name] = res
        return table_results

