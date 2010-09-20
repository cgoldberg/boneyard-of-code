// Corey Goldberg - 2010

using System;
using IBM.WMQ;



public class MQSeries
{
	private string queueName;
    private string replyQueueName;
    private string queueManagerName;
	
	private MQQueueManager queueManager;


    public MQSeries(string queueName, string queueManagerName, string host, string channel, int port)
    {
        MQEnvironment.Hostname = host;
        MQEnvironment.Channel = channel;
        MQEnvironment.Port = port;

        this.queueName = queueName;
		this.queueManagerName = queueManagerName;
		
		this.queueManager = new MQQueueManager(this.queueManagerName);
    }


    public MQSeries(string queueName, string replyQueueName, string queueManagerName, string host, string channel, int port)
    {
        MQEnvironment.Hostname = host;
        MQEnvironment.Channel = channel;
        MQEnvironment.Port = port; 
        
        this.queueName = queueName;
        this.replyQueueName = replyQueueName; 
        this.queueManagerName = queueManagerName;

        this.queueManager = new MQQueueManager(this.queueManagerName);
    }


    public void PutMessageOnQueue(string message)
    {   
        MQMessage queueMessage = new MQMessage();
        queueMessage.Format = MQC.MQFMT_STRING;
        queueMessage.Persistence = 0;
        queueMessage.WriteString(message);
        queueMessage.ReplyToQueueManagerName = this.queueManagerName;
        queueMessage.ReplyToQueueName = this.replyQueueName;

        this.queueManager.Put(this.queueName, this.queueManagerName, queueMessage);
    }


    public string GetMessageOffQueue()
    {
        string message = "";

        try
        {
            MQMessage queueMessage = new MQMessage();

            MQQueue queue = this.queueManager.AccessQueue(this.queueName, MQC.MQOO_INPUT_AS_Q_DEF + MQC.MQOO_FAIL_IF_QUIESCING);
            queueMessage.Format = MQC.MQFMT_STRING;
            queue.Get(queueMessage);
			
            message = queueMessage.ReadString(queueMessage.MessageLength);
			
			queue.Close();
        }
        catch (MQException mqexp)
        {
        }

        return message;
    }


}




   