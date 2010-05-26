// Corey Goldberg - 2010

using System;
using System.Threading;



class Worker
{
    private int iterations;
    private int waitTimeMillisecs;

    private long numIterations;
    public long NumIterations { get { return numIterations; } }


    public Worker(int iterations, int waitTimeMillisecs)
    {
        this.waitTimeMillisecs = waitTimeMillisecs;
        this.iterations = iterations;
    }

	
    public void Run()
    {
       
        for (int i = 0; i < this.iterations; i++)
        {
            numIterations++;
            Thread.Sleep(this.waitTimeMillisecs);
        }
    }
	
}


