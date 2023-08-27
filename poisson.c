#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define MAX(x, y) (((x) > (y)) ? (x) : (y))

double L = 10; // cm
const int N = 1000;
double h = L/N; // cm

double grid[N][N] = {0};
int locked[N][N] = {0}; 

double omega = 0.8; // Relaxation parameter
long long int max_iter = 50000000;
long long int prt_iter = 1000; // Print every 1000 iterations
double err_th = 1e-8; // Error threshold

char* err_fname = "./out/max-error.txt";
char* arr_fname = "./out/grid-val.txt";

void init();

int main() {
    init(); // Set up the grid 
    
    /* Over-relaxed Gauss-Siedal */
    long long int iter = 0;
    double err = 0;
    int first_grid = 1;
    do {
        first_grid = 1;
        for(int x1=0;x1<N;x1++){
            for(int x2=0;x2<N;x2++){
                if(!locked[x1][x2]){ // If it's not locked
                    double prev = grid[x1][x2];
                    grid[x1][x2] = 0.25*(1+omega)*(grid[x1-1][x2]+grid[x1+1][x2]+grid[x1][x2-1]+grid[x1][x2+1]) - omega*grid[x1][x2];
                    double loc_err = abs(grid[x1][x2] - prev);
                    if(first_grid) {
                        err = loc_err;
                        first_grid = 0;
                    } else {
                        err = MAX(loc_err,err);
                    }
                }
            }
        }
        
        /* Writing output */ 
        if(iter%prt_iter == 0) {
            printf("Iteration: %lld\n",iter+1);
            printf("Error: %e\n",err);
            
            printf("Writing error to file: %s\n",err_fname);
            FILE* err_fp = fopen(err_fname,"a");
            fprintf(err_fp,"%lld\t%e\n",iter,err);
            fclose(err_fp);
            
            printf("Writing array to file: %s\n",arr_fname);
            FILE* arr_fp = fopen(arr_fname,"a");
            for(int x1=0;x1<N;x1++){
                for(int x2=0;x2<N;x2++)
                    fprintf(arr_fp,"%e%c",grid[x1][x2],(x1==N-1 and x2==N-1)?'\n':'\t');
            }
            fclose(arr_fp);
            printf("\n\n");
        }
        iter ++;
    }while(iter < max_iter && err > err_th);
    
    printf("Process done after %lld iterations\n",iter);
    printf("Error: %e",err);
    printf("Writing error to file: %s\n",err_fname);
    FILE* err_fp = fopen(err_fname,"a");
    fprintf(err_fp,"%lld\t%e\n",iter,err);
    fclose(err_fp);
    
    printf("Writing array to file: %s\n",arr_fname);
    FILE* arr_fp = fopen(arr_fname,"a");
    for(int x1=0;x1<N;x1++){
        for(int x2=0;x2<N;x2++)
            fprintf(arr_fp,"%e%c",grid[x1][x2],(x1==N-1 and x2==N-1)?'\n':'\t');
    }
    fclose(arr_fp);
    printf("\n\n");
    return 0;
}


void init(){ 
    /* Setting up the grids */
    /* Grounding the boundaries */
    for(int x1=0;x1<N;x1++){
        grid[x1][0] = grid[x1][N-1] = 0;
        locked[x1][0] = locked[x1][N-1] = 1; // Lock the boundaries
    }
    for(int x2=0;x2<N;x2++){
        grid[0][x2] = grid[N-1][x2] = 0;
        locked[0][x2] = locked[N-1][x2] = 1; // same 
    }
    
    /* Setting up the parallel plates */
    int PLATE1_N1 = N*4/10; 
    int PLATE1_N2s = N*2/10, PLATE1_N2e = N*8/10;
    
    int PLATE2_N1 = N*6/10;
    int PLATE2_N2s = N*2/10, PLATE2_N2e = N*8/10;
    
    for(int x2=PLATE1_N2s; x2<=PLATE1_N2e; x2++){
        grid[PLATE1_N1][x2] = 1; // V
        locked[PLATE1_N1][x2] = 1;
    }
    
    for(int x2=PLATE2_N2s; x2<=PLATE2_N2e; x2++){
        grid[PLATE2_N1][x2] = -1; // V
        locked[PLATE2_N1][x2] = 1;
    }
}
