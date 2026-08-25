import yaml
import os


def parse_pipeline_config(config_path):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with open(config_path, "r") as file:
        data = yaml.safe_load(file)
    if not data or not isinstance(data, dict):
        raise ValueError("Invalid YAML configuration file.")
    if "name" not in data:
        raise ValueError("Pipeline configuration is missing 'name' field.")
    if "stages" not in data or not isinstance(data["stages"], list):
        raise ValueError("Pipeline configuration is missing 'stages' field.")
    for stage_name in data["stages"]:
        if stage_name not in data:
            raise ValueError(f"STage '{stage_name}'\
                              is declared in 'stages'but not defined.")

        stage_data = data[stage_name]
        if "image" not in stage_data:
            raise ValueError(f"Stage '{stage_name}' is missing 'image' field.")

        if "commands" not in stage_data or not (
                isinstance(stage_data["commands"], list)):
            raise ValueError(f"Stage '{stage_name}' is missing 'image' field.")
        if "timeout" not in stage_data:
            stage_data["timeout"] = 60
    return data


if __name__ == "__main__":
    result = parse_pipeline_config("sample-app/.ci-pipeline.yaml")
    print("✅ Parsed successfully! Pipeline Name:", result["name"])
    print("Stages found:", result["stages"])
