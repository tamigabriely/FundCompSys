// Tami Gabriely

import java.util.concurrent.Semaphore;
import java.util.*;

class Airport extends Thread{
    public static Random R = new Random();
    
    public static int numP;
    public static int N;
    public static int K;
    
    public static volatile Semaphore[] mutex;
    
    public static volatile Semaphore[] getOn;
    public static volatile Semaphore[] getOff;
    
    public static volatile int[] numOn;
    public static volatile int[] numOff;
    
    public static volatile int numPass;
    
    private static class Passanger extends Thread {
        
        private int id; // id which identifies each thread
        private int on; // floor where the passanger gets on
        private int off; // floor where the passanger will get off
        
        public Passanger(int i){
            id = i;
        }
        
        public void printA(int[] a) {
            for(int i =0; i < K; i++) {
                System.out.print(a[i] + " ");
            }
            System.out.println();
        }
        
        public void run(){
            while (true){
                
                try {
                    mutex[0].acquire();
                }catch(InterruptedException e){
                }
                
                //pick a stop to get on:
                on = R.nextInt(K);
                
                // increment num waiting
                numOn[on]++;
                //System.out.print("Num On: ");
                //printA(numOn);
                
                mutex[0].release();
                
                // wait for shuttle
                try {
                    getOn[on].acquire();
                }catch(InterruptedException e){
                }
                
                // get on shuttle
                
                try {
                    mutex[0].acquire();
                }catch(InterruptedException e){
                }
                
                //pick a stop to get off: (assuming no one wants to get off on the same stop that they got on
                off = R.nextInt((K-1));
                off = (on + off + 1) % K;
                // increment num waiting
                numOff[off]++;
                //System.out.print("\t\t Num Off: ");
                //printA(numOff);
                
                mutex[0].release();
                
                // wait to arrive at stop
                try {
                    getOff[off].acquire();
                }catch(InterruptedException e){
                }
                
                // get off shuttle

            }
        }
    }
    
    private static class Shuttle extends Thread {
        
        public void run() {
            //int y = 0;
            for (int x = 0; x < K; x = ((x + 1) % K)){
                //y++;
                
                // travel
                try{
                    Thread.sleep(R.nextInt(200));
                }catch (InterruptedException e){
                    System.out.println(e);
                }
                
                try {
                    mutex[0].acquire();
                }catch(InterruptedException e){
                }
                
                System.out.println("Shuttle arrived at stop "+ x);
                System.out.println("0 Number of passangers on bus: " + numPass);
                
                // let passangers off
                if (numOff[x] > 0){
                    for (int i = 0; i < numOff[x]; i++) {
                        getOff[x].release();
                    }
                    numPass = numPass - numOff[x];
                    numOff[x] = 0; // set the number waiting to the new number
                }
                
                
                //System.out.println("1 Number of passangers on bus: " + numPass);
                
                // let passangers on
                int numFree = N;
                numFree = numFree - numPass;
                
                int numLetOn = 0;
                if (numOn[x] < numFree){
                        numLetOn = numOn[x];
                    } else {
                        numLetOn = numFree;
                    }
                
                if (numOn[x] > 0) {
                    for (int i = 0; i < numLetOn; i++) {
                        getOn[x].release();
                    }
                    numPass = numPass + numLetOn;
                    numOn[x] = numOn[x] - numLetOn; // set the number waiting to the new number
                }
                
                //System.out.println("2 Number of passangers on bus: " + numPass);
                
                mutex[0].release();
                
                // to the next stop
                
                // to make it stop after a while
                //if (y == 19){
                //    break;
                //}
            }
        }
    }
    
    public static void main(String[] args) {
        numP = 50; // num passangers
        N = 10; // limit per shuttle
        K = 6; // number of terminals 
        
        Passanger[] p = new Passanger[numP];
        Shuttle s = new Shuttle();
        
        mutex = new Semaphore[2];
        mutex[0] = new Semaphore(1);
        mutex[1] = new Semaphore(1);
        
        numOn = new int[K];
        numOff = new int[K];
        
        
        // initialize all stops semaphore to 0:
        getOn = new Semaphore[K];
        getOff = new Semaphore[K];
        for (int i = 0; i < K; i++){
            getOn[i] = new Semaphore(0);
            getOff[i] = new Semaphore(0);
            
            numOn[i] = 0;
            numOff[i] = 0;
        }
        
        // start all passangers
        for (int i = 0; i < numP; i++){
            p[i] = new Passanger(i);
            p[i].start();
        }
        
        // start the shuttle
        s.start();
    }  
}