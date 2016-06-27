// Tami Gabriely

import java.util.concurrent.Semaphore;
import java.util.*;

class MyProcess extends Thread{
    private int id; // id which identifies each thread
    
    public MyProcess(int i){
        id = i;
        B[i] = new Semaphore(0); // intialize semaphore of each thread to 0
        R[i] = 0;
        numUsed[i] = 0;
    }
    
    public void run(){
        Random R = new Random();
        
        for (int k=1;k<=10;k++){
           
            newWait(id);
            
            System.out.println("Thread "+ id +" is in the CS " + k);
            
            try{
                Thread.sleep(R.nextInt(100));
            }catch (InterruptedException e){
                System.out.println(e);
            }
            
            newSignal(id);
            
            if (id == 1) {
                try{
                    Thread.sleep(R.nextInt(500));
                }catch (InterruptedException e){
                    System.out.println(e);
                }    
            }
            
        }
    }
        
    public void newWait(int i) {
        
        try {
            mutex.acquire();
        } catch(InterruptedException e) {
        }
        
        System.out.println("Thread "+ i +" is requesting CS");
        R[i] = 10 - numUsed[i]; // initialize priority 
        count++;
        if (count > 1) {
            try {
                B[i].acquire();
            } catch(InterruptedException e) {
            }
        }
        
        mutex.release();
    }
    
    public void newSignal(int i) {
        
        try {
            mutex0.acquire();
        } catch(InterruptedException e) {
        }
        
        R[i] = 0;
        count--;
        if (count > 0) {
            int j = 0;
            int highP = -1;
            for (int k = 0; k < R.length; k++) {
                if ((R[k] > highP) && (R[k] > 0)) {
                    j = k;
                }
            }
            B[j].release();
        }
        System.out.println("Thread "+ i +" is exiting CS");
        
        numUsed[i] = numUsed[i] +1;
        
        mutex0.release();
    }
    
    // counter to keep track of how many processes to let through
    private static volatile int count; 
    
    // array of binary semaphores so that each process can wait on its own
    private static volatile Semaphore[] B; 
    
    // array of priorities of the processes
    private static volatile int[] R;
    
    // mutual exclusion semaphore 
    private static volatile Semaphore mutex;
    private static volatile Semaphore mutex0;
    
    private static volatile int[] numUsed;
    
    public static void main(String[] args) {
        final int N = 5;
        
        MyProcess[] p = new MyProcess[N];
        
        count = 0;
        B = new Semaphore[N];
        R = new int[N];
        numUsed = new int[N];
        
        mutex = new Semaphore(1);
        mutex0 = new Semaphore(1);
        
        for (int i = 0; i < N; i++){
            p[i] = new MyProcess(i);
            p[i].start();
        }
    }
}