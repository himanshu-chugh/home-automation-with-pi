#include<iostream>
using namespace std;
int main()
{
    int flag=0;
    int a[10]={0,1,2,3,4,5,6,7,8,9};
    int b[10];
    for(int i=0;i<10;i++){
        if(a[i]<10){
            int t=a[i];
            if(b[t]!=a[i]){
                b[t]=t;
                

            }
            else{
                flag=1;
                break;
            }

        }
        else{
            flag=1;
            break;
        }
    }
    if(flag==1){
        cout<<"not a good series";
    }else{
        cout<<"a good series";
    }
    
}