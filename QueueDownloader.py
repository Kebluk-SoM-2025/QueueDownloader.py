import json
import subprocess
import os
import argparse
from datetime import datetime

class QueueDownloader:
    def __init__(self, destination: str, queue_file: str, retry: bool, curl_args: list[str]) -> None:
        self.destination: str = destination
        self.queue_file: str = queue_file
        self.retry: bool = retry
        self.curl_args: list[str] = curl_args if curl_args else []
        self.queue: dict[str, str] = self.load_data()


    def load_data(self) -> dict[str, str] | None:
        try:
            with open(self.queue_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                if not data:
                    raise ValueError(f"Queue file {self.queue_file} is empty.")
                if not isinstance(data, dict):
                    raise ValueError(f"Queue file {self.queue_file} does not contain a valid dict of filenames and URLs.")
                return data
        except json.JSONDecodeError:
            raise ValueError(f"File {self.queue_file} is not a valid JSON file.")


    def download_file(self, filename: str, url: str, current_order: int, total_files: int) -> bool:
        file_path = os.path.join(self.destination, filename)

        # Create a destination directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        curl_command = ["curl", url, "-o", file_path, *self.curl_args]

        try:
            print(f"\033\n[1;34m[{time_now()}] [{current_order}/{total_files}] Downloading: {filename}\033[0m")
            subprocess.run(curl_command, check=True)
            print(f"\033[1;32m[{time_now()}] [{current_order}/{total_files}] Downloaded {filename}\033[0m")
            return True
        except subprocess.CalledProcessError as e:
            print(f"\033[1;31m[{time_now()}] [{current_order}/{total_files}] Failed to download {filename}: {e}\033[0m")
            return False


    def start_download(self) -> tuple[int, int, dict[str, str]]:
        total_files = len(self.queue)
        successful_downloads = 0
        unsuccessful_files = {}

        print(f"\033[1;36mStarting download from queue file: {self.queue_file}\033[0m")
        print(f"\033[1;36mDownloading {total_files} files.\033[0m")

        for filename, url in self.queue.items():
            current_order = successful_downloads + len(unsuccessful_files) + 1
            if self.download_file(filename, url, current_order, total_files):
                successful_downloads += 1
            else:
                unsuccessful_files[filename] = url


        print(f"\n\033[1;32mDownload completed!\033[0m")
        print(f"\033[1;36mSuccessfully downloaded {successful_downloads}/{total_files} files.\033[0m")

        if successful_downloads:
            print(f"\033[1;33mFound {len(unsuccessful_files)} unsuccessful files:\033[0m")
            for file in unsuccessful_files:
                print(f"\t\033[33m- {file}\033[0m")

            if self.retry:
                print("\033[36mRetrying failed downloads...\033[0m")

                self.retry = False
                self.queue = unsuccessful_files
                retry_success, retry_total, retry_failed = self.start_download()

                successful_downloads += retry_success
                unsuccessful_files = retry_failed

        return successful_downloads, total_files, unsuccessful_files


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="QueueDownloader - A tool for downloading queue automatically.")
    parser.add_argument("-v", "--version", action="store_true")
    parser.add_argument("-f", "--file", type=str, help="Set the queue file to use")
    parser.add_argument("-d", "--destination", type=str, help="Set the destination folder for downloads")
    parser.add_argument("-p", "--predefined", action="store_true", help="Use predefined destination and queue if not specified")
    parser.add_argument("-r", "--retry", action="store_true", help="Retry downloading files that failed previously")
    parser.add_argument("-c", "--curl-args", type=str, help="Additional arguments for curl command")
    return parser.parse_args()


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")

def time_now() -> str:
    return datetime.now().strftime("%H:%M:%S")


def main() -> None:
    args = parse_args()

    if args.version:
        print("\033[36mQueueDownloader version \033[32m1.0.0\033[0m")
        return

    clear_screen()

    print(f"\033[1;36mWelcome to QueueDownloader.py!\033[0m\n")

    destination = "./downloads"
    queue_file = "queue.json"

    if args.destination:
        destination = args.destination
    elif not args.predefined:
        destination = input(f"Enter destination folder [{destination}]: ") or destination

    if args.file:
        queue_file = args.file
    elif not args.predefined:
        queue_file = input(f"Enter path to the queue file [{queue_file}]: ") or queue_file

    destination = os.path.abspath(os.path.expanduser(destination))
    queue_file = os.path.abspath(os.path.expanduser(queue_file))

    if not os.path.exists(queue_file):
        print(f"\033[31mQueue file does not exist at {queue_file}\033[0m")
        return

    if not queue_file.endswith(".json"):
        print(f"\033[31mQueue file is not a json file: {queue_file}\033[0m")
        return

    print(f"\n\033[35mDestination folder: {destination}\033[0m")
    print(f"\033[35mQueue file: {queue_file}\033[0m\n")

    curl_args = args.curl_args.split() if args.curl_args else []

    downloader = QueueDownloader(destination, queue_file, args.retry, curl_args)
    downloader.start_download()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[31mProcess interrupted by user.\033[0m")
    except Exception as e:
        print(f"\n\033[31mAn error occurred: {e}\033[0m")