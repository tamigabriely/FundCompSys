// Tami Gabriely

import java.util.concurrent.Semaphore;
import java.util.*;

class MyProcess extends Thread{
    public static Random R = new Random();
    public static volatile Semaphore[] mutex;
    public static volatile Semaphore[] dlock;
    public static volatile Semaphore lock;
    public static volatile Semaphore turn;
    public static volatile int[] num;
    private int id; // id which identifies each thread
    
    public MyProcess(int i){
        id = i;
    }
    
    public void run(){
        
        while (true){
            
            //pick a direction:
            int d = 0; // direction is north
            double x = R.nextDouble();
            if (x > 0.5) {
                d = 1; // direction is south
            }
            
            // wait for turn
            try {
                turn.acquire();
            }catch(InterruptedException e){
            }
            
            // wait on the appropriate mutex
            try {
                mutex[d].acquire();
            }catch(InterruptedException e){
            }
            
            num[d]++; 
            if (num[d] == 1) {
                // grab the lock
                try {
                    lock.acquire();
                }catch(InterruptedException e){
                }
            }
            
            
            mutex[d].release();
            turn.release();
            
            if (num[d] > 4) {
                // grab the dlock
                try {
                    dlock[d].acquire();
                }catch(InterruptedException e){
                }
            }
            
            // sleep / travel            
            System.out.println(d+ " Thread "+ id +" is starting");
            try{
                Thread.sleep(R.nextInt(21));
            }catch (InterruptedException e){
                System.out.println(e);
            }
            System.out.println(d + " Thread "+ id +" is ending");
            
            // wait on the appropriate mutex
            try {
                mutex[d].acquire();
            }catch(InterruptedException e){
            }
            
            num[d]--;
            
            if (num[d] >= 3){
                dlock[d].release();
            }
                        
            if (num[d] == 0) {
                lock.release();
            }
            
            mutex[d].release();
        }
    }
    
    public static void main(String[] args) {
        final int N = 20;
        MyProcess[] p = new MyProcess[N];
        
        mutex = new Semaphore[2];
        mutex[0] = new Semaphore(1);
        mutex[1] = new Semaphore(1);

        dlock = new Semaphore[2];
        dlock[0] = new Semaphore(0);
        dlock[1] = new Semaphore(0);
        
        lock = new Semaphore(1);
        turn = new Semaphore(1);
        
        num = new int[2];
        num[0] = 0;
        num[1] = 0;
        
        for (int i = 0; i < N; i++){
            p[i] = new MyProcess(i);
            p[i].start();
        }
    }    
}