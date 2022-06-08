class FileError(Exception):
    def __init__(self):
        self.message = (
            "\n\nThe employee schedule file was not found.\n"
            "Please attach your file in the root of the project\n"
            "By default, the file should be called 'worked_schedules.txt'. "
            "But you can use another name.\n"
            "Just remember to put your custom file name in the params of "
            "payment() function"
        )
        super().__init__(self.message)
