#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

int main(){

  int x = rand();
  printf("%d\n",x);
  x = rand();
  printf("%d\n",x);
  x = rand();
  printf("%d\n",x);
  x = rand();
  printf("%d\n",x);
  x = 1714636915 % 1337 - (1337 / 2);
  printf("%d\n",x);
  
}
