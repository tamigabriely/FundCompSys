// Tami Gabriely

import java.util.concurrent.Semaphore;
import java.util.*;

class Airport extends Thread{
    public static Random R = new Random();
    
    public static volatile int currentBus;
    
    public static int numP;
    public static int N;
    public static int K;
    public static int M;
    public static int thresh;
    
    public static volatile Semaphore[] mutex;
    
    public static volatile Semaphore[] getOn;
    public static volatile Semaphore[][] getOff;
    
    public static volatile int[] numOn;
    public static volatile int[][] numOff;
    
    public static volatile int[] numPass;
    
    private static class Passanger extends Thread {
        
        private int id; // id which identifies each thread
        private int on; // floor where the passanger gets on
        private int off; // floor where the passanger will get off
        private int bus; // identifies which shuttle it got on
        
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
                bus = currentBus;
                
                // get on shuttle
                
                try {
                    mutex[0].acquire();
                }catch(InterruptedException e){
                }
                
                //pick a stop to get off: (assuming no one wants to get off on the same stop that they got on
                off = R.nextInt((K-1));
                off = (on + off + 1) % K;
                // increment num waiting
                numOff[bus][off]++;
                //System.out.print("\t\t Num Off " + bus + ": ");
                //printA(numOff[bus]);
                
                mutex[0].release();
                
                // wait to arrive at stop
                try {
                    getOff[bus][off].acquire();
                }catch(InterruptedException e){
                }
                
                // get off shuttle
            }
        }
    }
    
    private static class Shuttle extends Thread {
        private int id; // id which identifies each thread
        private int trav;
        
        public Shuttle(int i){
            id = i;
        }
        
        public void run() {
            //int y = 0;
            trav = 0;
            for (int x = 0; x < K; x = ((x + 1) % K)){
                //y++;
                
                // travel
                int t = R.nextInt(100);
                trav = trav + t;
                try{
                    Thread.sleep(t);
                }catch (InterruptedException e){
                    System.out.println(e);
                }
                
                try {
                    mutex[0].acquire();
                }catch(InterruptedException e){
                }
                
                System.out.println(id + " Shuttle arrived at stop "+ x);
                System.out.println("Number of passangers on bus "+id+": " + numPass[id]);
                
                // let passangers off
                if (numOff[id][x] > 0){
                    for (int i = 0; i < numOff[id][x]; i++) {
                        getOff[id][x].release();
                    }
                    numPass[id] = numPass[id] - numOff[id][x];
                    numOff[id][x] = 0; // set the number waiting to the new number
                }
                
                
                System.out.println("1 Number of passangers on bus "+id+": " + numPass[id]);
                
                // let passangers on
                int numFree = N;
                numFree = numFree - numPass[id];
                
                int numLetOn = 0;
                if (trav < thresh) {
                    if (numOn[x] < numFree){
                        numLetOn = numOn[x];
                    } else {
                        numLetOn = numFree;
                    }
                } else {
                    System.out.println("Bus "+id+" needs to charge");
                }
                
                if (numOn[x] > 0) {
                    currentBus = id;
                    for (int i = 0; i < numLetOn; i++) {
                        getOn[x].release();
                    }
                    numPass[id] = numPass[id] + numLetOn;
                    numOn[x] = numOn[x] - numLetOn; // set the number waiting to the new number
                }
                
                System.out.println("2 Number of passangers on bus "+id+": " + numPass[id]);
                
                
                mutex[0].release();
                
                // if needs to charge and no one on the bus anymore
                if ((trav >= thresh) && (numPass[id] == 0)) {
                    System.out.println("Bus "+id+" traveling to charge");
                    // travel to charging station
                    try{
                        Thread.sleep(R.nextInt(100));
                    }catch (InterruptedException e){
                        System.out.println(e);
                    }
                    // spend time being charged
                    try{
                        Thread.sleep(R.nextInt(100));
                    }catch (InterruptedException e){
                        System.out.println(e);
                    }
                    // reset time spent traveling
                    trav = 0;
                    System.out.println("Bus "+id+" done charging");
                }
                
                
                
                // to the next stop
                
                /*
                // add another travel to offset bus arrivals
                if ((id %2) == 1) {
                    try{
                        Thread.sleep(R.nextInt(420));
                    }catch (InterruptedException e){
                        System.out.println(e);
                    }
                }
                */
                
                // to make it stop after a while
                //if (y == 33){
                //    break;
                //}
            }
        }
    }
    
    public static void main(String[] args) {
        numP = 50; // num passangers
        N = 10; // limit per shuttle
        K = 6; // number of terminals 
        M = 3; // number of shuttles
        thresh = 500; // when need to charge
        
        currentBus = 0;
        numPass = new int[M];
        
        Passanger[] p = new Passanger[numP];
        Shuttle[] s = new Shuttle[M];
        
        mutex = new Semaphore[2];
        mutex[0] = new Semaphore(1);
        mutex[1] = new Semaphore(1);
        
        numOn = new int[K];
        //numOff = new int[K];
        
        //initialize numOff and getOff
        numOff = new int[M][K];
        getOff = new Semaphore[M][K];
        for (int i = 0; i < M; i++){
            for (int j = 0; j < K; j++) {
                numOff[i][j] = 0;
                getOff[i][j] = new Semaphore(0);
            }
        }
        
        
        // initialize all stops semaphore to 0:
        getOn = new Semaphore[K];
        //getOff = new Semaphore[K];
        for (int i = 0; i < K; i++){
            getOn[i] = new Semaphore(0);
            //getOff[i] = new Semaphore(0);
            
            numOn[i] = 0;
        }
        
        // start all passangers
        for (int i = 0; i < numP; i++){
            p[i] = new Passanger(i);
            p[i].start();
        }
        
        // start all shuttles
        for (int i = 0; i < M; i++){
            numPass[i] = 0;
            
            s[i] = new Shuttle(i);
            s[i].start();
        }
    }  
}