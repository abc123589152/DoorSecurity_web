# 使用一个基础的 Linux 镜像，例如 Debian 或 Ubuntu
FROM ubuntu:latest

# 更新包列表并安装 NTP 服务
RUN apt-get update && \
    apt-get install -y ntp

# 复制 NTP 配置文件（如果需要自定义配置）
COPY ntp.conf /etc/ntp.conf

# 暴露 NTP 默认端口
EXPOSE 123/udp

# 启动 NTP 服务
CMD ["/bin/bash"]

