import psutil


def get_whitelist():
    whitelist = []
    with open("exe_files.txt", "r") as file:
        for line in file:
            # Remove leading/trailing whitespaces and add the line to the whitelist
            whitelist.append(line.strip())
    return whitelist


def is_uncommon_exe(process_id, whitelist):
    return process_id.endswith(".exe") and process_id not in whitelist


def get_process_by_name(process_id):
    for value in psutil.process_iter(['pid', 'name']):
        if value.info['name'] == process_id:
            return value


def kill_process(process):
    try:
        process.terminate()
        print(f"Process '{process.info['name']}' (PID: {process.info['pid']}) has been terminated.")
    except psutil.NoSuchProcess:
        print("Process not found.")
    except psutil.AccessDenied:
        print("Access denied. You may not have permission to terminate this process.")


if __name__ == "__main__":
    list_of_processes = get_whitelist()
    print("Scanning for uncommon .exe files running on your machine...")

    uncommon_processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        process_name = proc.info['name']
        if is_uncommon_exe(process_name, list_of_processes):
            uncommon_processes.append(process_name)

    if uncommon_processes:
        print("Uncommon .exe files detected:")
        for process in uncommon_processes:
            print(process)

        print("Do you want to terminate any of these processes? (y/n)")
        confirm = input()
        if confirm.lower() == 'y':
            print("Enter the name of the process you want to terminate:")
            target_process_name = input()
            process_to_kill = get_process_by_name(target_process_name)
            if process_to_kill:
                print(f"Are you sure you want to terminate '{target_process_name}'? (y/n)")
                confirm_kill = input()
                if confirm_kill.lower() == 'y':
                    kill_process(process_to_kill)
                else:
                    print("Process termination canceled.")
            else:
                print(f"No process with the name '{target_process_name}' found.")
        else:
            print("No processes terminated.")
    else:
        print("No uncommon .exe files detected.")
