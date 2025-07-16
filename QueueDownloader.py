import json, subprocess, os, argparse

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="QueueDownloader - A tool for downloading queue automatically.")
    parser.add_argument("-v", "--version", action="store_true")
    parser.add_argument("-f", "--file", type=str, help="Set the queue file to use")
    parser.add_argument("-d", "--destination", type=str, help="Set the destination folder for downloads")
    parser.add_argument("-p", "--predefined", action="store_true", help="Use predefined destination and queue if not specified")
    parser.add_argument("-c", "--curl-args", type=str, help="Additional arguments for curl command")
    return parser.parse_args()


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def start_download():
    pass


def load_data(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        raise ValueError(f"File {file_path} is not a valid JSON file.")


def main():
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

    if not os.path.exists(destination):
        print(f"\033[33mCreating new folder: {destination}\033[0m")

    if not os.path.exists(queue_file):
        print(f"\033[31mQueue file does not exist at {queue_file}\033[0m")
        return

    if not queue_file.endswith(".json"):
        print(f"\033[31mQueue file is not a json file: {queue_file}\033[0m")
        return

    print(f"\033[35mDestination folder: {destination}\033[0m")
    print(f"\033[35mQueue file: {queue_file}\033[0m")

    start_download()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[31mProcess interrupted by user.\033[0m")
    except Exception as e:
        print(f"\n\033[31mAn error occurred: {e}\033[0m")