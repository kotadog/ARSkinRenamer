import re
import time


class ARSkinFilenameParser:
    def __init__(self):
        self.delim = "_"

    def split_file(self, filename):
        if filename[-4:] == '.png':
            output = re.split(self.delim, filename[:-4])
        else:
            output = re.split(self.delim, filename)
        return output

    def valid_file(self, objects):
        return len(objects) == 5

    def locate_lancer(self, obj):
        return obj[1]

    def locate_skin_style(self, obj):
        return obj[2]

    def locate_skin_id(self, obj):
        return "_".join(obj[3:])

    def parse_filename(self, filename):
        output = {}
        objects = self.split_file(filename)
        if not self.valid_file(objects):
            return False
        output['lancer'] = self.locate_lancer(objects)
        output['skin_style'] = self.locate_skin_style(objects)
        output['skin_id'] = self.locate_skin_id(objects)
        return output
