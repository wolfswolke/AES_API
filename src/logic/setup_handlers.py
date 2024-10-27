import yaml


def load_config():
    with open('config//config.yaml', 'r') as f:
        config_file = yaml.safe_load(f)
    return config_file