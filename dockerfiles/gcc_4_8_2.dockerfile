FROM ubuntu:14.04

# Prevent interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive

# Install build dependencies including 32-bit support
RUN dpkg --add-architecture i386 && \
    apt-get update && apt-get install -y \
    build-essential \
    wget \
    libgmp-dev \
    libmpfr-dev \
    libmpc-dev \
    flex \
    bison \
    texinfo \
    gcc-multilib \
    g++-multilib \
    libc6-dev-i386 \
    lib32gcc-4.8-dev \
    && rm -rf /var/lib/apt/lists/*

# Download and extract GCC 4.8.2
WORKDIR /usr/src
RUN wget https://ftp.gnu.org/gnu/gcc/gcc-4.8.2/gcc-4.8.2.tar.gz && \
    tar -xzf gcc-4.8.2.tar.gz && \
    rm gcc-4.8.2.tar.gz

# Build GCC in a separate directory (recommended)
WORKDIR /usr/src/gcc-build
RUN /usr/src/gcc-4.8.2/configure \
    --prefix=/usr/local/gcc-4.8.2 \
    --enable-languages=c,c++ \
    --enable-multilib \
    --disable-bootstrap && \
    make -j$(nproc) && \
    make install

# Add GCC to PATH
ENV PATH="/usr/local/gcc-4.8.2/bin:${PATH}"
ENV LD_LIBRARY_PATH="/usr/local/gcc-4.8.2/lib64:/usr/local/gcc-4.8.2/lib:${LD_LIBRARY_PATH}"

# Set working directory
WORKDIR /workspace

# Default command
CMD ["/bin/bash"]