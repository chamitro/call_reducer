FROM ubuntu:20.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    libgmp-dev \
    libmpfr-dev \
    libmpc-dev \
    flex \
    bison \
    texinfo \
    && rm -rf /var/lib/apt/lists/*

# Download and extract GCC 4.8.2
WORKDIR /tmp
RUN wget https://ftp.gnu.org/gnu/gcc/gcc-4.8.2/gcc-4.8.2.tar.gz && \
    tar -xzf gcc-4.8.2.tar.gz && \
    rm gcc-4.8.2.tar.gz

# Build GCC 4.8.2
WORKDIR /tmp/gcc-4.8.2
RUN ./configure \
    --prefix=/usr/local/gcc-4.8.2 \
    --enable-languages=c,c++ \
    --disable-multilib \
    --disable-bootstrap && \
    make -j$(nproc) && \
    make install

# Clean up build files to reduce image size
RUN rm -rf /tmp/gcc-4.8.2

# Set up environment variables
ENV PATH="/usr/local/gcc-4.8.2/bin:${PATH}"
ENV LD_LIBRARY_PATH="/usr/local/gcc-4.8.2/lib64:${LD_LIBRARY_PATH}"

# Set working directory
WORKDIR /workspace

# Default command
CMD ["/bin/bash"]

