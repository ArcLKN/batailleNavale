import os
import json

class Save():

    def __init__(self):
        pass

    def create_data(self):
        with open(f"save.json", 'w') as json_file:
            base_dic = {}
            json.dump(base_dic, json_file, sort_keys=True, indent=4)
            return

    def load_data(self, base_dir):
        if os.path.exists(rf"{base_dir}\save.json"):
            with open(f"save.json") as json_file:
                data = json.load(json_file)
                json_file.close()
            return data
        return None


    def save_data(self, data):
        with open(f'save.json', 'w') as json_file:
            json.dump(data, json_file, sort_keys=True, indent=4)
            json_file.close()

    def create_files(self, base_dir):
        if os.path.exists(rf"{base_dir}\save.json"):
            data = self.load_data(base_dir)
            return data
        self.create_data()
        data = self.load_data(base_dir)
        return data