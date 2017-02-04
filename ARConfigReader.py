import json


class ARConfigReader:
    def __init__(self, config_file):
        with open(config_file) as f:
            self.config = json.load(f)
            self.unknown_rarity = 'U'

    def get_lancer_info(self, lancer):
        for lancer_info in self.config['Lancers']:
            if lancer_info['Name'] == lancer:
                return lancer_info

    def get_skins_from_style(self, lancer, style):
        lancer_info = self.get_lancer_info(lancer)
        for skin_style, skins in lancer_info['Skins'].iteritems():
            if skin_style == style:
                return skins

    def get_path_to_skins(self):
        if 'PathToSkins' in self.config:
            return self.config['PathToSkins']

    def get_skin_name(self, lancer, skin_style, skin_id):
        skins = self.get_skins_from_style(lancer, skin_style)
        for skin in skins:
            if skin['Id'] == skin_id:
                return skin['Name'] if not skin['Rarity'] == self.unknown_rarity else None

    def get_skin_rarity(self, lancer, skin_style, skin_id):
        skins = self.get_skins_from_style(lancer, skin_style)
        for skin in skins:
            if skin['Id'] == skin_id:
                return skin['Rarity'] if not skin['Rarity'] == self.unknown_rarity else None

    def get_style_name(self, lancer, skin_style):
        return self.get_skin_name(lancer, skin_style, 'Name')

    def get_all_skins(self, lancer):
        lancer_info = self.get_lancer_info(lancer)
        return lancer_info['Skins']

    def get_display_name(self, lancer):
        lancer_info = self.get_lancer_info(lancer)
        return lancer_info['Display_Name']
