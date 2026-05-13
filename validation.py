import os

import psutil

from models.process_info import ProcessInfo



CRITICAL_WINDOWS = {
    "system",
    "svchost.exe",
    "wininit.exe",
    "winlogon.exe",
    "csrss.exe",
    "services.exe",
}

CRITICAL_LINUX = {
    "systemd",
    "init",
}

def is_process_safe_to_terminate(process_info: ProcessInfo) -> bool:
    try:
        # Zombie processes are always safe
        if process_info.status == psutil.STATUS_ZOMBIE:
            return True

        name = (process_info.name or "").lower()

        # Never kill PID 0/1
        if process_info.pid in (0, 1):
            return False

        # Never kill ourselves
        if process_info.pid == os.getpid():
            return False

        # Windows critical processes
        if name in CRITICAL_WINDOWS:
            return False

        # Linux critical processes
        if name in CRITICAL_LINUX:
            return False

        return True

    except AttributeError:
        return False

    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return False


def get_safe_to_terminate_process(processes):
   safe_to_terminate_process = []
   for proc in processes:
       if is_process_safe_to_terminate(proc):
           safe_to_terminate_process.append(proc)
   return safe_to_terminate_process


def user_confirmed(action: str, confirmed: bool) -> bool:
    if not confirmed:
        raise ValueError(
            f"User confirmation required before performing: {action}"
        )
    return True