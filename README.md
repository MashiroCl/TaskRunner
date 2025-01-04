# Task Runner
This Python script reads commands from a file and executes them concurrently using a process pool. It is designed for efficiently running multiple shell commands in parallel, taking advantage of multi-core processors to reduce execution time.

## Requirements
Python 3.7 or higher.


## Usage
Run the script from the command line with the required arguments.

### Command-line Arguments
- `-f`: The file path containing the list of commands to execute (required).
- `-p`: The maximum number of processes to run concurrently (optional, defaults to half the number of CPU cores).

### File Format
The commands file should contain one command per line. Example:
```bash
echo "Hello, World!"
ls -l
pwd
```
There is also an example file in [test_command.txt](./test_command.txt).

**Note:** It is not recommended to include `nohup` commands in the command file, as they may cause excessive CPU burden.

### Example
```bash
# as foreground process
$ python3 taskRunner.py -f test_command.txt
```
```bash
# as background process
$ nohup python3 taskRunner.py -f test_command.txt>run.log 2>&1 &
```

### Specify the Number of Processes
To run the script with a custom number of parallel processes by specifing the `-p` option:
```bash
$ python taskRunner.py -f test_command.txt -p 4
```