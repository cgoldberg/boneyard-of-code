// Corey Goldberg - 2010

using System;
using System.Configuration;
using System.Collections.Generic;
using System.Threading;



class AsyncHarness
{   
    
    static void Main()
    {
        // load settings from App.config
        string host = ConfigurationManager.AppSettings["hostName"];
        string queueManagerName = ConfigurationManager.AppSettings["queueManagerName"];
        string channel = ConfigurationManager.AppSettings["channel"];
        int port = Int32.Parse(ConfigurationManager.AppSettings["port"]);
		int putSleepTimeMillisecs = Int32.Parse(ConfigurationManager.AppSettings["putSleepTimeMillisecs"]);
		int getPollingTimeMillisecs = Int32.Parse(ConfigurationManager.AppSettings["getPollingTimeMillisecs"]);
		int iterations = Int32.Parse(ConfigurationManager.AppSettings["iterations"]);

        string[] queuePairNames = new string[8] { "queuePair1", "queuePair2", "queuePair3", "queuePair4", "queuePair5", "queuePair6", "queuePair7", "queuePair8" };
		
        List<string> validQueuePairNames = new List<string>();
		
		foreach (string qpName in queuePairNames)
		{
            string queuePairName = ConfigurationManager.AppSettings[qpName];

            if (!String.IsNullOrEmpty(queuePairName))
            {
                validQueuePairNames.Add(queuePairName);
            }
		}

        List<QueueLoader> queueLoaders = new List<QueueLoader>();

        foreach (string queuePairName in validQueuePairNames)
        {
            string[] queuePair = queuePairName.Split(',');
			
			QueueLoader ql = new QueueLoader(queuePair[0], queuePair[1], queueManagerName, channel, host, port, putSleepTimeMillisecs, iterations);
            queueLoaders.Add(ql);
            ThreadStart queueLoadJob = new ThreadStart(ql.Run);
            Thread queueLoadThread = new Thread(queueLoadJob);
            queueLoadThread.Start();
			
			QueueUnloader qu = new QueueUnloader(queuePair[1], queueManagerName, channel, host, port, getPollingTimeMillisecs);
            ThreadStart queueUnloadJob = new ThreadStart(qu.Run);
            Thread queueUnloadThread = new Thread(queueUnloadJob);
            queueUnloadThread.Start();
        }

        Console.WriteLine("\nMaking MQSeries connections...");
        Console.WriteLine(String.Format("  MQ Host: {0}", host));
        Console.WriteLine(String.Format("  Queue Manager: {0}", queueManagerName));
        Console.WriteLine(String.Format("  Channel: {0}", channel));
        Console.WriteLine(String.Format("  Port: {0}\n", port));
        Console.WriteLine("Queues:");
        foreach (string queuePairName in validQueuePairNames)
        {
            Console.WriteLine(String.Format("  {0}", queuePairName));
        }
        Console.WriteLine("-------------------------------------------\n");

        long numMsgs = 0;

        while (numMsgs < (iterations * validQueuePairNames.Count))
        {
            numMsgs = 0;

            foreach (QueueLoader ql in queueLoaders)
            {
                numMsgs += ql.NumMsgs;
            }

            Console.WriteLine("Messages: {0}", numMsgs);

            Thread.Sleep(500);
        }
    }
}




class QueueLoader
{
    private string queueName;
    private string replyQueueName;
    private string queueManagerName;
    private string channel;
    private string host;
    private int port;
    private int putSleepTimeMillisecs;
    private int iterations;

    private long numMsgs;
    public long NumMsgs { get { return numMsgs; } }


    public QueueLoader(string queueName, string replyQueueName, string queueManagerName, string channel, string host, int port, int putSleepTimeMillisecs, int iterations)
    {
        this.queueName = queueName;
        this.replyQueueName = replyQueueName;
        this.queueManagerName = queueManagerName;
        this.channel = channel;
        this.host = host;
        this.port = port;
        this.putSleepTimeMillisecs = putSleepTimeMillisecs;
        this.iterations = iterations;
    }

	
    public void Run()
    {
        MQSeries mq = new MQSeries(this.queueName, this.replyQueueName, this.queueManagerName, this.host, this.channel, this.port);

        for (int i = 0; i < this.iterations; i++)
        {
            mq.PutMessageOnQueue("TEST MESSAGE");
            
            numMsgs++;
            
            Thread.Sleep(this.putSleepTimeMillisecs);
        }
    }
	
}




class QueueUnloader
{
    private string queueName;
    private string queueManagerName;
    private string channel;
    private string host;
    private int port;
    private int getPollingTimeMillisecs;


    public QueueUnloader(string queueName, string queueManagerName, string channel, string host, int port, int getPollingTimeMillisecs)
    {
        this.queueName = queueName;
        this.queueManagerName = queueManagerName;
        this.channel = channel;
        this.host = host;
        this.port = port;
        this.getPollingTimeMillisecs = getPollingTimeMillisecs;
    }


    public void Run()
    {
        MQSeries mq = new MQSeries(this.queueName, this.queueManagerName, this.host, this.channel, this.port);

        while (true)
        {          
			string receivedMsg = mq.GetMessageOffQueue();
            if (!receivedMsg.Equals(""))
            {
                Thread.Sleep(this.getPollingTimeMillisecs);
            }
        }
    }
	
}


