/*
*   Corey Goldberg - 2010
*   C#/.NET - Windows Performance Counters (perfmon) - Creating and Updating
*   
*   Creates a Performance Counter Category and associated Counters.
*   Updates the Counters with random values (0-100) every 2 secs.   
*/



using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading;



class Program
{
    public static void Main()
    {
        string categoryName = "Sample Perf Counters";
        string[] counterNames = {"Counter 1", "Counter 2"};

        
        
        CounterCreationDataCollection counters = new CounterCreationDataCollection();

        foreach (string counterName in counterNames) 
        {
            counters.Add(new CounterCreationData(counterName, "", PerformanceCounterType.NumberOfItems64));
        }
    
    
        // example of recreating the counters
    
        if (PerformanceCounterCategory.Exists(categoryName))
        {
            PerformanceCounterCategory.Delete(categoryName);
        }
        PerformanceCounterCategory.Create(categoryName, "", PerformanceCounterCategoryType.SingleInstance, counters);
    
    
        // example of conditionally creating the counters
    
        if (!PerformanceCounterCategory.Exists(categoryName))
        {
            PerformanceCounterCategory.Create(categoryName, "", PerformanceCounterCategoryType.SingleInstance, counters);
        }
        
    
    
        // update the counters (don't create a new instance each time you update)
    
        List<PerformanceCounter> perfCounters = new List<PerformanceCounter>();

        foreach (string counterName in counterNames) 
        {
            perfCounters.Add(new PerformanceCounter(categoryName, counterName, false));
        }

        Random rand = new Random();

        while (true)
        {    
            foreach (PerformanceCounter perfCounter in perfCounters) 
            {	
                perfCounter.RawValue = rand.Next(101);
            }

            Thread.Sleep(2000);
        }
    }
}