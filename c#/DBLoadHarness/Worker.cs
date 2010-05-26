// Corey Goldberg - 2010

using System;
using System.Data;
using System.Data.SqlClient;
using System.Collections.Generic;
using System.Threading;



class Worker
{
    private string connectionString;
    private long iterations;
    private int waitTimeMillisecs;

    private long numIterations;
    public long NumIterations { get { return numIterations; } }

	

    public Worker(string connectionString, long iterations, int waitTimeMillisecs)
    {
        this.connectionString = connectionString;
        this.iterations = iterations;
        this.waitTimeMillisecs = waitTimeMillisecs;
    }

	
	
    public void Run()
    {
        Random rand = new Random(((int)DateTime.Now.Ticks) * Thread.CurrentThread.ManagedThreadId);
        int sleepTime = rand.Next(1, 5000);
        Thread.Sleep(sleepTime);
           
        for (int i = 0; i < this.iterations; i++)
        {
            using (SqlConnection connection = new SqlConnection(this.connectionString))
            {
                connection.Open(); 
                
                string command = "exec spMySproc @Foo=1,@Bar='baz'";
                SqlCommand cmd = new SqlCommand(command, connection);
                SqlDataReader reader = cmd.ExecuteReader();
                reader.Close();
            }

            numIterations++;
            Thread.Sleep(this.waitTimeMillisecs);
        }
    }

}


