import tempfile, subprocess, os

class pdf_to_text():

    def __init__(self, root_path, style = '-layout'):
        '''
        The class function will convert all pdf files within the directory into text files
        :param root_path: input the root path for all pdf files
        :param style:

        -layout(default)     : maintain original physical layout
        -table               : similar to -layout, but optimized for tables
        -lineprinter         : use strict fixed-pitch/height layout
        -raw                 : keep strings in content stream order
        '''

        self.root_path = root_path
        self.style = style
        self.filePath = []

    def find_all(self):

        dir_list = os.walk(self.root_path)

        for root, dirs, files in dir_list:
            for file in files:
                self.filePath.append(os.path.join(root, file))

    def convert(self):

        self.find_all()

        for file in self.filePath:

            output = tempfile.NamedTemporaryFile()
            output_file = file.replace('.pdf', '.txt')

            out, err = subprocess.Popen(['pdftotext', self.style, file, output.name]).communicate()

            pdf = output.read()

            pdf = pdf.decode('windows-1252')

            if not os.path.isfile(output_file):
                with open(output_file, 'w') as f:
                    f.write(pdf)

if __name__ == '__main__':

    root_path = '/Users/maxwelllee54/GitHubs/Rapid_Assessment_Tools/SharedFiles/Fordham/RIA Bhutan/Docs Reviewed'
    pdf_to_text(root_path).convert()
