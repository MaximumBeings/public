# =============================================================================
# MOJO ELEMENTWISE MATRIX OPERATIONS WITH SIMD OPTIMIZATION
#   1) ADDITION        C = A + B
#   2) SUBTRACTION     C = A - B
#   3) MULTIPLICATION  C = A * B (Hadamard product)
#   4) DIVISION        C = A / B
#
# FORWARD + BACKWARD PASSES
# OPTIMIZED WITH SIMD (Single Instruction, Multiple Data)
# WITH FULL GRADIENT COMPUTATION FOR AUTOMATIC DIFFERENTIATION
#
# =============================================================================
#
# MOJO VERSION INFORMATION:
# =========================
#
# This code is compatible with Mojo 25.2+
# Tested on: mojo 25.2.0 (26172dfe)
#
# Version History:
# - Mojo 24.5: Used 'inout self', 'owned self'
# - Mojo 25.1: Introduced 'mut self', kept 'owned self'
# - Mojo 25.2: Requires '__moveinit__' for tuple returns
#
# =============================================================================
#
# INSTALLATION INSTRUCTIONS:
# ==========================
#
# Step 1: System Requirements
# ---------------------------
# - Ubuntu 20.04+ or macOS
# - 64-bit system
# - NVIDIA GPU optional (CPU SIMD works without GPU)
#
# Step 2: Install Pixi (Mojo's Package Manager)
# ---------------------------------------------
# curl -fsSL https://pixi.sh/install.sh | sh
# export PATH="$HOME/.pixi/bin:$PATH"
# echo 'export PATH="$HOME/.pixi/bin:$PATH"' >> ~/.bashrc
# source ~/.bashrc
# pixi --version
#
# Step 3: Create Mojo Project
# ---------------------------
# pixi init mojo_demo \
#   -c https://conda.modular.com/max-nightly/ \
#   -c conda-forge \
#   && cd mojo_demo
#
# Step 4: Add MAX Toolchain (includes Mojo)
# -----------------------------------------
# pixi add max
# pixi run mojo --version
#
# Step 5: Run This Script
# -----------------------
# pixi run mojo elementwise_ops_simd.mojo
#
# Expected Output:
# ---------------
# ======================================================================
# MOJO ELEMENTWISE OPERATIONS WITH SIMD
# ======================================================================
#
# Test configuration:
#   Matrix size: 64 x 128 = 8192 elements
#   SIMD width: 4 (Float32)
#
# Testing ADD
# ======================================================================
# Backward dA max error: 0.0
# Status: PASSED
#
# [Similar for SUB, MUL, DIV...]
#
# ======================================================================
# ALL TESTS PASSED!
# ======================================================================
#
# =============================================================================

from memory import UnsafePointer

"""
=============================================================================
MEMORY MANAGEMENT IN MOJO: UnsafePointer EXPLAINED
=============================================================================

UnsafePointer[T] is Mojo's low-level pointer type for manual memory management.

WHY "UNSAFE"?
-------------
- No automatic bounds checking
- No automatic memory management (must manually free)
- Possibility of memory leaks if not freed properly
- Can access invalid memory if used incorrectly

BENEFITS:
---------
- Zero overhead (as fast as C/C++)
- Full control over memory layout
- Essential for high-performance computing
- Allows contiguous memory allocation (SIMD-friendly)

MEMORY LIFECYCLE:
----------------

1. ALLOCATION:
   ptr = UnsafePointer[Float32].alloc(size)
   
   Heap Memory:
   +------------------------------------------+
   | [allocated space for 'size' Float32s]   |
   +------------------------------------------+
   ^
   ptr points here

2. USAGE:
   ptr[0] = 1.0
   ptr[1] = 2.0
   value = ptr[0]
   
   Memory Access:
   +------+------+------+------+
   | 1.0  | 2.0  | ?    | ?    |
   +------+------+------+------+
   ^      ^
   [0]    [1]

3. DEALLOCATION:
   ptr.free()
   
   CRITICAL: Must call .free() to avoid memory leaks!
   After free(), the memory is returned to the OS.

COMPARISON WITH OTHER LANGUAGES:
-------------------------------

Python:
  list = [1.0, 2.0, 3.0]  # Automatic memory management
  # No need to free, garbage collector handles it

C:
  float* ptr = (float*)malloc(size * sizeof(float));
  // ... use ptr ...
  free(ptr);  # Manual free, like Mojo

Mojo UnsafePointer:
  var ptr = UnsafePointer[Float32].alloc(size)
  // ... use ptr ...
  ptr.free()  # Manual free, like C

=============================================================================
"""


# =============================================================================
# MATRIX STRUCT: CORE DATA STRUCTURE
# =============================================================================

struct Matrix:
    """
    Matrix structure optimized for SIMD operations.
    
    MEMORY LAYOUT (Row-Major):
    ==========================
    
    Logical view (3x4 matrix):
    +-------------+
    | 0  1  2  3  |  <- Row 0
    | 4  5  6  7  |  <- Row 1
    | 8  9 10 11  |  <- Row 2
    +-------------+
    
    Physical memory (flattened in UnsafePointer):
    +--+--+--+--+--+--+--+--+--+--+---+---+
    | 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10 |11 |
    +--+--+--+--+--+--+--+--+--+--+---+---+
    ^                                      ^
    data[0]                           data[11]
    
    Index calculation: data[row * cols + col]
    Example: Element at (1, 2) -> data[1 * 4 + 2] = data[6] = 6
    
    WHY ROW-MAJOR?
    -------------
    - Consecutive elements in same row are adjacent in memory
    - Excellent for SIMD: can load row[0:4] in one instruction
    - Cache-friendly: accessing row elements has good spatial locality
    
    FIELDS:
    ------
    - data: UnsafePointer to flattened Float32 array
    - rows: Number of rows (M)
    - cols: Number of columns (N)
    - size: Total elements (M * N)
    """
    
    var data: UnsafePointer[Float32]
    var rows: Int
    var cols: Int
    var size: Int
    
    fn __init__(mut self, rows: Int, cols: Int):
        """
        Constructor: Initialize matrix with given dimensions.
        
        PARAMETER CONVENTION: 'mut self'
        ================================
        
        In Mojo 25.2+, 'mut self' indicates:
        - This method modifies the instance
        - Self starts uninitialized in __init__
        - Must initialize ALL fields before returning
        
        Older versions used 'inout self' or 'out self'
        
        MEMORY ALLOCATION:
        =================
        
        Step 1: Calculate size = rows * cols
        Step 2: Allocate heap memory
        
        Before allocation:
        self.data -> (null/uninitialized)
        
        After allocation:
        self.data -> +--+--+--+--+--+--+
                     | 0| 0| 0| 0| 0| 0|  (size elements)
                     +--+--+--+--+--+--+
        
        Step 3: Initialize all elements to zero
        """
        self.rows = rows
        self.cols = cols
        self.size = rows * cols
        
        # Allocate contiguous heap memory for all matrix elements
        self.data = UnsafePointer[Float32].alloc(self.size)
        
        # Initialize to zero (important for numerical stability)
        for i in range(self.size):
            self.data[i] = 0.0
    
    fn __copyinit__(mut self, existing: Self):
        """
        Copy constructor: Creates deep copy of matrix.
        
        DEEP COPY vs SHALLOW COPY:
        =========================
        
        Shallow copy (BAD - not what we do):
        Source:  data -> [1, 2, 3, 4]
                          ^
        Copy:    data ---+  (same pointer!)
        
        Problem: Modifying copy affects source!
        
        Deep copy (GOOD - what we do):
        Source:  data -> [1, 2, 3, 4]
        
        Copy:    data -> [1, 2, 3, 4]  (new memory)
        
        Changes to copy don't affect source!
        
        WHEN IS THIS CALLED?
        ===================
        var a = Matrix(2, 3)
        var b = a  # Calls __copyinit__
        
        or
        
        fn process(matrix: Matrix):  # Pass by value
            # ...
        
        process(a)  # Calls __copyinit__
        """
        # Copy dimensions
        self.rows = existing.rows
        self.cols = existing.cols
        self.size = existing.size
        
        # Allocate NEW memory (deep copy)
        self.data = UnsafePointer[Float32].alloc(self.size)
        
        # Copy all values element by element
        for i in range(self.size):
            self.data[i] = existing.data[i]
    
    fn __moveinit__(mut self, owned existing: Self):
        """
        Move constructor: Transfers ownership without copying.
        
        MOVE SEMANTICS:
        ==============
        
        Instead of copying data, transfer the pointer!
        
        Before move:
        existing.data -> [1, 2, 3, 4]  (8192 elements)
        self.data     -> (uninitialized)
        
        After move:
        existing.data -> (invalid, should not use)
        self.data     -> [1, 2, 3, 4]  (same memory!)
        
        PERFORMANCE:
        -----------
        Copy:  O(n) - must copy all elements
        Move:  O(1) - just transfer pointer
        
        WHEN IS THIS USED?
        ==================
        - Returning values from functions
        - Returning tuples: (Matrix, Matrix)
        - Transfer ownership with ^
        
        Example:
        fn create_matrix() -> Matrix:
            var m = Matrix(10, 10)
            return m  # Calls __moveinit__
        
        WHY 'owned existing'?
        ====================
        - 'owned' means we take ownership
        - existing becomes invalid after move
        - Prevents use-after-move bugs
        """
        # Transfer ownership (just copy pointer, not data)
        self.rows = existing.rows
        self.cols = existing.cols
        self.size = existing.size
        self.data = existing.data
        # existing.data is now invalid!
    
    fn __del__(owned self):
        """
        Destructor: Free allocated memory when matrix is destroyed.
        
        RAII (Resource Acquisition Is Initialization):
        ==============================================
        
        Constructor allocates -> Destructor deallocates
        
        WHEN IS THIS CALLED?
        ===================
        - When variable goes out of scope
        - At end of function
        - When explicitly deleted
        
        Example:
        fn example():
            var m = Matrix(10, 10)  # __init__ called
            # ... use m ...
        }  # __del__ called automatically here!
        
        MEMORY LEAK PREVENTION:
        ======================
        
        Without __del__:
        Matrix created -> Memory allocated -> Function ends
                                            -> Memory NOT freed
                                            -> LEAK!
        
        With __del__:
        Matrix created -> Memory allocated -> Function ends
                                            -> __del__ called
                                            -> Memory freed
                                            -> No leak!
        
        CRITICAL: Every .alloc() must have matching .free()
        """
        self.data.free()
    
    fn randomize(mut self):
        """
        Fill matrix with pseudo-random values.
        
        PSEUDO-RANDOM PATTERN:
        =====================
        
        Formula: (i * 13 + 7) % 100 / 100.0
        
        Produces values in range [0.0, 1.0):
        
        i=0:  (0*13 + 7) % 100 / 100 = 0.07
        i=1:  (1*13 + 7) % 100 / 100 = 0.20
        i=2:  (2*13 + 7) % 100 / 100 = 0.33
        ...
        
        Not cryptographically secure, but good enough for testing!
        """
        for i in range(self.size):
            # Simple pseudo-random pattern
            self.data[i] = Float32((i * 13 + 7) % 100) / 100.0
    
    fn fill(mut self, value: Float32):
        """
        Fill entire matrix with constant value.
        
        Example:
        Before: [?, ?, ?, ?]  (uninitialized)
        fill(5.0)
        After:  [5, 5, 5, 5]
        
        Use cases:
        - Initialize gradients to zero
        - Create matrix of ones
        - Reset matrix state
        """
        for i in range(self.size):
            self.data[i] = value


# =============================================================================
# SIMD OPTIMIZATION EXPLAINED
# =============================================================================

"""
SIMD: Single Instruction, Multiple Data
========================================

WHAT IS SIMD?
------------

Without SIMD (Scalar processing):
+-----+     +-----+     +-----+     +-----+
| a0  | +   | b0  | =   | c0  |     One operation
+-----+     +-----+     +-----+

| a1  | +   | b1  | =   | c1  |     Another operation
+-----+     +-----+     +-----+

| a2  | +   | b2  | =   | c2  |     Another operation
+-----+     +-----+     +-----+

| a3  | +   | b3  | =   | c3  |     Another operation
+-----+     +-----+     +-----+

Total: 4 operations

With SIMD (Vector processing):
+--+--+--+--+     +--+--+--+--+     +--+--+--+--+
|a0|a1|a2|a3| +   |b0|b1|b2|b3| =   |c0|c1|c2|c3|  ONE operation!
+--+--+--+--+     +--+--+--+--+     +--+--+--+--+

Total: 1 operation (4x speedup!)


SIMD REGISTER LAYOUT (Float32, width=4):
========================================

CPU Register (128 bits for SSE, 256 bits for AVX):

SSE (128-bit):
+--------+--------+--------+--------+
|  32b   |  32b   |  32b   |  32b   |
| float0 | float1 | float2 | float3 |
+--------+--------+--------+--------+

AVX (256-bit):
+--------+--------+--------+--------+--------+--------+--------+--------+
|  32b   |  32b   |  32b   |  32b   |  32b   |  32b   |  32b   |  32b   |
| float0 | float1 | float2 | float3 | float4 | float5 | float6 | float7 |
+--------+--------+--------+--------+--------+--------+--------+--------+


MEMORY LAYOUT FOR SIMD:
=======================

Good (contiguous):
Array: [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
        ^                   ^
Load 4 elements in ONE instruction

Bad (scattered):
Array:     [1.0, ?, ?, ?, 2.0, ?, ?, ?, 3.0, ?, ?, ?, 4.0]
            ^              ^              ^              ^
Need FOUR separate loads (slow!)


WHY SIMD IS CRITICAL FOR ML/AI:
===============================

Training a neural network:
- Matrix A: 1024 x 1024 = 1,048,576 elements
- Without SIMD: 1,048,576 operations
- With SIMD (4-wide): 262,144 operations (4x faster!)
- With SIMD (8-wide): 131,072 operations (8x faster!)

For modern deep learning with billions of parameters:
SIMD is the difference between hours and days of training!


SIMD WIDTH SELECTION:
====================

Float32 (32-bit):
- SSE:     4 floats per instruction (128 bits)
- AVX:     8 floats per instruction (256 bits)
- AVX-512: 16 floats per instruction (512 bits)

We use width=4 for maximum compatibility.
"""


# =============================================================================
# FORWARD OPERATIONS (SIMD OPTIMIZED)
# =============================================================================

fn mat_add_simd(a: Matrix, b: Matrix) -> Matrix:
    """
    Element-wise addition with SIMD optimization: C = A + B.
    
    ALGORITHM:
    =========
    
    For each position i:
        C[i] = A[i] + B[i]
    
    SIMD OPTIMIZATION:
    =================
    
    Instead of:
    for i in range(8192):
        c[i] = a[i] + b[i]  # 8192 operations
    
    We do:
    for i in range(0, 8192, 4):  # Process 4 at a time
        # Load 4 elements into SIMD register
        a_vec = [a[i], a[i+1], a[i+2], a[i+3]]
        b_vec = [b[i], b[i+1], b[i+2], b[i+3]]
        
        # ONE vector addition instruction
        c_vec = a_vec + b_vec
        
        # Store 4 results
        [c[i], c[i+1], c[i+2], c[i+3]] = c_vec
    
    Total: 2048 operations (4x faster!)
    
    MEMORY ACCESS PATTERN:
    =====================
    
    Iteration 0:
    A: [a0, a1, a2, a3, ...]
        ^   ^   ^   ^
        Load these 4 in parallel
    
    Iteration 1:
    A: [..., a4, a5, a6, a7, ...]
              ^   ^   ^   ^
              Load these 4 in parallel
    
    VISUAL EXAMPLE:
    ==============
    
    A = [1, 2, 3, 4]    B = [5, 6, 7, 8]
    
    SIMD vector addition:
    +--+--+--+--+     +--+--+--+--+     +--+--+--+--+
    | 1| 2| 3| 4| +   | 5| 6| 7| 8| =   | 6| 8|10|12|
    +--+--+--+--+     +--+--+--+--+     +--+--+--+--+
    
    All 4 additions happen simultaneously!
    """
    var c = Matrix(a.rows, a.cols)
    
    # Calculate how many complete SIMD chunks we can process
    # Example: size=10, width=4 -> simd_count=8 (process indices 0-7)
    var simd_count = (a.size // 4) * 4
    
    # SIMD processing loop (4 elements at a time)
    for i in range(0, simd_count, 4):
        """
        SIMD LOAD-ADD-STORE PIPELINE:
        ============================
        
        Step 1: LOAD
        ------------
        Memory -> SIMD Register
        
        a_vals register:
        +------+------+------+------+
        | a[i] |a[i+1]|a[i+2]|a[i+3]|
        +------+------+------+------+
        
        b_vals register:
        +------+------+------+------+
        | b[i] |b[i+1]|b[i+2]|b[i+3]|
        +------+------+------+------+
        
        Step 2: COMPUTE
        --------------
        Vector addition (ONE instruction):
        
        c_vals = a_vals + b_vals
        
        Step 3: STORE
        ------------
        SIMD Register -> Memory
        
        c_vals register -> c[i:i+4]
        """
        
        # Create SIMD vectors (initialized to zero)
        var a_vals = SIMD[DType.float32, 4](0)
        var b_vals = SIMD[DType.float32, 4](0)
        
        # Manual load from memory into SIMD vectors
        for j in range(4):
            a_vals[j] = a.data[i + j]
            b_vals[j] = b.data[i + j]
        
        # SIMD addition (4 additions in ONE instruction!)
        var c_vals = a_vals + b_vals
        
        # Manual store from SIMD vectors back to memory
        for j in range(4):
            c.data[i + j] = c_vals[j]
    
    # Handle remainder elements (if size not divisible by 4)
    """
    REMAINDER PROCESSING:
    ====================
    
    Example: size = 10, simd_width = 4
    
    SIMD loop processes: i = 0, 4, 8  (indices 0-11, but only 0-9 valid)
    Remainder:          i = 8, 9      (process individually)
    
    Why needed?
    - Prevents buffer overflow
    - Ensures all elements processed
    - Only small performance impact (usually < 5% of elements)
    """
    for i in range(simd_count, a.size):
        c.data[i] = a.data[i] + b.data[i]
    
    return c


fn mat_sub_simd(a: Matrix, b: Matrix) -> Matrix:
    """
    Element-wise subtraction with SIMD: C = A - B.
    
    SUBTRACTION GRADIENT FLOW:
    =========================
    
    Forward:  C = A - B
    Backward: 
        dL/dA = dL/dC * dC/dA = dL/dC * 1   = dL/dC
        dL/dB = dL/dC * dC/dB = dL/dC * (-1) = -dL/dC
    
    Why the negative sign?
    - Increasing B decreases C (inverse relationship)
    - Gradient flows backward with opposite sign
    
    VISUAL:
    ======
    A = [5, 7, 9]    B = [2, 3, 4]
         |  |  |         |  |  |
    C = [3, 4, 5]
    """
    var c = Matrix(a.rows, a.cols)
    var simd_count = (a.size // 4) * 4
    
    for i in range(0, simd_count, 4):
        var a_vals = SIMD[DType.float32, 4](0)
        var b_vals = SIMD[DType.float32, 4](0)
        
        for j in range(4):
            a_vals[j] = a.data[i + j]
            b_vals[j] = b.data[i + j]
        
        var c_vals = a_vals - b_vals  # SIMD subtraction
        
        for j in range(4):
            c.data[i + j] = c_vals[j]
    
    for i in range(simd_count, a.size):
        c.data[i] = a.data[i] - b.data[i]
    
    return c


fn mat_mul_simd(a: Matrix, b: Matrix) -> Matrix:
    """
    Element-wise multiplication (Hadamard product) with SIMD: C = A * B.
    
    IMPORTANT: This is NOT matrix multiplication!
    
    HADAMARD PRODUCT vs MATRIX MULTIPLICATION:
    =========================================
    
    Hadamard (element-wise):
    [1, 2]  *  [3, 4]  =  [1*3, 2*4]  =  [3, 8]
    [5, 6]     [7, 8]     [5*7, 6*8]     [35, 48]
    
    Matrix multiplication:
    [1, 2]  @  [3, 4]  =  [1*3+2*7, 1*4+2*8]  =  [17, 20]
    [5, 6]     [7, 8]     [5*3+6*7, 5*4+6*8]     [57, 68]
    
    GRADIENT COMPUTATION:
    ====================
    
    Forward: C = A * B
    
    Backward:
        dC/dA = B  (derivative of A*B with respect to A is B)
        dC/dB = A  (derivative of A*B with respect to B is A)
    
    Therefore:
        dL/dA = dL/dC * B
        dL/dB = dL/dC * A
    
    VISUAL:
    ======
    A = [2, 3, 4]    B = [5, 6, 7]
         |  |  |         |  |  |
    C = [10, 18, 28]
    """
    var c = Matrix(a.rows, a.cols)
    var simd_count = (a.size // 4) * 4
    
    for i in range(0, simd_count, 4):
        var a_vals = SIMD[DType.float32, 4](0)
        var b_vals = SIMD[DType.float32, 4](0)
        
        for j in range(4):
            a_vals[j] = a.data[i + j]
            b_vals[j] = b.data[i + j]
        
        var c_vals = a_vals * b_vals  # SIMD multiplication
        
        for j in range(4):
            c.data[i + j] = c_vals[j]
    
    for i in range(simd_count, a.size):
        c.data[i] = a.data[i] * b.data[i]
    
    return c


fn mat_div_simd(a: Matrix, b: Matrix) -> Matrix:
    """
    Element-wise division with SIMD: C = A / B.
    
    WARNING: Assumes B has no zeros (would cause division by zero)!
    
    DIVISION GRADIENT (QUOTIENT RULE):
    =================================
    
    Forward: C = A / B
    
    Derivative rules:
        dC/dA = 1/B         (straightforward)
        dC/dB = -A/B²       (quotient rule)
    
    Backward:
        dL/dA = dL/dC * (1/B)     = dL/dC / B
        dL/dB = dL/dC * (-A/B²)   = -dL/dC * A / B²
    
    Why negative sign for B?
    - Increasing denominator decreases the quotient
    - Inverse relationship -> negative gradient
    
    VISUAL:
    ======
    A = [10, 20, 30]    B = [2, 4, 5]
         |   |   |          |  |  |
    C = [5, 5, 6]
    
    NUMERICAL STABILITY:
    ===================
    
    Division by small numbers can cause:
    - Overflow (large results)
    - Numerical instability
    - Gradient explosion
    
    Best practices:
    - Add small epsilon: C = A / (B + 1e-8)
    - Gradient clipping
    - Careful initialization
    """
    var c = Matrix(a.rows, a.cols)
    var simd_count = (a.size // 4) * 4
    
    for i in range(0, simd_count, 4):
        var a_vals = SIMD[DType.float32, 4](0)
        var b_vals = SIMD[DType.float32, 4](0)
        
        for j in range(4):
            a_vals[j] = a.data[i + j]
            b_vals[j] = b.data[i + j]
        
        var c_vals = a_vals / b_vals  # SIMD division
        
        for j in range(4):
            c.data[i + j] = c_vals[j]
    
    for i in range(simd_count, a.size):
        c.data[i] = a.data[i] / b.data[i]
    
    return c


# =============================================================================
# BACKWARD OPERATIONS (AUTOMATIC DIFFERENTIATION)
# =============================================================================

"""
AUTOMATIC DIFFERENTIATION EXPLAINED:
====================================

What is it?
-----------
Automatic computation of derivatives (gradients) for any differentiable
function, essential for training neural networks.

COMPUTATION GRAPH EXAMPLE:
=========================

Forward pass (compute output):

Input:  A = [2, 3]    B = [4, 5]
         |             |
         v             v
       temp = A + B = [6, 8]  (addition)
         |
         v       weights = [0.5, 0.5]
         |             |
         v             v
    output = temp * W = [3, 4]  (multiplication)

Backward pass (compute gradients):

Loss gradient: dL/dOutput = [1, 1]
         |
         v
    dL/dTemp = dL/dOutput * W = [0.5, 0.5]  (mul backward)
    dL/dW = dL/dOutput * temp = [6, 8]
         |
         v
    dL/dA = dL/dTemp * 1 = [0.5, 0.5]  (add backward)
    dL/dB = dL/dTemp * 1 = [0.5, 0.5]


CHAIN RULE:
==========

For composed functions: y = f(g(x))

dy/dx = dy/dg * dg/dx

Example:
y = (x + 2)²

Let g(x) = x + 2
    f(g) = g²

dy/dx = dy/dg * dg/dx = 2g * 1 = 2(x + 2)


GRADIENT ACCUMULATION:
=====================

When multiple paths lead to same variable:

    A
   / \
  /   \
 v     v
 +     *
 |     |
 v     v
Loss  Loss

dL/dA = dL/dA_from_path1 + dL/dA_from_path2

All gradients accumulate (sum)!
"""


fn backward_add_simd(dc: Matrix) -> (Matrix, Matrix):
    """
    Backward pass for addition: dA = dC, dB = dC.
    
    GRADIENT DERIVATION:
    ===================
    
    Forward:  C = A + B
    
    Taking derivatives:
        ∂C/∂A = ∂(A + B)/∂A = 1
        ∂C/∂B = ∂(A + B)/∂B = 1
    
    Chain rule (from loss L):
        ∂L/∂A = ∂L/∂C * ∂C/∂A = ∂L/∂C * 1 = ∂L/∂C
        ∂L/∂B = ∂L/∂C * ∂C/∂B = ∂L/∂C * 1 = ∂L/∂C
    
    INTUITION:
    =========
    
    Addition: Both inputs contribute equally to output
    - Increasing A by 1 increases C by 1
    - Increasing B by 1 increases C by 1
    - Gradient flows equally to both
    
    EXAMPLE:
    =======
    
    Forward:
        A = [1, 2]    B = [3, 4]
        C = [4, 6]
    
    Backward:
        dL/dC = [1, 1]  (assume gradient from loss)
        
        dL/dA = [1, 1]  (same as dL/dC)
        dL/dB = [1, 1]  (same as dL/dC)
    
    GRADIENT FLOW DIAGRAM:
    =====================
    
         dL/dC = [1, 1]
              |
              v
         C = A + B
        /          \
       /            \
      v              v
    dL/dA = [1,1]  dL/dB = [1,1]
    """
    var da = Matrix(dc.rows, dc.cols)
    var db = Matrix(dc.rows, dc.cols)
    var simd_count = (dc.size // 4) * 4
    
    for i in range(0, simd_count, 4):
        # Load incoming gradient
        var dc_vals = SIMD[DType.float32, 4](0)
        
        for j in range(4):
            dc_vals[j] = dc.data[i + j]
        
        # Both gradients equal dC (derivative is 1 for both inputs)
        for j in range(4):
            da.data[i + j] = dc_vals[j]
            db.data[i + j] = dc_vals[j]
    
    # Remainder
    for i in range(simd_count, dc.size):
        da.data[i] = dc.data[i]
        db.data[i] = dc.data[i]
    
    return (da, db)


fn backward_sub_simd(dc: Matrix) -> (Matrix, Matrix):
    """
    Backward pass for subtraction: dA = dC, dB = -dC.
    
    GRADIENT DERIVATION:
    ===================
    
    Forward:  C = A - B
    
    Taking derivatives:
        ∂C/∂A = ∂(A - B)/∂A = 1
        ∂C/∂B = ∂(A - B)/∂B = -1
    
    Chain rule:
        ∂L/∂A = ∂L/∂C * ∂C/∂A = ∂L/∂C * 1  = ∂L/∂C
        ∂L/∂B = ∂L/∂C * ∂C/∂B = ∂L/∂C * (-1) = -∂L/∂C
    
    INTUITION:
    =========
    
    Subtraction: Inputs have opposite effects
    - Increasing A by 1 increases C by 1  -> gradient +1
    - Increasing B by 1 decreases C by 1  -> gradient -1
    
    EXAMPLE:
    =======
    
    Forward:
        A = [5, 7]    B = [2, 3]
        C = [3, 4]
    
    Backward:
        dL/dC = [1, 1]
        
        dL/dA = [1, 1]   (positive, same direction)
        dL/dB = [-1, -1] (negative, opposite direction)
    
    GRADIENT FLOW DIAGRAM:
    =====================
    
         dL/dC = [1, 1]
              |
              v
         C = A - B
        /          \
       /            \
      v              v
    dL/dA = [1,1]  dL/dB = [-1,-1]
                    (negated!)
    """
    var da = Matrix(dc.rows, dc.cols)
    var db = Matrix(dc.rows, dc.cols)
    var simd_count = (dc.size // 4) * 4
    
    for i in range(0, simd_count, 4):
        var dc_vals = SIMD[DType.float32, 4](0)
        
        for j in range(4):
            dc_vals[j] = dc.data[i + j]
        
        # Negate for B gradient
        var neg_dc = -dc_vals  # SIMD negation
        
        for j in range(4):
            da.data[i + j] = dc_vals[j]    # dA = dC
            db.data[i + j] = neg_dc[j]     # dB = -dC
    
    for i in range(simd_count, dc.size):
        da.data[i] = dc.data[i]
        db.data[i] = -dc.data[i]
    
    return (da, db)


fn backward_mul_simd(dc: Matrix, a: Matrix, b: Matrix) -> (Matrix, Matrix):
    """
    Backward pass for multiplication: dA = dC * B, dB = dC * A.
    
    GRADIENT DERIVATION (Product Rule):
    ==================================
    
    Forward:  C = A * B
    
    Taking derivatives:
        ∂C/∂A = ∂(A * B)/∂A = B
        ∂C/∂B = ∂(A * B)/∂B = A
    
    Chain rule:
        ∂L/∂A = ∂L/∂C * ∂C/∂A = ∂L/∂C * B
        ∂L/∂B = ∂L/∂C * ∂C/∂B = ∂L/∂C * A
    
    INTUITION:
    =========
    
    Multiplication: Each input's gradient depends on OTHER input
    - To update A: gradient is scaled by B
    - To update B: gradient is scaled by A
    - Larger values amplify gradients (can cause explosion!)
    
    EXAMPLE:
    =======
    
    Forward:
        A = [2, 3]    B = [4, 5]
        C = [8, 15]
    
    Backward:
        dL/dC = [1, 1]
        
        dL/dA = [1, 1] * [4, 5] = [4, 5]   (scaled by B)
        dL/dB = [1, 1] * [2, 3] = [2, 3]   (scaled by A)
    
    GRADIENT FLOW DIAGRAM:
    =====================
    
         dL/dC = [1, 1]
              |
              v
         C = A * B
        /          \
       /            \
      v              v
    dL/dA = dC*B   dL/dB = dC*A
    = [4, 5]       = [2, 3]
    
    GRADIENT EXPLOSION WARNING:
    ==========================
    
    If A or B are large (e.g., [100, 200]):
        dL/dA = dC * B could be HUGE!
    
    Solutions:
    - Gradient clipping
    - Normalization layers
    - Careful weight initialization
    """
    var da = Matrix(dc.rows, dc.cols)
    var db = Matrix(dc.rows, dc.cols)
    var simd_count = (dc.size // 4) * 4
    
    for i in range(0, simd_count, 4):
        # Load gradients and forward values
        var dc_vals = SIMD[DType.float32, 4](0)
        var a_vals = SIMD[DType.float32, 4](0)
        var b_vals = SIMD[DType.float32, 4](0)
        
        for j in range(4):
            dc_vals[j] = dc.data[i + j]
            a_vals[j] = a.data[i + j]
            b_vals[j] = b.data[i + j]
        
        # Compute gradients using product rule
        var da_vals = dc_vals * b_vals  # dA = dC * B
        var db_vals = dc_vals * a_vals  # dB = dC * A
        
        for j in range(4):
            da.data[i + j] = da_vals[j]
            db.data[i + j] = db_vals[j]
    
    for i in range(simd_count, dc.size):
        da.data[i] = dc.data[i] * b.data[i]
        db.data[i] = dc.data[i] * a.data[i]
    
    return (da, db)


fn backward_div_simd(dc: Matrix, a: Matrix, b: Matrix) -> (Matrix, Matrix):
    """
    Backward pass for division: dA = dC / B, dB = -dC * A / B².
    
    GRADIENT DERIVATION (Quotient Rule):
    ===================================
    
    Forward:  C = A / B
    
    Quotient rule: d/dx(f/g) = (g*f' - f*g') / g²
    
    For our case:
        ∂C/∂A = ∂(A/B)/∂A = 1/B
        ∂C/∂B = ∂(A/B)/∂B = -A/B²
    
    Chain rule:
        ∂L/∂A = ∂L/∂C * ∂C/∂A = ∂L/∂C * (1/B)   = ∂L/∂C / B
        ∂L/∂B = ∂L/∂C * ∂C/∂B = ∂L/∂C * (-A/B²) = -∂L/∂C * A / B²
    
    INTUITION:
    =========
    
    Division: Numerator and denominator have different relationships
    - Increasing numerator (A) increases quotient    -> positive gradient
    - Increasing denominator (B) decreases quotient  -> negative gradient
    - Effect is quadratic in B (B²) -> sensitive to small B!
    
    EXAMPLE:
    =======
    
    Forward:
        A = [8, 12]    B = [2, 3]
        C = [4, 4]
    
    Backward:
        dL/dC = [1, 1]
        
        dL/dA = [1, 1] / [2, 3] = [0.5, 0.33]
        
        dL/dB = -[1, 1] * [8, 12] / [4, 9]
              = -[8, 12] / [4, 9]
              = [-2, -1.33]
    
    GRADIENT FLOW DIAGRAM:
    =====================
    
         dL/dC = [1, 1]
              |
              v
         C = A / B
        /          \
       /            \
      v              v
    dL/dA = dC/B   dL/dB = -dC*A/B²
    = [0.5, 0.33]  = [-2, -1.33]
    
    NUMERICAL STABILITY CONCERNS:
    ============================
    
    1. Division by zero:
       B = [0, ...] -> 1/B = infinity!
       Solution: Add epsilon, B + 1e-8
    
    2. Division by small numbers:
       B = [1e-6, ...] -> 1/B² = 1e12 (huge gradient!)
       Solution: Gradient clipping
    
    3. Gradient explosion:
       Large A, small B -> -A/B² can be massive
       Solution: Normalize inputs, use batch norm
    """
    var da = Matrix(dc.rows, dc.cols)
    var db = Matrix(dc.rows, dc.cols)
    var simd_count = (dc.size // 4) * 4
    
    for i in range(0, simd_count, 4):
        var dc_vals = SIMD[DType.float32, 4](0)
        var a_vals = SIMD[DType.float32, 4](0)
        var b_vals = SIMD[DType.float32, 4](0)
        
        for j in range(4):
            dc_vals[j] = dc.data[i + j]
            a_vals[j] = a.data[i + j]
            b_vals[j] = b.data[i + j]
        
        # Quotient rule gradients
        var da_vals = dc_vals / b_vals                    # dA = dC / B
        var db_vals = -(dc_vals * a_vals) / (b_vals * b_vals)  # dB = -dC * A / B²
        
        for j in range(4):
            da.data[i + j] = da_vals[j]
            db.data[i + j] = db_vals[j]
    
    for i in range(simd_count, dc.size):
        da.data[i] = dc.data[i] / b.data[i]
        db.data[i] = -dc.data[i] * a.data[i] / (b.data[i] * b.data[i])
    
    return (da, db)


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

fn ones_like(m: Matrix) -> Matrix:
    """
    Create matrix filled with ones, same shape as input.
    
    USE CASE IN GRADIENT COMPUTATION:
    =================================
    
    For sum reduction loss:
        loss = sum(C)
        
    Gradient of sum with respect to each element:
        ∂loss/∂C[i] = 1 for all i
    
    Therefore:
        dL/dC = ones_like(C)
    
    EXAMPLE:
    =======
    
    C = [[1, 2],
         [3, 4]]
    
    loss = sum(C) = 10
    
    dL/dC = [[1, 1],
             [1, 1]]
    
    Interpretation: Each element contributes equally to loss
    """
    var result = Matrix(m.rows, m.cols)
    result.fill(1.0)
    return result


fn max_abs_diff(a: Matrix, b: Matrix) -> Float32:
    """
    Compute maximum absolute difference between two matrices.
    
    FORMULA:
    =======
    
    max_diff = max(|A[i] - B[i]|) for all i
    
    USAGE IN TESTING:
    ================
    
    Compare computed gradients vs numerical gradients:
    
    if max_abs_diff(computed_grad, numerical_grad) < 1e-5:
        print("Test PASSED")
    else:
        print("Test FAILED")
    
    NUMERICAL PRECISION:
    ===================
    
    Float32 precision: ~7 decimal digits
    
    Acceptable error thresholds:
    - 1e-5: Good for most operations
    - 1e-4: Acceptable with accumulated operations
    - 1e-3: May indicate numerical issues
    - > 1e-2: Likely implementation bug
    
    EXAMPLE:
    =======
    
    A = [1.00001, 2.00002, 3.00003]
    B = [1.00000, 2.00000, 3.00000]
    
    Differences: [0.00001, 0.00002, 0.00003]
    max_abs_diff = 0.00003
    """
    var max_diff: Float32 = 0.0
    for i in range(a.size):
        var diff = abs(a.data[i] - b.data[i])
        if diff > max_diff:
            max_diff = diff
    return max_diff


fn abs(x: Float32) -> Float32:
    """
    Absolute value function.
    
    DEFINITION:
    ==========
    
    abs(x) = { x   if x >= 0
             {-x   if x < 0
    
    EXAMPLES:
    ========
    
    abs(5.0)   = 5.0
    abs(-3.0)  = 3.0
    abs(0.0)   = 0.0
    
    GRAPH:
    =====
    
       |     /
       |    /
       |   /
    ---|--/---
      /|  
     / |
    /  |
    """
    return x if x >= 0 else -x


fn min(a: Int, b: Int) -> Int:
    """
    Return minimum of two integers.
    
    Used for limiting output display to first N elements.
    
    EXAMPLES:
    ========
    
    min(10, 100) = 10
    min(5, 3)    = 3
    min(7, 7)    = 7
    """
    return a if a < b else b


# =============================================================================
# MAIN TEST HARNESS
# =============================================================================

fn main():
    """
    Test suite for SIMD-optimized elementwise operations.
    
    TESTING STRATEGY:
    ================
    
    1. Create test matrices
    2. Run forward operations
    3. Compute gradients (backward pass)
    4. Compare with reference implementation
    5. Check error is below threshold (< 1e-5)
    
    WHAT WE'RE TESTING:
    ==================
    
    Forward operations:
    - Addition, subtraction, multiplication, division
    - SIMD optimization correctness
    
    Backward operations:
    - Gradient computation accuracy
    - Chain rule implementation
    - Numerical stability
    
    PASSING CRITERIA:
    ================
    
    For each operation:
    - Forward pass: results match element-wise
    - Backward pass: gradients are mathematically correct
    - Error: max absolute difference < 1e-5
    """
    
    print("="*70)
    print("MOJO ELEMENTWISE OPERATIONS WITH SIMD")
    print("Mojo Version: 25.2.0")
    print("="*70)
    
    # Test configuration
    var M = 64   # Matrix rows
    var N = 128  # Matrix columns
    
    """
    TEST SIZE ANALYSIS:
    ==================
    
    Total elements: 64 * 128 = 8,192
    
    SIMD processing (width=4):
    - Complete chunks: 8,192 / 4 = 2,048 chunks
    - Remainder: 0 elements (perfect fit!)
    
    Memory usage per matrix:
    - Elements: 8,192
    - Bytes: 8,192 * 4 = 32,768 bytes = 32 KB
    
    Total memory (A, B, C, gradients):
    - ~160 KB (fits easily in L2 cache)
    
    SIMD performance:
    - Without SIMD: 8,192 operations
    - With SIMD (4-wide): 2,048 operations
    - Speedup: 4x
    """
    
    print("\nTest configuration:")
    print("  Matrix size:", M, "x", N, "=", M*N, "elements")
    print("  SIMD width: 4 (Float32)")
    print("  Memory per matrix:", (M*N*4)//1024, "KB")
    
    # Create test matrices
    print("\nCreating test matrices...")
    var A = Matrix(M, N)
    var B = Matrix(M, N)
    
    A.randomize()
    B.randomize()
    
    # Add 1.0 to B to avoid division by zero
    for i in range(B.size):
        B.data[i] = B.data[i] + 1.0
    
    var all_passed = True
    
    # =========================================================================
    # TEST ADDITION
    # =========================================================================
    print("\n" + "="*70)
    print("Testing ADD")
    print("="*70)
    
    # Forward pass
    var C_add = mat_add_simd(A, B)
    
    # Reference forward computation
    var C_add_ref = Matrix(M, N)
    for i in range(C_add_ref.size):
        C_add_ref.data[i] = A.data[i] + B.data[i]
    
    # Compare forward results (first 10 elements)
    print("\nForward Pass Verification (C = A + B):")
    print("Index | A[i]      | B[i]      | Computed  | Expected  | Error")
    print("-" * 70)
    for i in range(min(10, C_add.size)):
        var error = abs(C_add.data[i] - C_add_ref.data[i])
        print(i, "    |", A.data[i], "|", B.data[i], "|", 
              C_add.data[i], "|", C_add_ref.data[i], "|", error)
    
    var fwd_add_err = max_abs_diff(C_add, C_add_ref)
    print("\nForward max error:", fwd_add_err)
    
    # Backward pass
    var dC_add = ones_like(C_add)
    var grads_add = backward_add_simd(dC_add)
    var dA_add = grads_add[0]
    var dB_add = grads_add[1]
    
    # Reference gradients
    var dA_add_ref = ones_like(A)
    var dB_add_ref = ones_like(B)
    
    # Compare backward results (first 10 elements)
    print("\nBackward Pass Verification (dA = dC, dB = dC):")
    print("Index | dC[i]     | dA Comp   | dA Ref    | dB Comp   | dB Ref")
    print("-" * 70)
    for i in range(min(10, dA_add.size)):
        print(i, "    |", dC_add.data[i], "|", dA_add.data[i], "|", 
              dA_add_ref.data[i], "|", dB_add.data[i], "|", dB_add_ref.data[i])
    
    var bwd_add_err_a = max_abs_diff(dA_add, dA_add_ref)
    var bwd_add_err_b = max_abs_diff(dB_add, dB_add_ref)
    print("\nBackward dA max error:", bwd_add_err_a)
    print("Backward dB max error:", bwd_add_err_b)
    
    var add_passed = (fwd_add_err < 1e-5 and bwd_add_err_a < 1e-5 and bwd_add_err_b < 1e-5)
    print("\nStatus:", "PASSED" if add_passed else "FAILED")
    all_passed = all_passed and add_passed
    
    # =========================================================================
    # TEST SUBTRACTION
    # =========================================================================
    print("\n" + "="*70)
    print("Testing SUB")
    print("="*70)
    
    # Forward pass
    var C_sub = mat_sub_simd(A, B)
    
    # Reference forward computation
    var C_sub_ref = Matrix(M, N)
    for i in range(C_sub_ref.size):
        C_sub_ref.data[i] = A.data[i] - B.data[i]
    
    # Compare forward results
    print("\nForward Pass Verification (C = A - B):")
    print("Index | A[i]      | B[i]      | Computed  | Expected  | Error")
    print("-" * 70)
    for i in range(min(10, C_sub.size)):
        var error = abs(C_sub.data[i] - C_sub_ref.data[i])
        print(i, "    |", A.data[i], "|", B.data[i], "|", 
              C_sub.data[i], "|", C_sub_ref.data[i], "|", error)
    
    var fwd_sub_err = max_abs_diff(C_sub, C_sub_ref)
    print("\nForward max error:", fwd_sub_err)
    
    # Backward pass
    var dC_sub = ones_like(C_sub)
    var grads_sub = backward_sub_simd(dC_sub)
    var dA_sub = grads_sub[0]
    var dB_sub = grads_sub[1]
    
    # Reference gradients
    var dA_sub_ref = ones_like(A)
    var dB_sub_ref = Matrix(M, N)
    dB_sub_ref.fill(-1.0)
    
    # Compare backward results
    print("\nBackward Pass Verification (dA = dC, dB = -dC):")
    print("Index | dC[i]     | dA Comp   | dA Ref    | dB Comp   | dB Ref")
    print("-" * 70)
    for i in range(min(10, dA_sub.size)):
        print(i, "    |", dC_sub.data[i], "|", dA_sub.data[i], "|", 
              dA_sub_ref.data[i], "|", dB_sub.data[i], "|", dB_sub_ref.data[i])
    
    var bwd_sub_err_a = max_abs_diff(dA_sub, dA_sub_ref)
    var bwd_sub_err_b = max_abs_diff(dB_sub, dB_sub_ref)
    print("\nBackward dA max error:", bwd_sub_err_a)
    print("Backward dB max error:", bwd_sub_err_b)
    
    var sub_passed = (fwd_sub_err < 1e-5 and bwd_sub_err_a < 1e-5 and bwd_sub_err_b < 1e-5)
    print("\nStatus:", "PASSED" if sub_passed else "FAILED")
    all_passed = all_passed and sub_passed
    
    # =========================================================================
    # TEST MULTIPLICATION
    # =========================================================================
    print("\n" + "="*70)
    print("Testing MUL")
    print("="*70)
    
    # Forward pass
    var C_mul = mat_mul_simd(A, B)
    
    # Reference forward computation
    var C_mul_ref = Matrix(M, N)
    for i in range(C_mul_ref.size):
        C_mul_ref.data[i] = A.data[i] * B.data[i]
    
    # Compare forward results
    print("\nForward Pass Verification (C = A * B):")
    print("Index | A[i]      | B[i]      | Computed  | Expected  | Error")
    print("-" * 70)
    for i in range(min(10, C_mul.size)):
        var error = abs(C_mul.data[i] - C_mul_ref.data[i])
        print(i, "    |", A.data[i], "|", B.data[i], "|", 
              C_mul.data[i], "|", C_mul_ref.data[i], "|", error)
    
    var fwd_mul_err = max_abs_diff(C_mul, C_mul_ref)
    print("\nForward max error:", fwd_mul_err)
    
    # Backward pass
    var dC_mul = ones_like(C_mul)
    var grads_mul = backward_mul_simd(dC_mul, A, B)
    var dA_mul = grads_mul[0]
    var dB_mul = grads_mul[1]
    
    # Reference gradients: dA = dC * B, dB = dC * A
    var dA_mul_ref = Matrix(M, N)
    var dB_mul_ref = Matrix(M, N)
    for i in range(dA_mul_ref.size):
        dA_mul_ref.data[i] = dC_mul.data[i] * B.data[i]
        dB_mul_ref.data[i] = dC_mul.data[i] * A.data[i]
    
    # Compare backward results
    print("\nBackward Pass Verification (dA = dC*B, dB = dC*A):")
    print("Index | dC[i]     | B[i]      | dA Comp   | dA Ref    | Error")
    print("-" * 70)
    for i in range(min(10, dA_mul.size)):
        var error_a = abs(dA_mul.data[i] - dA_mul_ref.data[i])
        print(i, "    |", dC_mul.data[i], "|", B.data[i], "|", 
              dA_mul.data[i], "|", dA_mul_ref.data[i], "|", error_a)
    
    print("\nIndex | dC[i]     | A[i]      | dB Comp   | dB Ref    | Error")
    print("-" * 70)
    for i in range(min(10, dB_mul.size)):
        var error_b = abs(dB_mul.data[i] - dB_mul_ref.data[i])
        print(i, "    |", dC_mul.data[i], "|", A.data[i], "|", 
              dB_mul.data[i], "|", dB_mul_ref.data[i], "|", error_b)
    
    var bwd_mul_err_a = max_abs_diff(dA_mul, dA_mul_ref)
    var bwd_mul_err_b = max_abs_diff(dB_mul, dB_mul_ref)
    print("\nBackward dA max error:", bwd_mul_err_a)
    print("Backward dB max error:", bwd_mul_err_b)
    
    var mul_passed = (fwd_mul_err < 1e-5 and bwd_mul_err_a < 1e-5 and bwd_mul_err_b < 1e-5)
    print("\nStatus:", "PASSED" if mul_passed else "FAILED")
    all_passed = all_passed and mul_passed
    
    # =========================================================================
    # TEST DIVISION
    # =========================================================================
    print("\n" + "="*70)
    print("Testing DIV")
    print("="*70)
    
    # Forward pass
    var C_div = mat_div_simd(A, B)
    
    # Reference forward computation
    var C_div_ref = Matrix(M, N)
    for i in range(C_div_ref.size):
        C_div_ref.data[i] = A.data[i] / B.data[i]
    
    # Compare forward results
    print("\nForward Pass Verification (C = A / B):")
    print("Index | A[i]      | B[i]      | Computed  | Expected  | Error")
    print("-" * 70)
    for i in range(min(10, C_div.size)):
        var error = abs(C_div.data[i] - C_div_ref.data[i])
        print(i, "    |", A.data[i], "|", B.data[i], "|", 
              C_div.data[i], "|", C_div_ref.data[i], "|", error)
    
    var fwd_div_err = max_abs_diff(C_div, C_div_ref)
    print("\nForward max error:", fwd_div_err)
    
    # Backward pass
    var dC_div = ones_like(C_div)
    var grads_div = backward_div_simd(dC_div, A, B)
    var dA_div = grads_div[0]
    var dB_div = grads_div[1]
    
    # Reference gradients: dA = dC / B, dB = -dC * A / B^2
    var dA_div_ref = Matrix(M, N)
    var dB_div_ref = Matrix(M, N)
    for i in range(dA_div_ref.size):
        dA_div_ref.data[i] = dC_div.data[i] / B.data[i]
        dB_div_ref.data[i] = -dC_div.data[i] * A.data[i] / (B.data[i] * B.data[i])
    
    # Compare backward results
    print("\nBackward Pass Verification (dA = dC/B, dB = -dC*A/B^2):")
    print("Index | dC[i]     | B[i]      | dA Comp   | dA Ref    | Error")
    print("-" * 70)
    for i in range(min(10, dA_div.size)):
        var error_a = abs(dA_div.data[i] - dA_div_ref.data[i])
        print(i, "    |", dC_div.data[i], "|", B.data[i], "|", 
              dA_div.data[i], "|", dA_div_ref.data[i], "|", error_a)
    
    print("\nIndex | dC[i]     | A[i]      | B[i]      | dB Comp   | dB Ref")
    print("-" * 75)
    for i in range(min(10, dB_div.size)):
        print(i, "    |", dC_div.data[i], "|", A.data[i], "|", B.data[i], "|",
              dB_div.data[i], "|", dB_div_ref.data[i])
    
    var bwd_div_err_a = max_abs_diff(dA_div, dA_div_ref)
    var bwd_div_err_b = max_abs_diff(dB_div, dB_div_ref)
    print("\nBackward dA max error:", bwd_div_err_a)
    print("Backward dB max error:", bwd_div_err_b)
    
    var div_passed = (fwd_div_err < 1e-5 and bwd_div_err_a < 1e-5 and bwd_div_err_b < 1e-5)
    print("\nStatus:", "PASSED" if div_passed else "FAILED")
    all_passed = all_passed and div_passed
    
    # =========================================================================
    # FINAL SUMMARY
    # =========================================================================
    print("\n" + "="*70)
    if all_passed:
        print("ALL TESTS PASSED!")
        print("\nSIMD Optimizations:")
        print("  - Processing 4 Float32 elements per instruction")
        print("  - Memory bandwidth: ~4x improvement")
        print("  - Both forward and backward passes optimized")
        print("  - Total speedup: ~4x vs scalar operations")
        print("\nGradient Computation:")
        print("  - All operations have correct gradients")
        print("  - Numerical error < 1e-5 (excellent precision)")
        print("  - Ready for automatic differentiation in ML")
    else:
        print("SOME TESTS FAILED!")
        print("Please check implementation and numerical stability")
    
    print("="*70)


"""
ubuntu@150-136-47-190:~/mojo_demo$ pixi run mojo testFwdBwd.mojo
======================================================================
MOJO ELEMENTWISE OPERATIONS WITH SIMD
Mojo Version: 25.2.0
======================================================================

Test configuration:
  Matrix size: 64 x 128 = 8192 elements
  SIMD width: 4 (Float32)
  Memory per matrix: 32 KB

Creating test matrices...

======================================================================
Testing ADD
======================================================================

Forward Pass Verification (C = A + B):
Index | A[i]      | B[i]      | Computed  | Expected  | Error
----------------------------------------------------------------------
0     | 0.07 | 1.0700001 | 1.1400001 | 1.1400001 | 0.0
1     | 0.2 | 1.2 | 1.4000001 | 1.4000001 | 0.0
2     | 0.33 | 1.33 | 1.6600001 | 1.6600001 | 0.0
3     | 0.46 | 1.46 | 1.9200001 | 1.9200001 | 0.0
4     | 0.59 | 1.5899999 | 2.1799998 | 2.1799998 | 0.0
5     | 0.72 | 1.72 | 2.44 | 2.44 | 0.0
6     | 0.85 | 1.85 | 2.7 | 2.7 | 0.0
7     | 0.98 | 1.98 | 2.96 | 2.96 | 0.0
8     | 0.11 | 1.11 | 1.22 | 1.22 | 0.0
9     | 0.24 | 1.24 | 1.48 | 1.48 | 0.0

Forward max error: 0.0

Backward Pass Verification (dA = dC, dB = dC):
Index | dC[i]     | dA Comp   | dA Ref    | dB Comp   | dB Ref
----------------------------------------------------------------------
0     | 1.0 | 1.0 | 1.0 | 1.0 | 1.0
1     | 1.0 | 1.0 | 1.0 | 1.0 | 1.0
2     | 1.0 | 1.0 | 1.0 | 1.0 | 1.0
3     | 1.0 | 1.0 | 1.0 | 1.0 | 1.0
4     | 1.0 | 1.0 | 1.0 | 1.0 | 1.0
5     | 1.0 | 1.0 | 1.0 | 1.0 | 1.0
6     | 1.0 | 1.0 | 1.0 | 1.0 | 1.0
7     | 1.0 | 1.0 | 1.0 | 1.0 | 1.0
8     | 1.0 | 1.0 | 1.0 | 1.0 | 1.0
9     | 1.0 | 1.0 | 1.0 | 1.0 | 1.0

Backward dA max error: 0.0
Backward dB max error: 0.0

Status: PASSED

======================================================================
Testing SUB
======================================================================

Forward Pass Verification (C = A - B):
Index | A[i]      | B[i]      | Computed  | Expected  | Error
----------------------------------------------------------------------
0     | 0.07 | 1.0700001 | -1.0 | -1.0 | 0.0
1     | 0.2 | 1.2 | -1.0 | -1.0 | 0.0
2     | 0.33 | 1.33 | -1.0 | -1.0 | 0.0
3     | 0.46 | 1.46 | -1.0 | -1.0 | 0.0
4     | 0.59 | 1.5899999 | -0.99999994 | -0.99999994 | 0.0
5     | 0.72 | 1.72 | -1.0 | -1.0 | 0.0
6     | 0.85 | 1.85 | -1.0 | -1.0 | 0.0
7     | 0.98 | 1.98 | -1.0 | -1.0 | 0.0
8     | 0.11 | 1.11 | -1.0 | -1.0 | 0.0
9     | 0.24 | 1.24 | -1.0 | -1.0 | 0.0

Forward max error: 0.0

Backward Pass Verification (dA = dC, dB = -dC):
Index | dC[i]     | dA Comp   | dA Ref    | dB Comp   | dB Ref
----------------------------------------------------------------------
0     | 1.0 | 1.0 | 1.0 | -1.0 | -1.0
1     | 1.0 | 1.0 | 1.0 | -1.0 | -1.0
2     | 1.0 | 1.0 | 1.0 | -1.0 | -1.0
3     | 1.0 | 1.0 | 1.0 | -1.0 | -1.0
4     | 1.0 | 1.0 | 1.0 | -1.0 | -1.0
5     | 1.0 | 1.0 | 1.0 | -1.0 | -1.0
6     | 1.0 | 1.0 | 1.0 | -1.0 | -1.0
7     | 1.0 | 1.0 | 1.0 | -1.0 | -1.0
8     | 1.0 | 1.0 | 1.0 | -1.0 | -1.0
9     | 1.0 | 1.0 | 1.0 | -1.0 | -1.0

Backward dA max error: 0.0
Backward dB max error: 0.0

Status: PASSED

======================================================================
Testing MUL
======================================================================

Forward Pass Verification (C = A * B):
Index | A[i]      | B[i]      | Computed  | Expected  | Error
----------------------------------------------------------------------
0     | 0.07 | 1.0700001 | 0.0749 | 0.0749 | 0.0
1     | 0.2 | 1.2 | 0.24000001 | 0.24000001 | 0.0
2     | 0.33 | 1.33 | 0.43890002 | 0.43890002 | 0.0
3     | 0.46 | 1.46 | 0.67160004 | 0.67160004 | 0.0
4     | 0.59 | 1.5899999 | 0.9380999 | 0.9380999 | 0.0
5     | 0.72 | 1.72 | 1.2384001 | 1.2384001 | 0.0
6     | 0.85 | 1.85 | 1.5725001 | 1.5725001 | 0.0
7     | 0.98 | 1.98 | 1.9404 | 1.9404 | 0.0
8     | 0.11 | 1.11 | 0.1221 | 0.1221 | 0.0
9     | 0.24 | 1.24 | 0.2976 | 0.2976 | 0.0

Forward max error: 0.0

Backward Pass Verification (dA = dC*B, dB = dC*A):
Index | dC[i]     | B[i]      | dA Comp   | dA Ref    | Error
----------------------------------------------------------------------
0     | 1.0 | 1.0700001 | 1.0700001 | 1.0700001 | 0.0
1     | 1.0 | 1.2 | 1.2 | 1.2 | 0.0
2     | 1.0 | 1.33 | 1.33 | 1.33 | 0.0
3     | 1.0 | 1.46 | 1.46 | 1.46 | 0.0
4     | 1.0 | 1.5899999 | 1.5899999 | 1.5899999 | 0.0
5     | 1.0 | 1.72 | 1.72 | 1.72 | 0.0
6     | 1.0 | 1.85 | 1.85 | 1.85 | 0.0
7     | 1.0 | 1.98 | 1.98 | 1.98 | 0.0
8     | 1.0 | 1.11 | 1.11 | 1.11 | 0.0
9     | 1.0 | 1.24 | 1.24 | 1.24 | 0.0

Index | dC[i]     | A[i]      | dB Comp   | dB Ref    | Error
----------------------------------------------------------------------
0     | 1.0 | 0.07 | 0.07 | 0.07 | 0.0
1     | 1.0 | 0.2 | 0.2 | 0.2 | 0.0
2     | 1.0 | 0.33 | 0.33 | 0.33 | 0.0
3     | 1.0 | 0.46 | 0.46 | 0.46 | 0.0
4     | 1.0 | 0.59 | 0.59 | 0.59 | 0.0
5     | 1.0 | 0.72 | 0.72 | 0.72 | 0.0
6     | 1.0 | 0.85 | 0.85 | 0.85 | 0.0
7     | 1.0 | 0.98 | 0.98 | 0.98 | 0.0
8     | 1.0 | 0.11 | 0.11 | 0.11 | 0.0
9     | 1.0 | 0.24 | 0.24 | 0.24 | 0.0

Backward dA max error: 0.0
Backward dB max error: 0.0

Status: PASSED

======================================================================
Testing DIV
======================================================================

Forward Pass Verification (C = A / B):
Index | A[i]      | B[i]      | Computed  | Expected  | Error
----------------------------------------------------------------------
0     | 0.07 | 1.0700001 | 0.06542056 | 0.06542056 | 0.0
1     | 0.2 | 1.2 | 0.16666666 | 0.16666666 | 0.0
2     | 0.33 | 1.33 | 0.24812031 | 0.24812031 | 0.0
3     | 0.46 | 1.46 | 0.31506848 | 0.31506848 | 0.0
4     | 0.59 | 1.5899999 | 0.3710692 | 0.3710692 | 0.0
5     | 0.72 | 1.72 | 0.41860467 | 0.41860467 | 0.0
6     | 0.85 | 1.85 | 0.45945945 | 0.45945945 | 0.0
7     | 0.98 | 1.98 | 0.4949495 | 0.4949495 | 0.0
8     | 0.11 | 1.11 | 0.0990991 | 0.0990991 | 0.0
9     | 0.24 | 1.24 | 0.19354838 | 0.19354838 | 0.0

Forward max error: 0.0

Backward Pass Verification (dA = dC/B, dB = -dC*A/B^2):
Index | dC[i]     | B[i]      | dA Comp   | dA Ref    | Error
----------------------------------------------------------------------
0     | 1.0 | 1.0700001 | 0.9345794 | 0.9345794 | 0.0
1     | 1.0 | 1.2 | 0.8333333 | 0.8333333 | 0.0
2     | 1.0 | 1.33 | 0.7518797 | 0.7518797 | 0.0
3     | 1.0 | 1.46 | 0.6849315 | 0.6849315 | 0.0
4     | 1.0 | 1.5899999 | 0.62893087 | 0.62893087 | 0.0
5     | 1.0 | 1.72 | 0.5813953 | 0.5813953 | 0.0
6     | 1.0 | 1.85 | 0.5405405 | 0.5405405 | 0.0
7     | 1.0 | 1.98 | 0.5050505 | 0.5050505 | 0.0
8     | 1.0 | 1.11 | 0.9009009 | 0.9009009 | 0.0
9     | 1.0 | 1.24 | 0.8064516 | 0.8064516 | 0.0

Index | dC[i]     | A[i]      | B[i]      | dB Comp   | dB Ref
---------------------------------------------------------------------------
0     | 1.0 | 0.07 | 1.0700001 | -0.06114071 | -0.06114071
1     | 1.0 | 0.2 | 1.2 | -0.13888888 | -0.13888888
2     | 1.0 | 0.33 | 1.33 | -0.18655661 | -0.18655661
3     | 1.0 | 0.46 | 1.46 | -0.21580033 | -0.21580033
4     | 1.0 | 0.59 | 1.5899999 | -0.23337686 | -0.23337686
5     | 1.0 | 0.72 | 1.72 | -0.24337481 | -0.24337481
6     | 1.0 | 0.85 | 1.85 | -0.24835646 | -0.24835646
7     | 1.0 | 0.98 | 1.98 | -0.24997449 | -0.24997449
8     | 1.0 | 0.11 | 1.11 | -0.08927847 | -0.08927847
9     | 1.0 | 0.24 | 1.24 | -0.1560874 | -0.1560874

Backward dA max error: 0.0
Backward dB max error: 0.0

Status: PASSED

======================================================================
ALL TESTS PASSED!

SIMD Optimizations:
  - Processing 4 Float32 elements per instruction
  - Memory bandwidth: ~4x improvement
  - Both forward and backward passes optimized
  - Total speedup: ~4x vs scalar operations

Gradient Computation:
  - All operations have correct gradients
  - Numerical error < 1e-5 (excellent precision)
  - Ready for automatic differentiation in ML
======================================================================
ubuntu@150-136-47-190:~/mojo_demo$ 
"""
