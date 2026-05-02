FROM ubuntu:18.04 AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    python \
    wget \
    xz-utils \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Set up build directory
WORKDIR /build

# Download LLVM 7.1.0
RUN wget https://github.com/llvm/llvm-project/releases/download/llvmorg-7.1.0/llvm-7.1.0.src.tar.xz && \
    tar xf llvm-7.1.0.src.tar.xz && \
    mv llvm-7.1.0.src llvm

# Download Clang 7.1.0
RUN wget https://github.com/llvm/llvm-project/releases/download/llvmorg-7.1.0/cfe-7.1.0.src.tar.xz && \
    tar xf cfe-7.1.0.src.tar.xz && \
    mv cfe-7.1.0.src llvm/tools/clang

# Download Compiler-RT 7.1.0
RUN wget https://github.com/llvm/llvm-project/releases/download/llvmorg-7.1.0/compiler-rt-7.1.0.src.tar.xz && \
    tar xf compiler-rt-7.1.0.src.tar.xz && \
    mv compiler-rt-7.1.0.src llvm/projects/compiler-rt

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
FROM ubuntu:18.04

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libstdc++6 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed binaries from builder
COPY --from=builder /usr/local /usr/local

# Set up environment
ENV PATH="/usr/local/bin:${PATH}"
ENV LD_LIBRARY_PATH="/usr/local/lib:${LD_LIBRARY_PATH}"

# Create /work directory to match the mount point
WORKDIR /work

# Verify installation
RUN clang --version

# Set clang as default entrypoint
ENTRYPOINT ["clang"]

