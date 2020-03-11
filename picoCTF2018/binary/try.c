#include <stdio.h>
//0000120d
void win(){
  printf("Yay! you made it!\n");
}

void vuln(){

  char buf[4];
  printf("please input 4 characters: ");
  gets(buf);
  printf("%s\n",buf);
  printf("buf: %p\n",buf);
  printf("1st char: %p\n",&buf[0]);
  printf("2nd char: %p\n",&buf[1]);
  printf("3rd char: %p\n",&buf[2]);
}

int main(){

vuln();
return 0;

}
