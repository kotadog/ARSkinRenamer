import os
from ARConstants import ARConstants


class ARCsvReader:
    def __init__(self, csv_dir):
        self.imported_data = self.format_data(csv_dir)
        self.constants = ARConstants()

    def get_csv_dir(self):
        return self.csv_dir

    def get_files(self, csv_dir):
        output = []
        for root, dirs, files in os.walk(csv_dir):
            if root == csv_dir:
                output.extend(files)
                break
        return output

    def format_data(self, csv_dir):
        output = {}
        files = self.get_files(csv_dir)
        for filename in files:
            skin_data = self.export_skin_data(filename)
            metadata = self.parse_metadata(skin_data[0].split(self.constants.delim))
            skin_info = self.format_skin_data(skin_data)
            result = self.build_skin_output(metadata, skin_info)
            if lancer_id not in output:
                output[lancer_id] = {}
                output[lancer_id][self.constants.lancer_name] = lancer_name
                output[lancer_id][self.constants.skins] = {}
            output[lancer_id][self.constants.skins].update(result)
        return output

    def export_skin_data(self, filename):
        loc = os.path.join(self.get_csv_dir(), filename)
        with open(filename) as f:
            contents = f.read().split('\n')
        return contents

    def build_skin_output(self, metadata, skin_data):

        name_item = {}
        name_item[self.constants.skin_id] = self.constants.skin_id
        name_item[self.constants.skin_name] = parse_meta[self.constants.skin_name]
        name_item[self.constants.rarity] = self.constants.skin_id
        result[parsed_meta[self.constants.lancer_name]][self.constants.skins][parsed_meta[self.constants.skin_id]].append(new_item)
        result[parsed_meta[self.constants.lancer_name]][self.constants.skins][parsed_meta[self.constants.skin_id]].append(skin_data)
        return result

    def parse_metadata(self, metadata):
        lancer_id = metadata[0]
        lancer_name = metadata[1]
        skin_id = metadata[2]
        skin_name = metadata[3]
        output = {}
        output[self.constants.lancer_name] = lancer_id
        output[self.constants.lancer_display_name] = lancer_name
        output[self.constants.skin_id] = skin_id
        output[self.constants.skin_name] = skin_name
        return output

    def format_skin_data(self, skin_data):
        output = []
        labels = skin_data[2].split(self.constants.delim)
        for skin in skin_data[3:]:
            skin_info = skin.split(self.constants.delim)
            result = {}
            for index, value in skin_info.enumerate():
                result[labels[index]] = skin_info[index]
            output.append(result)
        return output