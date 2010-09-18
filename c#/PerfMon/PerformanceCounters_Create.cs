/*
*   Corey Goldberg - 2010
*   C#/.NET - Windows Performance Counters (perfmon) - Creating
*   
*   Creates a Performance Counter Category and associated Counters.  
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
    }
}