import maya.cmds as mc
import functools

def on_delete(ls_script_jobs = [], node= None, method = None):
    print(f"NODE : {node}")
    ls_script_jobs.append(mc.scriptJob(nodeDeleted=(node, method)))
    return ls_script_jobs

def create_script_jobs(events = {}, ls_script_jobs = []):
    for key in events.keys():
        event = events[key]["event"]
        method = events[key]["method"]
        ls_script_jobs.append(mc.scriptJob(event = [f"{event}", functools.partial(method)]))
    print(f"##########   Script Jobs {ls_script_jobs}\n")
    return ls_script_jobs


def delete_script_jobs(ls_script_jobs):
    for job_num in ls_script_jobs:
        mc.scriptJob(kill=job_num)
        print(f"Script killed ---> {job_num}")