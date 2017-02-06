import os
import shutil
from ARSkinFilenameParser import ARSkinFilenameParser
from ARConfigReader import ARConfigReader
from ARConstants import ARConstants
import ARArgParser


class RenameSkinsAR:
    def __init__(self, config_file, path_to_skins=None):
        self.config_reader = ARConfigReader(config_file)
        self.constants = ARConstants()
        self.arsfp = ARSkinFilenameParser()
        self.path_to_skins = path_to_skins

    def get_dir(self):
        if self.path_to_skins is None:
            path_to_skins = self.config_reader.get_path_to_skins()
        else:
            path_to_skins = self.path_to_skins
        if path_to_skins is None:
            folder = os.path.dirname(os.path.realpath(__file__))
        else:
            folder = path_to_skins
        return folder

    def get_output_dir(self):
        skin_dir = self.get_dir()
        output = "/".join([skin_dir, "rename"])
        try:
            os.mkdir(output)
        except WindowsError:
            pass
        return output

    def get_all_lancers(self):
        config = self.read_config()
        output = []
        if 'Lancers' in config:
            for lancer in 'Lancers':
                output.append(lancer['Name'])
        return output

    def get_lancer_filenames(self, lancer):
        all_files = self.get_file_list()
        output = []
        for filename in all_files:
            if self.is_lancer_file(lancer, filename):
                output.append(filename)
        return output

    def is_lancer_file(self, lancer, filename):
        compare = self.arsfp.parse_filename(filename)
        if not compare:
            return False
        return compare['lancer'] == lancer

    def get_file_list(self):
        output = []
        skin_dir = self.get_dir()
        for root, dirs, files in os.walk(skin_dir):
            if root == skin_dir:
                output.extend(files)
                break
        return output

    def rename_skins(self, lancer):
        # Find list of files for that lancer
        filenames = self.get_lancer_filenames(lancer)
        # Determine new name
        skin_names = self.generate_names(filenames)
        # Perform copy action
        self.perform_rename(skin_names)
        return True

    def generate_names(self, filenames):
        output = []
        for filename in filenames:
            elements = self.arsfp.parse_filename(filename)
            if not elements:
                continue
            display_name = self.config_reader.get_display_name(elements['lancer'])
            if not display_name:
                print " ".join([
                    'New lancer "',
                    elements['lancer'],
                    '" found. Please add to config file.'])
            skin_name = self.config_reader.get_skin_name(
                elements['lancer'],
                elements['skin_style'],
                elements['skin_id'])
            if not skin_name:
                print " ".join([
                    'New skin"',
                    elements['skin_id'],
                    elements['skin_style'],
                    '"found. Please update config for new skin'])
                continue
            style_name = self.config_reader.get_style_name(
                elements['lancer'],
                elements['skin_style'])
            if not style_name:
                print "".join([
                    'New skin style "',
                    elements['skin_style'],
                    '" found.  Please update config for new skins.'])
                continue
            newname = self.gen_newname(
                display_name,
                style_name,
                skin_name)
            result = (filename, newname)
            output.append(result)
        return output

    def gen_newname(self, lancer, style, name):
        return "-".join([lancer, style, name])

    def perform_rename(self, skin_names):
        source_rt = self.get_dir()
        dest_rt = self.get_output_dir()
        for skin in skin_names:
            source_file = skin[0]
            dest_file = "".join([skin[1], '.png'])
            print " ".join([source_file, "-->", dest_file])
            source = os.path.join(source_rt, source_file)
            dest = os.path.join(dest_rt, dest_file)
            shutil.copyfile(source, dest)
        return True

    def generate_full_wiki_string(self, lancer):
        skins = self.config_reader.get_all_skins(lancer)
        output = []
        for style, ids in skins.iteritems():
            for skin in ids:
                if skin[self.constants.rarity] == 'U' or skin[self.constants.rarity] == 'Name':
                    continue
                new_wiki = "".join([
                    '{{Style|',
                    skin[self.constants.skin_name],
                    "|",
                    skin[self.constants.rarity],
                    '}}'])
                output.append(new_wiki)
        result = " ".join(output)
        return result

    def run(self, lancers=[]):
        if not lancers:
            lancers = self.get_all_lancers()
        output_dir = self.get_output_dir()
        for lancer in lancers:
            print "".join(['Renaming ', lancer, ' skins...'])
            self.rename_skins(lancer)
            wiki_string = self.generate_full_wiki_string(lancer)
            print "".join([
                'Use the following string to add skins to ',
                lancer,
                ' profile on Wiki: ',
                wiki_string])
        print "".join(['Renamed images can be found at: ', output_dir])


args = vars(ARArgParser.parse())
new_skins = RenameSkinsAR(args['config'], path_to_skins=args['skin_dir'])
new_skins.run([args['lancer']])

#config_file = 'config.json'
#new_skins = RenameSkinsAR(config_file)
#new_skins.run(['Garrison'])
