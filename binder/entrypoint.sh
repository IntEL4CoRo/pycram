#!/bin/bash

source ${PYCRAM_WS}/devel/setup.bash
roscore &
roslaunch --wait rvizweb rvizweb.launch &
roslaunch --wait pycram ik_and_description.launch &

# Config Vscode in launcher
if [[ -n "$JUPYTERHUB_CLIENT_ID" ]]; then
    VS_BASE_PATH="/user/$JUPYTERHUB_CLIENT_ID"
else
    VS_BASE_PATH=""
fi
echo "
c.ServerProxy.servers = {
    'code': {
        'command': ['code-server',
                    '--auth=none', 
                    '--abs-proxy-base-path=$VS_BASE_PATH/code',
                    '--disable-workspace-trust',
                    ],
        'timeout': 20,
        'port': 8080,
        'launch_url': '/code/?folder=$PWD',
        'launcher_entry': {
            'title': 'Visual Studio Code',
            'icon_path': '$HOME/vscode.svg',
        },
        'new_browser_tab': True
    }
}
" >> ~/.jupyter/jupyter_notebook_config.py


exec "$@"