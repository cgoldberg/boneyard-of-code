/*
*   Corey Goldberg - 2010
*   C#/.NET - Windows Performance Counters (perfmon) - Creating and Updating
*   
*   Creates a Performance Counter Category and associated Counters.
*   Updates the Counters with random values (0-100) every 2 secs.   
*/

using System;
using System.Diagnostics;
using System.Threading;


class Program
{
    static void Main()
    {
        string categoryName = "Sample Perf Counters";
        string[] counterNames = {"Counter 1", "Counter 2"};
		
		
		CounterCreationDataCollection counters = new CounterCreationDataCollection();

        foreach (string counterName in counterNames) 
		{
			counters.Add(new CounterCreationData(counterName, "", PerformanceCounterType.NumberOfItems64));
		}
		
		if (PerformanceCounterCategory.Exists(categoryName))
		{
            PerformanceCounterCategory.Delete(categoryName);
		}
		
        PerformanceCounterCategory.Create(categoryName, "", PerformanceCounterCategoryType.SingleInstance, counters);
		
		
		Random rand = new Random();
		
        while (true)
        {
            foreach (string counterName in counterNames) 
			{	
				using (PerformanceCounter perfCounter = new PerformanceCounter(categoryName, counterName, false))
            	{
                	perfCounter.RawValue = rand.Next(101);
            	}
			}
			
            Thread.Sleep(2000);
        }
    }
}

