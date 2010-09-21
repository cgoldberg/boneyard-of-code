/*
*   Corey Goldberg - 2010
*   C#/.NET - Windows Performance Counters (perfmon) - Creating and Updating
*   
*   Creates a Performance Counter Category and associated Counters.
*   References to counter instances are stored in a lookup Dictionary.
*   Updates the Counters with random values (0-100) every sec.   
*/



using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading;



class Program
{
    public static void Main()
    {
        string perfCounterCategoryName = "Sample Perf Counters";
        string[] perfCounterNames = { "Counter1", "Counter2" };
        bool overWriteCounters = true;
        
        Dictionary<string, PerformanceCounter> perfCounterLookup = CreatePerfCounters(perfCounterCategoryName, perfCounterNames, overWriteCounters);

        Random rand = new Random();

        while (true)
        {
            foreach (string perfCounterName in perfCounterNames)
            {
                perfCounterLookup[perfCounterName].RawValue = rand.Next(101);
            }

            Thread.Sleep(1000);
        }  
    }



    private static Dictionary<string, PerformanceCounter> CreatePerfCounters(string perfCounterCategoryName, string[] perfCounterNames, bool overWriteCounters)
    {
        CounterCreationDataCollection counters = new CounterCreationDataCollection();

        foreach (string perfCounterName in perfCounterNames)
        {
            counters.Add(new CounterCreationData(perfCounterName, "", PerformanceCounterType.NumberOfItems64));
        }

        if (overWriteCounters)
        {
            if (PerformanceCounterCategory.Exists(perfCounterCategoryName))
            {
                PerformanceCounterCategory.Delete(perfCounterCategoryName);
            }
            PerformanceCounterCategory.Create(perfCounterCategoryName, "", PerformanceCounterCategoryType.SingleInstance, counters);
        }
        else
        {
            if (!PerformanceCounterCategory.Exists(perfCounterCategoryName))
            {
                PerformanceCounterCategory.Create(perfCounterCategoryName, "", PerformanceCounterCategoryType.SingleInstance, counters);
            }
        }

        Dictionary<string, PerformanceCounter> perfCounterLookup = new Dictionary<string, PerformanceCounter>();

        foreach (string perfCounterName in perfCounterNames)
        {
            perfCounterLookup.Add(perfCounterName, new PerformanceCounter(perfCounterCategoryName, perfCounterName, false));
        }

        return perfCounterLookup;
    }

}