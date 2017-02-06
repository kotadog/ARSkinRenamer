import json
from ARConstants import ARConstants


class ARConfigReader:
    def __init__(self, config_file):
        self.constants = ARConstants()
        with open(config_file) as f:
            self.config = json.load(f)

    def get_all_lancers(self):
        return self.config

    def get_lancer_info(self, lancer):
        for lancer_info in self.config:
            if lancer_info[self.constants.lancer_display_name] == lancer:
                return lancer_info

    def get_skins_from_style(self, lancer, style):
        lancer_info = self.get_lancer_info(lancer)
        for skin_style, skins in lancer_info[self.constants.skins].iteritems():
            if skin_style == style:
                return skins

    def get_skin_name(self, lancer, skin_style, skin_id):
        skins = self.get_skins_from_style(lancer, skin_style)
        for skin in skins:
            if skin[self.constants.skin_id] == skin_id:
                return skin[self.constants.skin_name] if not skin[self.constants.rarity] == self.constants.unknown_rarity else None

    def get_skin_rarity(self, lancer, skin_style, skin_id):
        skins = self.get_skins_from_style(lancer, skin_style)
        for skin in skins:
            if skin[self.constants.skin_id] == skin_id:
                return skin[self.constants.rarity] if not skin[self.constants.rarity] == self.constants.unknown_rarity else None

    def get_style_name(self, lancer, skin_style):
        return self.get_skin_name(lancer, skin_style, self.constants.name)

    def get_all_skins(self, lancer):
        lancer_info = self.get_lancer_info(lancer)
        return lancer_info[self.constants.skins]

    def get_display_name(self, lancer):
        lancer_info = self.get_lancer_info(lancer)
        return lancer_info[self.constants.lancer_display_name]
