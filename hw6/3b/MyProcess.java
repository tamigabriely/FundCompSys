// Tami Gabriely

import java.util.concurrent.Semaphore;
import java.util.*;

class MyProcess extends Thread{
    private int id; // id which identifies each thread
    public MyProcess(int i){
        id = i;
    }
    
    public void run(){
        Random R = new Random();
        
        for (int k=0;k<5;k++){
            flag[id] = true;
            while (flag[1-id]) {
                if (!(turn == id)){
                    flag[id] = false;
                    while (flag[1-id]) {
                    }
                    flag[id] = true;
                }
            }
            System.out.println("Thread "+ id +" is starting iteration " + k);
            try{
                Thread.sleep(R.nextInt(21));
            }catch (InterruptedException e){
                System.out.println(e);
            }
            System.out.println("We hold these truths to be self-evident, that all men are created equal,");
            try{
                Thread.sleep(R.nextInt(21));
            }catch (InterruptedException e){
                System.out.println(e);
            }
            System.out.println("that they are endowed by their Creator with certain unalienable Rights,");
            try{
                Thread.sleep(R.nextInt(21));
            }catch (InterruptedException e){
                System.out.println(e);
            }
            System.out.println("that among these are Life, Liberty and the pursuit of Happiness.");
            try{
                Thread.sleep(R.nextInt(21));
            }catch (InterruptedException e){
                System.out.println(e);
            }
            System.out.println("Thread "+ id +" is done with iteration " + k);
            try{
                Thread.sleep(R.nextInt(21));
            }catch (InterruptedException e){
                System.out.println(e);
            }
            
            turn = 1-id;
            flag[id] = false;
        }
    }
    
    // For just one thread:
    /*
     public static void main(String[] args){    
     MyProcess p = new MyProcess(0);
     p.start();
     }
     */
    
    public static void main(String[] args) {
        final int N = 2;
        MyProcess[] p = new MyProcess[N];
        for (int i = 0; i < N; i++)
        {
            p[i] = new MyProcess(i);
            p[i].start();
        }
    }
    
    static volatile int Counter = 0; 
    static volatile int turn = 0;
    static volatile boolean[] flag = new boolean[2];
}