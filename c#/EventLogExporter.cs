// Corey Goldberg - 2008


using System;
using System.Diagnostics;


class EventLogExporter
{
    static void Main(string[] args)
    {
        EventLog evtLog = new EventLog("Application");  // Event Log type
        evtLog.MachineName = ".";  // dot is local machine
        
        foreach (EventLogEntry evtEntry in evtLog.Entries)
        {
            Console.WriteLine(evtEntry.Message);
        }
        
        evtLog.Close();
    }
}

