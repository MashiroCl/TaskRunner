import concurrent.futures
import subprocess
import argparse
import os


def run_command(command):
    """Executes a command in the shell."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stderr


def main(commands_file, max_workers):
    """Reads commands from a file and executes them in a process pool."""
    # Read commands from the file
    with open(commands_file, "r") as file:
        commands = [line.strip() for line in file.readlines() if line.strip()]
    # Use a process pool to execute commands concurrently
    with concurrent.futures.ProcessPoolExecutor(
        max_workers=min(max_workers, os.cpu_count())
    ) as executor:
        future_to_command = {executor.submit(run_command, cmd): cmd for cmd in commands}

        for future in concurrent.futures.as_completed(future_to_command):
            command = future_to_command[future]
            try:
                result = future.result()
                print(f"Command: '{command}' executed successfully.")
                print(f"Result: {result}")
            except Exception as exc:
                print(f"Command: '{command}' generated an exception: {exc}")


if __name__ == "__main__":
    # Create the parser and add the argument
    parser = argparse.ArgumentParser(
        description="Execute commands from a file in a process pool."
    )
    parser.add_argument(
        "-f", type=str, help="The file path containing commands to execute."
    )
    parser.add_argument(
        "-p",
        type=int,
        default=os.cpu_count() // 2,
        help="The number of processes allowed to run concurrently, default value is half number of the cpu cores.",
    )

    # Parse the command line arguments
    args = parser.parse_args()

    # Call the main function with the commands file argument
    main(args.f, args.p)
