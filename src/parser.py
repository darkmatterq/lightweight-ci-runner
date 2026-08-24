import yaml
import os
def parse_pipeline_config(config_path):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, "r") as file:
        data = yaml.safe_load(file)
    if not data or not isinstance(data,dict):
        raise ValueError("Invalid YAML configuration file.")
    if "name" not in data:
        raise ValueError("Pipeline configuration is missing 'name' field.")
    if "stages" not in data or not isinstance(data["stages"],list):
        raise ValueError("Pipeline configuration is missing 'name' field.")
    for stage_name in data["stages"]:
        if not (stage_name["image"] and stage_name["commands"]):
            raise ValueError("Pipeline configuration is missing 'name' field.")
        if not stage_name["timeout"]:
            stage_name["timeout"]=60
   return data 

