from chartsbot import WidgetWrapper, Parser
from config import details


def main():
    widget = WidgetWrapper(details)
    parser = Parser()
    table = parser.get_top_10()
    widget.make_update(table)


if __name__ == "__main__":
    main()
