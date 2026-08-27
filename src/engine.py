import os
import sys
import docker
from parser import parse_pipeline_config


class CIRunner:
    def __init__(self, config_path):
        self.config_path = config_path
        self.workspace_dir = os.path.abspath(os.getcwd())
        try:
            self.client = docker.from_env()
            self.client.ping()
        except Exception as e:
            print(
                f"Error: Cannot connect to Docker Deamon.\
                      Is Docker running? \n{e}")
            sys.exit(1)

    def run_stage(self, stage_name, stage_config):
        self.stage_name = stage_name
        self.stage_config = stage_config
        cmd_str = " && " .join(stage_config['commands'])
        entry_command = f"sh -c 'set -e && {cmd_str}'"
        volumes = {
            self.workspace_dir: {
                'bind': '/workspace',
                'mode': 'rw'
            }
        }
        if 'docker' in stage_config['image']:
            volumes['/var/run/docker.sock'] = {
                'bind': '/var/run/docker.sock', 'mode': 'rw'}

        container = None
        try:
            print(f"Pulling image: {stage_config['image']}...")
            self.client.images.pull(stage_config['image'])
            print(f"Starting container for stage[{stage_name}]...")
            container = self.client.containers.create(
                image=stage_config['image'],
                command=entry_command,
                working_dir='/workspace',
                volumes=volumes,
                network_mode='host',
                detach=True
            )
            container.start()
            for chunk in container.logs(
                    stream=True, follow=True, stdout=True, stderr=True):
                print(chunk.decode('utf-8', errors='replace'), end='')
            timeout_val = stage_config.get('timeout', 60)
            result = container.wait(timeout=timeout_val)
            exit_code = result.get('StatusCode', 1)
            return exit_code == 0
        except Exception as e:
            print(f"Error running stage [{stage_name}]:{e}")
            return False
        finally:
            if container:
                try:
                    container.remove(force=True)
                except Exception:
                    pass

    def run_pipeline(self):
        config = parse_pipeline_config(self.config_path)
        print(f"Running Pipeline:{config['name']}")
        for stage_name in config['stages']:
            print(
                f"\n==================[STAGE:{stage_name}]"
                "====================="
            )
            success = self.run_stage(stage_name, config[stage_name])
            if not success:
                print(f"\n Pipeline FAILED at stage [{stage_name}]!")
                return False

            print(f"Stage[{stage_name}] PASSED.")
        print("\n ALL STAGES PASSED! Pipeline completed successfully.")
        return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 src/engine.py <path-to-yaml-file>")
        sys.exit(1)
    config_file = sys.argv[1]
    runner = CIRunner(config_file)
    success = runner.run_pipeline()
    sys.exit(0 if success else 1)
