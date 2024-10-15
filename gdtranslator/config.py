import yaml
from dataclasses import dataclass, field


@dataclass
class ServerConfig:
    api_key: str = ""
    base_url: str = ""
    model: str = ""
    price: dict[str, float] = field(default_factory=lambda: {})
    lock_file_path: str = ""

    def load_server_config_from_yaml(self, file_path):
        with open(file_path, "r") as file:
            config_data = yaml.safe_load(file)
            self.api_key = config_data["server"]["api_key"]
            self.base_url = config_data["server"]["base_url"]
            self.model = config_data["server"]["model"]
            price = config_data["server"]["price"]
            price = {key: float(value) for key, value in price.items()}
            self.price = price
            self.lock_file_path = config_data["server"]["lock_file_path"]


server_config = ServerConfig()
