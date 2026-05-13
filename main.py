from __future__ import annotations

from mcp.server.fastmcp import FastMCP
import services.system_info_service as system_info
import validation as validation


mcp = FastMCP("system-info-mcp-server")



@mcp.tool(description=
          "This tool returns system information like CPU, RAM, Disk usage, etc.")
def system_info_tool():
    return system_info.get_system_info().to_dict()



@mcp.tool(description=
          "This tool checks for processes consuming excessive resources and suggests closing them.")
def resource_usage_tool():
    high_usage = system_info.check_high_resource_usage()
    safe_processes = validation.get_safe_to_terminate_process(high_usage)
    processes_dict = []

    for proc in safe_processes:
        processes_dict.append(proc.to_dict())

    return processes_dict



@mcp.tool(description=
    "Terminate a process after validation and user confirmation"
)
def terminate_process_tool(pid: int, confirmed: bool):

    if not confirmed:
        return {
            "success": False,
            "message": "User confirmation required",
            "pid": pid
        }
    return system_info.terminate_process_with_validation(pid)



@mcp.tool(
    description="Return the first 20 running processes in the system"
)
def list_processes_tool(number: int=30):

    processes = system_info.get_processes(number)

    return {
        "count": len(processes),
        "processes": [p.to_dict() for p in processes]
    }


if __name__ == "__main__":
    mcp.run()
