import os
import sys
import json
import time
from ARConfigReader import ARConfigReader
from ARConstants import ARConstants


class JsonToCsv:
    def __init__(self, config_file):
        self.config_reader = ARConfigReader(config_file)
        self.constants = ARConstants()

    def get_lancers(self):
        return self.config_reader.get_all_lancers()

    def convert_lancer(self, lancer_info):
        '''#DrFinn,Dr. Finn,base,Medicine Fish
        #---------------
        #skin_id,skin_name,rarity
        #000_000,Oceanic,C'''
        output = []
        for skin_id, skin_info in lancer_info[self.constants.skins].iteritems():
            result = []
            result.append(self.create_header_row(lancer_info, skin_id))
            result.append("-" * 25)
            result.append('skin_id,skin_name,rarity')
            for skin in skin_info:
                if skin[self.constants.skin_id] == self.constants.name:
                    continue
                result.append(self.create_skin_row(skin))
            output.append(result)
        return output

    def create_header_row(self, lancer_info, skin_id):
        lancer_id = lancer_info[self.constants.lancer_name]
        lancer_ign = lancer_info[self.constants.lancer_display_name]
        skin_name = ''
        for info in lancer_info[self.constants.skins][skin_id]:
            if info[self.constants.skin_id] == 'Name':
                skin_name = info[self.constants.skin_name]
                break
        return ",".join([lancer_id, lancer_ign, skin_id, skin_name])

    def create_skin_row(self, skin):
        return ",".join([skin[self.constants.skin_id], skin[self.constants.skin_name], skin[self.constants.rarity]])

    def write_csvs(self, result, output_dir):
        for new_file in result:
            title = "-".join(new_file[0].split(',')) + '.csv'
            joined = "\n".join(new_file)
            filename = os.path.join(output_dir, title)
            print "".join(['Writing new file: ', filename])
            with open(filename, 'w') as f:
                f.write(joined)
        return True

    def run(self, output_dir):
        lancers = self.get_lancers()
        for lancer in lancers:
            result = self.convert_lancer(lancer)
            self.write_csvs(result, output_dir)
        return True


class CsvToJson:
    def __init__(self, csv_dir):
        self.csv_dir = csv_dir
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

    def format_data(self):
        csv_dir = self.get_csv_dir()
        output = []
        files = self.get_files(csv_dir)
        for filename in files:
            skin_data = self.export_skin_data(filename)
            metadata = self.parse_metadata(skin_data[0].split(self.constants.delim))
            skin_info = self.format_skin_data(skin_data)
            result = self.build_skin_output(metadata, skin_info)
            try:
                self.update_output(metadata, result, output)
            except:
                print 'meta: ', metadata
                print 'skin_info: ', skin_info
                print 'result: ', result
                print 'output: ', output
                exit()
        return output

    def export_skin_data(self, filename):
        loc = os.path.join(self.get_csv_dir(), filename)
        with open(loc) as f:
            contents = f.read().split('\n')
        return contents

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

    def build_lancer_info(self, metadata):
        output = {}
        output[self.constants.lancer_name] = metadata[self.constants.lancer_name]
        output[self.constants.lancer_display_name] = metadata[self.constants.lancer_display_name]
        output[self.constants.skins] = {}
        return output

    def format_skin_data(self, skin_data):
        output = []
        labels = skin_data[2].split(self.constants.delim)
        for skin in skin_data[3:]:
            skin_info = skin.split(self.constants.delim)
            result = {}
            for index, value in enumerate(skin_info):
                result[labels[index]] = skin_info[index]
            output.append(result)
        return output

    def build_skin_output(self, metadata, skin_data):
        name_item = {}
        name_item[self.constants.skin_id] = self.constants.name
        name_item[self.constants.skin_name] = metadata[self.constants.skin_name]
        name_item[self.constants.rarity] = self.constants.name
        result = {}
        result[metadata[self.constants.skin_id]] = []
        result[metadata[self.constants.skin_id]].append(name_item)
        result[metadata[self.constants.skin_id]].extend(skin_data)
        return result

    def update_output(self, metadata, result, output):
        for lancer in output:
            if lancer[self.constants.lancer_name] == metadata[self.constants.lancer_name]:
                lancer[self.constants.skins].update(result)
        else:
            new_lancer = self.build_lancer_info(metadata)
            output.append(new_lancer)
            output[-1][self.constants.skins].update(result)


    def write_to_json(self, imported_data, output_file):
        with open(output_file, 'w') as f:
            json.dump(imported_data, f, indent=2)

    def run(self, output_file):
        imported_data = self.format_data()
        self.write_to_json(imported_data, output_file)


if __name__ == '__main__':
    if sys.argv[1] == 'j2c':
        converter = JsonToCsv('config.json')
        converter.run(
            'csvs')
    if sys.argv[1] == 'c2j':
        converter = CsvToJson('csvs\\')
        converter.run(
            'new_config.json')
