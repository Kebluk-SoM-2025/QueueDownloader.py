# QueueDownloader.py

QueueDownloader.py is a Python script that downloads files specified in a JSON file using the `curl` command-line tool.
The JSON file contains a dictionary mapping filenames to URLs, as shown below:

```json
{
  "example.txt": "https://example.com/file.txt",
  "document.pdf": "https://example.com/doc.pdf"
}
```

The script processes each file in the queue, downloads it using `curl`, skips failed downloads with error logging, and
reports a success rate upon completion. Users can customize `curl` arguments (except the output path) to control
download behavior, such as ignoring HTTPS verification or enabling verbose output.

## Features

- Reads a JSON file with a dictionary of filenames and their URLs.
- Downloads files using the `curl` command-line tool.
- Creates the destination folder if it doesn’t exist.
- Skips failed downloads, logs errors to the console, and continues processing.
- Reports the success rate (e.g., "80% (4/5 files downloaded successfully)").
- Supports custom `curl` arguments (e.g., `--insecure --verbose`) via the `--curl-args` option.
- Uses colored terminal output for better readability.
- Handles keyboard interrupts gracefully.

## Requirements

- Python 3.10 or higher.
- `curl` command-line tool installed and accessible in the system PATH (on Windows, `curl.exe` expected).
- Standard Python libraries: `json`, `subprocess`, `os`, `argparse` (included with Python).

## Installation

The script requires Python and `curl` to be installed:

1. Install Python 3.10 or higher from [Python.org](https://www.python.org/).
2. Install `curl`:
    - **Windows**: Use the built-in `curl.exe`, or download from [curl.se](https://curl.se) or via Chocolatey (
      `choco install curl`).
    - **Linux**: Install via package manager (e.g., `sudo apt install curl` on Debian/Ubuntu, `sudo dnf install curl` on
      Fedora).
    - **macOS**: Use the system-provided `curl` or install via Homebrew (`brew install curl`).
3. Verify `curl` is accessible by running `curl --version` (or `curl.exe --version` on Windows).

## Usage

Run the script from the command line, specifying the JSON queue file and destination folder:

```bash
python QueueDownloader.py -f queue.json -d ./downloads
```

### Command-Line Arguments

- `-h`, `--help` Show the help message and exit.
- `-v`, `--version` Show the script version (1.0.0) and exit.
- `-f`, `--file` Path to the JSON queue file (default: `queue.json`).
- `-d`, `--destination` Directory to save downloaded files (default: `./downloads`).
- `-p`, `--predefined` Use a default queue file and destination without interactive prompts.
- `-c `, `--curl-args` Additional `curl` arguments (e.g., `--insecure --verbose`).

### Example

```bash
python QueueDownloader.py -f queue.json -d downloads -c "--insecure --verbose"
```

If run without `-p`, the script prompts for the queue file and destination folder, defaulting to `queue.json` and `
./downloads`.

## JSON File Format

The JSON file must contain a dictionary where keys are filenames and values are URLs:

```json
{
  "example.txt": "https://example.com/file.txt",
  "document.pdf": "https://example.com/doc.pdf"
}
```

## Output

- Files are saved to the specified destination folder.
- Failed downloads are logged to the console with error details.
- A success rate is printed at the end (e.g., "80% (4/5 files downloaded successfully)").
- Output is color-coded: blue for status, green for success, red for errors.

## License

Licensed under the GNU General Public License v3.0. See [LICENSE](LICENSE.txt)
or [gnu.org/licenses/gpl-3.0.txt](https://www.gnu.org/licenses/gpl-3.0.txt).

### Dependencies

- Python standard libraries (`json`, `subprocess`, `os` , `argparse`): Licensed under
  the [Python Software Foundation License](https://docs.python.org/3/license.html), compatible with GPL v3.0.
- `curl`: Licensed under the [curl License](https://curl.se/docs/copyright.html) (MIT-like), compatible with GPL v3.0.
  Must be installed separately.
