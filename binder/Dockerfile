FROM intel4coro/base-notebook:20.04-noetic-vnc

# Install VSCode server
USER root
RUN export VERSION=4.101.2 && \
    curl -fOL https://github.com/coder/code-server/releases/download/v$VERSION/code-server_${VERSION}_amd64.deb && \
    dpkg -i code-server_${VERSION}_amd64.deb && \
    rm code-server_${VERSION}_amd64.deb
USER ${NB_USER}

# Initiate workspace 
ENV PYCRAM_WS=/home/${NB_USER}/workspace/ros
WORKDIR ${PYCRAM_WS}/src/

# Copy everything to the ROS workspace
# COPY --chown=${NB_USER}:users . ${PYCRAM_WS}/src/pycram

# Can not use the pycram-https.rosinstall under the root directory, because some submodules are linked with SSH urls
RUN vcs import --input https://github.com/cram2/pycram/raw/refs/heads/dev/rosinstall/pycram-https.rosinstall
# Install python dependencies
WORKDIR ${PYCRAM_WS}/src/pycram
RUN pip install --requirement src/neem_interface_python/requirements.txt \
  && pip install --requirement requirements.txt

# Install ROS dependencies
WORKDIR  ${PYCRAM_WS}
USER root
RUN rosdep update --include-eol-distros && apt update && apt dist-upgrade -y \
  && rosdep install -y --ignore-src --from-paths ./ -r \
  && rosdep fix-permissions

# Build catkin workspace
USER ${NB_USER}
RUN catkin build

# JupyterLab UI configuration
WORKDIR ${PYCRAM_WS}/src/pycram
RUN git config --global --add safe.directory ${PWD}
COPY --chown=${NB_USER}:users binder/webapps.json ${PYCRAM_WS}/src/rvizweb/webapps/app.json

# Override container entrypoint
COPY --chown=${NB_USER}:users binder/entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]

COPY --chown=${NB_USER}:users binder/vscode.svg $HOME/
