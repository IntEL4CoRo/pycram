# This file is to setup the visualization tools for pycram notebooks.
# Will be run automatically when opening a notebook on BinderHub.

import os
from IPython.display import display, HTML
from sidecar import Sidecar
import subprocess
import threading
from time import sleep
from IPython import get_ipython
from pycram.datastructures.enums import WorldMode
from pycram.ros_utils.viz_marker_publisher import VizMarkerPublisher

# Display remote desktop on sidecar tab
def display_desktop():
    try:
        JUPYTERHUB_USER = os.environ['JUPYTERHUB_USER']
    except KeyError:
        JUPYTERHUB_USER = None
    url_prefix = f"/user/{JUPYTERHUB_USER}" if JUPYTERHUB_USER is not None else ''
    remote_desktop_url = f"{url_prefix}/desktop"
    sc = Sidecar(title='Desktop', anchor="split-right")
    with sc:
        # The inserted custom HTML and CSS snippets are to make the tab resizable
        display(HTML(f"""
            <style>
            body.p-mod-override-cursor div.iframe-widget {{
                position: relative;
                pointer-events: none;

            }}

            body.p-mod-override-cursor div.iframe-widget:before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: transparent;
            }}
            </style>
            <div class="iframe-widget" style="width: calc(100% + 10px);height:100%;">
                <iframe src="{remote_desktop_url}" width="100%" height="100%"></iframe>
            </div>
        """))

# Run bash command in the background
def run_background_command(cmd):
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setpgrp
    )
    # print(f"Started process with PID {process.pid}")
    process.wait()

# Run rivz2 in the background
def launch_rviz(config='pycram.rviz'):
    try:
        subprocess.run(["killall", "rviz2"], check=False)
    except Exception as e:
        pass
    thread = threading.Thread(target=run_background_command, kwargs={
        "cmd":["rviz2", "-d", config]
    }, daemon=True)
    thread.start()

# Init visualization tools when running notebook on binderhub
def _init_visual_tools(result):
    if result.error_in_exec is not None:
        return
    if "BulletWorld" in result.info.raw_cell and world is not None:
        display_desktop()
        sleep(3)
        if world.mode == WorldMode.DIRECT:
            viz_marker_publisher = VizMarkerPublisher()
            launch_rviz()
        ip.events.unregister('post_run_cell', _init_visual_tools)

ip = get_ipython()
if ip:
    ip.events.register('post_run_cell', _init_visual_tools)