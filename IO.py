class IO_worker:
    def __init__(self, infilepath):
        self.infilepath = infilepath

    def read(self):
        try:
            infile = open(self.infilepath, 'r')
            return infile.read()
        except FileNotFoundError:
            print("No such file! Try again.")
            return None
