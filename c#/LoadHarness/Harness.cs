// Corey Goldberg - 20010

using System;
using System.Configuration;
using System.Collections.Generic;
using System.Threading;



class Harness
{   
    
    static void Main()
    {
        // load settings from App.config
        int numThreads = Int32.Parse(ConfigurationManager.AppSettings["numThreads"]);
        int waitTimeMillisecs = Int32.Parse(ConfigurationManager.AppSettings["waitTimeMillisecs"]);
        int iterations = Int32.Parse(ConfigurationManager.AppSettings["iterations"]);

        List<Worker> workers = new List<Worker>();

        for (int i = 0; i < numThreads; i++)
        {
            Worker worker = new Worker(iterations, waitTimeMillisecs);
            workers.Add(worker);
            ThreadStart job = new ThreadStart(worker.Run);
            Thread t = new Thread(job);
            t.Start();
        }

        long numIterations = 0;

        while (numIterations < (iterations * numThreads))
        {
            numIterations = 0;

            foreach (Worker worker in workers)
            {
                numIterations += worker.NumIterations;
            }

            Console.WriteLine("Iterations: {0}", numIterations);

            Thread.Sleep(500);
        }
    }
}


