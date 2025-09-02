import time
import json
import requests
import platform
import subprocess
import psutil
import uuid
import pandas as pd
import os
from typing import Dict
from enum import Enum


class StartType(Enum):
    COLDSTART = "cold"
    WARMSTART = "warm"


def calculate_average_cpu_usage(cpus_before, cpus_after):
    total_idle_diff = 0
    total_time_diff = 0

    # Calculate the total idle and total time differences for all cores
    for t0, t1 in zip(cpus_before, cpus_after):
        # Calculate the difference in idle time
        idle_diff = t1.idle - t0.idle

        # Calculate the difference in total time
        total_diff = (
            (t1.user - t0.user)
            + (t1.nice - t0.nice)
            + (t1.system - t0.system)
            + (t1.idle - t0.idle)
            + (t1.iowait - t0.iowait)
            + (t1.irq - t0.irq)
            + (t1.softirq - t0.softirq)
            + (t1.steal - t0.steal)
        )

        total_idle_diff += idle_diff
        total_time_diff += total_diff

    # Calculate the average CPU usage
    if total_time_diff > 0:
        average_usage = 100.0 * (1.0 - (total_idle_diff / total_time_diff))
    else:
        average_usage = 0.0

    return round(average_usage, 2)


class EC2TestCase:
    executime_time_ms = ""
    avg_cpu_usage_percent = ""
    max_memory_usage_mb = ""
    avg_memory_usage_mb = ""
    subprocess_input = []

    def __init__(
        self,
        architecture: str,
        language: str,
        start_type: StartType,
        iterations: int,
        instance_type: str,
        operation: str,
    ) -> None:

        self.architecture = architecture
        self.language = language
        self.start_type = start_type
        self.iterations = iterations
        self.instance_type = instance_type
        self.operation = operation

        # Get the base directory where the script is being executed
        base_dir = str(os.path.dirname(os.path.abspath(__file__)))
        new_file_base_str = (
            f"iac-microbenchmark/ec2/{language}/{architecture}/{operation}"
        )
        file_executable_location = base_dir.replace(
            "benchmarkrunner", new_file_base_str
        )

        # Mapping of language to command and file location format
        language_settings = {
            "c#": {"command": "", "file_loc": f"{file_executable_location}"},
            "go": {"command": "", "file_loc": f"{file_executable_location}"},
            "java": {
                "command": "java -jar",
                "file_loc": f"{file_executable_location}-1.0-SNAPSHOT.jar",
            },
            "python": {
                "command": "python3.11",
                "file_loc": f"{file_executable_location}.py",
            },
            "rust": {"command": "", "file_loc": f"{file_executable_location}"},
            "typescript": {
                "command": "node",
                "file_loc": f"{file_executable_location}.js",
            },
        }

        # Default values if language is unknown
        language_settings_default = {"command": "", "file_loc": ""}

        # Retrieve settings based on language, fallback to default if language is unknown
        settings = language_settings.get(language, language_settings_default)
        if settings["file_loc"] == "":
            print("ERROR WHEN BUILDING A TEST CASE, language settings default entered?")
            print("No File Location for executable?")
            print(f"Operation: {operation}")
            print(f"Language: {language}")
            # EXIT FAILURE STOP BENCHMARK
            exit(1)

    def export_results(self):
        print("")


def get_instance_type():
    try:
        # Querying the instance metadata service to get the instance type
        response = requests.get("http://169.254.169.254/latest/meta-data/instance-type")
        if response.status_code == 200:
            return response.text
        else:
            print(
                f"Unable to retrieve instance type. Status code: {response.status_code}"
            )
            exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error querying instance metadata: {e}")
        exit(1)


def get_testcase_input(file_name: str) -> Dict[str, str]:

    test_case_inputs = {}

    print("Reading Test Case Inputs.")

    return test_case_inputs


def main():

    # Get the architecture of the current machine.
    # Can be x86_64 or aarch64
    architecture = platform.machine()
    print(architecture)

    # Get the instance type
    # instance_type = get_instance_type()
    instance_type = "Test"

    # use comments to select specific test cases

    languages = [
        #'c#',
        "go",
        #'java',
        #'python',
        #'rust',
        #'typescript',
    ]

    operations = [
        "aes256_decrypt",  # works for all
        "aes256_encrypt",  # works for all
        "ecc256_sign",  # works for all
        "ecc256_verify",  # works for all
        "ecc384_sign",  # works for all
        "ecc384_verify",  # works for all
        "rsa2048_decrypt",  # works for all
        "rsa2048_encrypt",  # works for all
        "rsa3072_decrypt",  # works for all
        "rsa3072_encrypt",  # works for all
        "rsa4096_decrypt",  # works for all
        "rsa4096_encrypt",  # works for all
        "sha256",  # works for all
        "sha384",  # works for all
    ]

    # for cold_start
    start_options = ["cold", "warm"]

    # set the number of iterations for a test case.
    iterations = 1

    # Since we have multiple file sizes, we need to determine what files to read
    # Check TestArtifacts directory for the raw file inputs.
    # The file inputs raw strings latin letters a-zA-Z, 1kb, 100kb, 1mb, 10mb.
    # test_case_inputs = get_testcase_inputs()

    save_result_file_name = (
        f"./{architecture}-{instance_type}-AWSEC2-Benchmarkresults.csv"
    )

    print("Finished Initialization")

    print("")
    print("")

    print("Beginning AWS EC2 Benchmark Runnner")
    print(f"Architecture: {architecture}")
    print(f"Instance Type: {instance_type}")

    print("Finished AWS EC2 Benchmark Runner")

    # save_testcase_results(finished_test_cases, save_result_file_name)

    print(f"Saved benchmark results to file: {save_result_file_name}")

    exit(0)


if __name__ == "__main__":
    print("Begin Initialization of AWS EC2 Benchmark Runner.")
    main()
