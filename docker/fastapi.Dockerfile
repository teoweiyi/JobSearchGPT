FROM nvidia/cuda:11.3.0-cudnn8-devel-ubuntu18.04

SHELL ["/bin/bash", "-c"]

ARG REPO_DIR="."
ARG CONDA_ENV_FILE="jobsearchgpt-conda-env.yaml"
ARG CONDA_ENV_NAME="jobsearchgpt"
ARG PROJECT_USER="jobsearchgptuser"
ARG HOME_DIR="/home/$PROJECT_USER"

ARG CONDA_HOME="/miniconda3"
ARG CONDA_BIN="$CONDA_HOME/bin/conda"
ARG MINI_CONDA_SH="Miniconda3-latest-Linux-x86_64.sh"

WORKDIR $HOME_DIR

RUN groupadd -g 1001 $PROJECT_USER && useradd -u 1001 -g 1001 -m $PROJECT_USER

RUN touch "$HOME_DIR/.bashrc"

RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub

RUN apt-get update && \
    apt-get -y install bzip2 curl wget gcc rsync git vim locales \
    apt-transport-https ca-certificates gnupg && \
    sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8 && \
    apt-get clean

COPY $REPO_DIR jobsearchgpt

RUN mkdir $CONDA_HOME && chown -R 1001:1001 $CONDA_HOME
RUN chown -R 1001:1001 $HOME_DIR && \
    rm /bin/sh && ln -s /bin/bash /bin/sh

ENV PYTHONIOENCODING utf8
ENV LANG "C.UTF-8"
ENV LC_ALL "C.UTF-8"
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV LD_LIBRARY_PATH /usr/local/cuda/lib64:$LD_LIBRARY_PATH

USER 1001

# Install Miniconda
RUN curl -O https://repo.anaconda.com/miniconda/$MINI_CONDA_SH && \
    chmod +x $MINI_CONDA_SH && \
    ./$MINI_CONDA_SH -u -b -p $CONDA_HOME && \
    rm $MINI_CONDA_SH
ENV PATH $CONDA_HOME/bin:$HOME_DIR/.local/bin:$PATH
# Install conda environment
RUN $CONDA_BIN env create -f jobsearchgpt/$CONDA_ENV_FILE && \
    $CONDA_BIN init bash && \
    $CONDA_BIN clean -a -y && \
    echo "source activate $CONDA_ENV_NAME" >> "$HOME_DIR/.bashrc"

EXPOSE 8080

WORKDIR $HOME_DIR/jobsearchgpt
RUN chmod -R +x scripts

ENTRYPOINT [ "/bin/bash", "./scripts/api-entrypoint.sh" ]