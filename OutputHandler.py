
import csv

class OutputHandler:

    def __init__(self, output_filename):
        self.output_filename = output_filename
        self.initialized = False

    def write(self, data):
        if not self.initialized:
            self.file_handle = open(self.output_filename, "w")  # TODO handle exceptions
            keys = data.keys()
            self.writer = csv.DictWriter(self.file_handle, keys)
            self.writer.writeheader()
            self.initialized = True

        self.writer.writerow(data)
        print(data)

    def close(self):
        if self.initialized:
            self.file_handle.close()
