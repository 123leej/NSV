import psutil


def kill_process(process_name):
    for proc in psutil.process_iter():
        process = psutil.Process(proc.pid)
        pname = process.name()
        if process_name in pname:
            process.terminate()
        else:
            pass
    return True
