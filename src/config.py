import yaml


class Test1Class:
    def __init__(self, raw):
        self.minVolt = raw['minVolt']
        self.maxVolt = raw['maxVolt']


class Test2Class:
    def __init__(self, raw):
        self.curr = raw['curr']
        self.volt = raw['volt']


class Config:
    def __init__(self, raw):
        for sections in raw:
            print(sections)


with open("learning_path.yaml") as config_file:
    config = Config(yaml.safe_load(config_file))

print(config)
