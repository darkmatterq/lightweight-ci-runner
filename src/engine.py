from parser import parse_pipeline_config
import os
import sys
import docker
import subprocess
import time


class CIRunner:
    def __init__(self, config_path):
        self.config_path = config_path
        self.workspace_dir = os.path.abspath(os.getcwd())
        try:
            self.client = docker.from_env()
            self.client.ping()
        except Exception as e:
            print(
                f"Error: Cannot connect to Docker Daemon.\
                      Is Docker running? \n{e}")
            sys.exit(1)

    def run_stage(self, stage_name, stage_config):
        cmd_str = " && ".join(stage_config['commands'])
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

            container_kwargs = {
                'image': stage_config['image'],
                'command': entry_command,
                'working_dir': '/workspace',
                'volumes': volumes,
                'network_mode': 'host',
                'detach': True
            }
            if 'memory' in stage_config:
                container_kwargs['mem_limit'] = stage_config['memory']
            if 'cpus' in stage_config:
                container_kwargs['nano_cpus'] = int(
                    float(stage_config['cpus'])*1e9)
            container = self.client.containers.create(**container_kwargs)
            container.start()
            monitor_bin = os.path.join(self.workspace_dir, "bin", "ci-monitor")
            monitor_proc = None
            if os.path.exists(monitor_bin):
                try:
                    monitor_proc = subprocess.Popen(
                        [monitor_bin, container.id, "500"])
                except Exception as me:
                    print(f"Warning: Could not start C++ monitor: {me}")
            for chunk in container.logs(
                    stream=True, follow=True, stdout=True, stderr=True):
                print(chunk.decode('utf-8', errors='replace'), end='')
            timeout_val = stage_config.get('timeout', 60)
            result = container.wait(timeout=timeout_val)
            if monitor_proc and monitor_proc.poll() is None:
                try:
                    monitor_proc.terminate()
                    monitor_proc.wait(timeout=2)
                except Exception:
                    monitor_proc.kill()
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
        stage_status = {}
        stage_duration = {}
        pipeline_success = True
        for stage_name in config['stages']:
            start_time = time.perf_counter()
            print(
                f"\n==================[STAGE:{stage_name}]"
                "====================="
            )
            success = self.run_stage(stage_name, config[stage_name])
            if not success:
                print(f"\n Pipeline FAILED at stage [{stage_name}]!")
                stage_status[stage_name] = "FAILED"
                pipeline_success = False
                end_time = time.perf_counter()
                stage_duration[stage_name] = end_time-start_time
                break
            else:
                stage_status[stage_name] = "PASSED"

            print(f"Stage[{stage_name}] PASSED.")
            end_time = time.perf_counter()

            stage_duration[stage_name] = end_time-start_time
        print("====================== PIPELINE SUMMARY ======================")
        for stage_name in config['stages']:
            if stage_name not in stage_status:
                stage_status[stage_name] = "SKIPPED"
                stage_duration[stage_name] = 0.0
            print(
                f"Stage: {stage_name:<8}"
                f" | Status:{stage_status[stage_name]:<8}"
                f" | Duration: {round(stage_duration[stage_name], 2)}s"
            )
        if pipeline_success:
            print("\n ALL STAGES PASSED! Pipeline completed successfully.")
            return True
        print("\n Pipeline FAILED! ")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 src/engine.py <path-to-yaml-file>")
        sys.exit(1)
    config_file = sys.argv[1]
    runner = CIRunner(config_file)
    success = runner.run_pipeline()
    sys.exit(0 if success else 1)
