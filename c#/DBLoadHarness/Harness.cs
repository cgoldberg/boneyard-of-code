// Corey Goldberg - 2010

using System;
using System.Text;
using System.Configuration;
using System.Collections.Generic;
using System.Threading;



class Harness
{   
    
    static void Main()
    {
        // load settings from App.config
        string server = ConfigurationManager.AppSettings["server"];
        string dbName = ConfigurationManager.AppSettings["dbName"];
        string userName = ConfigurationManager.AppSettings["userName"];
        string password = ConfigurationManager.AppSettings["password"];
        long iterations = long.Parse(ConfigurationManager.AppSettings["iterations"]); 
        int waitTimeMillisecs = int.Parse(ConfigurationManager.AppSettings["waitTimeMillisecs"]);
        int numThreads = int.Parse(ConfigurationManager.AppSettings["numThreads"]);

        string connectionString = String.Format("Data Source={0};Initial Catalog={1};Persist Security Info=True;User ID={2};Password={3}", server, dbName, userName, password);

        List<Worker> workers = new List<Worker>();

        for (int i = 0; i < numThreads; i++)
        {
            Worker worker = new Worker(connectionString, iterations, waitTimeMillisecs);
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


