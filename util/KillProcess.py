import psutil


def process_kill(process_list):
    for proc in psutil.process_iter():
        process = psutil.Process(proc.pid)
        pname = process.name()
        for process_name in process_list:
            if process_name in pname:
                print("Yes")
                process.terminate()
            else:
                pass
