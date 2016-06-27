// Tami Gabriely

import java.util.concurrent.Semaphore;
import java.util.*;
import java.lang.*;

class MyProcess extends Thread{
    private int id; // id which identifies each thread
    public MyProcess(int i){
        id = i;
    }
    
    private int max(int[] a) {
        int m = 0;
        for (int i = 0; i < a.length; i++){
            if (a[i] >m) 
                m = a[i];
        }
        return m;
    }
    
    public void run(){
        Random R = new Random();
        
        for (int k=0;k<5;k++){
            //System.out.println(id + " starting entry for iteration " + k);

            ticket[id] = 1; 
            ticket[id] = max(ticket)+1;
            for (int j=0; j < ticket.length; j++) {
                while(ticket[j]!=0 && (ticket[j]<ticket[id])){}
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
            
            ticket[id] = 0;
        }
    }
    
    public static void main(String[] args) {
        final int N = 4;
        MyProcess[] p = new MyProcess[N];
        ticket = new int[N];
        
        for (int i = 0; i < N; i++){
            p[i] = new MyProcess(i);
            p[i].start();
        }
    }
    
    static volatile int[] ticket; 
}