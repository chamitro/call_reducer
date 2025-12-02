FROM ubuntu:14.04 AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    python \
    wget \
    subversion \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set up build directory
WORKDIR /work

# Download LLVM 3.6.0
RUN wget https://releases.llvm.org/3.6.0/llvm-3.6.0.src.tar.xz && \
    tar xf llvm-3.6.0.src.tar.xz && \
    mv llvm-3.6.0.src llvm

# Download Clang 3.6.0
RUN wget https://releases.llvm.org/3.6.0/cfe-3.6.0.src.tar.xz && \
    tar xf cfe-3.6.0.src.tar.xz && \
    mv cfe-3.6.0.src llvm/tools/clang

# Download Compiler-RT 3.6.0
RUN wget https://releases.llvm.org/3.6.0/compiler-rt-3.6.0.src.tar.xz && \
    tar xf compiler-rt-3.6.0.src.tar.xz && \
    mv compiler-rt-3.6.0.src llvm/projects/compiler-rt

# Create build directory and configure
RUN mkdir llvm-build && cd llvm-build && \
    cmake -DCMAKE_BUILD_TYPE=Release \
          -DCMAKE_INSTALL_PREFIX=/usr/local \
          -DLLVM_TARGETS_TO_BUILD=X86 \
          ../llvm

# Build (this will take a while)
RUN cd llvm-build && make -j$(nproc)

# Install
RUN cd llvm-build && make install

# Final stage - smaller runtime image
FROM ubuntu:14.04

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libstdc++6 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed binaries from builder
COPY --from=builder /usr/local /usr/local

# Set up environment
ENV PATH="/usr/local/bin:${PATH}"
ENV LD_LIBRARY_PATH="/usr/local/lib:${LD_LIBRARY_PATH}"

# Verify installation
RUN clang --version

WORKDIR /workspace

CMD ["/bin/bash"]

