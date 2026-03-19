#include <stdio.h>
#include <stdlib.h>

#define N 32  // Matrix size (32x32) - large enough for L2, small enough to finish

void multiply() {
    double *A = (double *)malloc(N * N * sizeof(double));
    double *B = (double *)malloc(N * N * sizeof(double));
    double *C = (double *)malloc(N * N * sizeof(double));

    // Initialize matrices
    for (int i = 0; i < N * N; i++) {
        A[i] = 1.0; B[i] = 2.0; C[i] = 0.0;
    }

    printf("Starting Matrix Multiplication (%dx%d)...\n", N, N);

    // Actual Multiplication (This will stress the MSHRs and L2)
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            for (int k = 0; k < N; k++) {
                C[i * N + j] += A[i * N + k] * B[k * N + j];
            }
        }
    }

    printf("Multiplication Complete. Sum: %f\n", C[0]);
    free(A); free(B); free(C);
}

int main() {
    multiply();
    return 0;
}
