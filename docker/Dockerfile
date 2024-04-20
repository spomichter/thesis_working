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
    iputils-ping \
    net-tools \
    python3-pip \
    ros-humble-robot-state-publisher \
    ros-humble-moveit \
    ros-humble-rosbridge-suite \
    ros-humble-joy \
    ros-humble-ros2-control \
    ros-humble-ros2-controllers \
    ros-humble-tf* \
    ros-humble-gazebo-ros-pkgs \
    ros-humble-joint-state-publisher \
    dos2unix \
    git \
    python3-pip \
    python3-genmsg \
    && rm -rf /var/lib/apt/lists/

RUN pip3 install rospkg numpy==1.24.0 jsonpickle scipy easydict matplotlib opencv-python opencv-python-headless pyyaml pyquaternion pybullet
RUN pip3 install tensorflow keras pybullet
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

ARG USERNAME=ros

ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && mkdir /home/$USERNAME/.config && chown $USER_UID:$USER_GID /home/$USERNAME/.config

EXPOSE 8765
EXPOSE 10000

# Set up sudo
RUN apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME\
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/$USERNAME/dev_ws/src && chown -R $USER_UID:$USER_GID /home/$USERNAME/dev_ws
RUN cd /home/$USERNAME/dev_ws/src && git clone https://github.com/yashas-salankimatt/thesis_ros_ws.git
RUN cd /home/$USERNAME/dev_ws

# Copy the entrypoint and bashrc scripts so we have 
# our container's environment set up correctly
COPY entrypoint.sh /entrypoint.sh
COPY bashrc /home/${USERNAME}/.bashrc
COPY .tmux.conf /home/${USERNAME}/.tmux.conf

RUN /bin/bash -c "source /opt/ros/humble/setup.bash && cd /home/$USERNAME/dev_ws && colcon build"

# Set up entrypoint and default command
ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
CMD ["bash"]