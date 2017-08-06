
class reader_input:
    '''
    General class parsing the data input
    '''
    def __init__(self, file_path):
        self.file = open(file_path, "r")

        self.profile = ""
        self.read_file()

        self.file.close()

    def read_file(self):
        '''
        Internal function reading the input file line by line
        '''
        for line in self.file:
            divided = line.split()
            if (divided[0] == "PROFILE"):
                self.profile = str(divided[1])


