FROM osrf/ros:humble-desktop-full

RUN apt-get update \
    && apt-get install -y \
    nano \
    vim \
    git \
    x11-apps \
    tmux \
    ros-humble-foxglove-bridge \
    ros-humble-moveit \
    ros-humble-moveit-visual-tools \
    ros-humble-moveit-ros-visualization \
    ros-humble-moveit-servo \
    ros-humble-joint-state-publisher-gui \
    ros-humble-rosbridge-suite \
    ros-humble-xacro \
    ros-humble-robot-state-publisher \
    ros-humble-teleop-twist-keyboard \
    ros-humble-teleop-twist-joy \
    ros-humble-joy \
    ros-humble-controller-manager \
    ros-humble-ros2-control \
    ros-humble-ros2-controllers \
    ros-humble-robot-state-publisher \
    ros-humble-joint-state-publisher \
    ros-humble-joint-trajectory-controller \
    ros-humble-joint-state-broadcaster \
    net-tools \
    && rm -rf /var/lib/apt/lists/

ARG USERNAME=ros
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && mkdir /home/$USERNAME/.config && chown $USER_UID:$USER_GID /home/$USERNAME/.config

EXPOSE 8765

# Set up sudo
RUN apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME\
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && rm -rf /var/lib/apt/lists/*

# Copy the entrypoint and bashrc scripts so we have 
# our container's environment set up correctly
COPY entrypoint.sh /entrypoint.sh
COPY bashrc /home/${USERNAME}/.bashrc

# Set up entrypoint and default command
ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
CMD ["bash"]