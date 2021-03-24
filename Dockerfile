FROM python:3.8

ARG USER_ID
ARG GROUP_ID

RUN addgroup --gid $GROUP_ID user
RUN adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID user

USER user

COPY ./requirements.txt /home/user/setup/

WORKDIR /home/user/setup
RUN pip install -r requirements.txt --trusted-host files.pythonhosted.org --trusted-host pypi.org

ENV PATH "$PATH:/home/user/.local/bin"
RUN mkdir /home/user/proj
WORKDIR /home/user/proj
