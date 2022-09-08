class FilePatternError(Exception):
    def __init__(self):
        self.message = (
            "\n\nThe employee schedule file is out of the pattern.\n"
            "Please review your file content"
        )
        super().__init__(self.message)
