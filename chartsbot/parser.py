from instiz import iChart
from pendulum import now


class Parser:
    def __init__(self):
        self._instance = iChart()
        self._data = None

    def get_top_10(self):
        self._instance.refresh()
        self._data = self._instance.realtime_top_10()
        return self._prettify()

    def _prettify(self):
        output = "# Realtime iChart\n\n"
        output += self._table_formatting()
        output += "---\n\n"
        output += "Last updated at {}".format(self._get_time())
        return output

    def _table_formatting(self):
        output = "Rank | Artist - Song"
        output += "\n"
        output += " --- | --- \n"
        index = 0
        for data in self._data:
            output += "{rank} | {song}".format(
                rank=index + 1, song=data.nice_title
            )
            output += "\n"
            index += 1
        output += "\n"
        return output

    def _get_time(self):
        return now("Asia/Seoul").to_rfc850_string()

