FROM ubuntu:16.04

RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    libgmp-dev \
    libmpfr-dev \
    libmpc-dev \
    flex \
    bison \
    gcc-multilib \
    g++-multilib \
    lib32gcc-4.8-dev \
    && rm -rf /var/lib/apt/lists/*

# Download and build GCC 4.9.0 with multilib support
RUN cd /tmp && \
    wget https://ftp.gnu.org/gnu/gcc/gcc-4.9.0/gcc-4.9.0.tar.gz && \
    tar xzf gcc-4.9.0.tar.gz && \
    cd gcc-4.9.0 && \
    ./configure --prefix=/usr/local/gcc-4.9.0 \
                --enable-languages=c,c++ \
                --enable-multilib \
                --disable-bootstrap && \
    make -j$(nproc) && \
    make install && \
    cd / && rm -rf /tmp/gcc-4.9.0*

# Create gcc-4.9.0 symlink
RUN ln -s /usr/local/gcc-4.9.0/bin/gcc /usr/local/bin/gcc-4.9.0

# Add to PATH
ENV PATH="/usr/local/gcc-4.9.0/bin:${PATH}"

WORKDIR /work