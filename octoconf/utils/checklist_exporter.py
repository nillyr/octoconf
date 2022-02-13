import sys

class ChecklistExporter:
    """
    Class responsible for the export of checklists.
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def export(src: str, dst: str) -> int:
        try:
            with open(src, "r") as checklist:
                content = checklist.read()
            with open(dst, "w+") as output:
                output.write(content)
        except FileNotFoundError as _err:
            print(
                f"Error: Checklist not found. Error message: {_err}",
                file=sys.stderr,
            )
            return 1
        return 0
