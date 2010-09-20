// Corey Goldberg - 2010
// C#/.NET - accurate high precision timing



using System;
using System.Diagnostics;



class Program
{
   
    public static void Main()
    {
        DisplayTimerProperties();

        
        
        // don't use DateTime() for accurate high precision timing:

        DateTime start = DateTime.Now;

            // do timed work here

        DateTime stop = DateTime.Now;

        // don't do this. you won't accurate timing
        Console.WriteLine("{0} ms", (stop - start).TotalMilliseconds);

        // definitely don't do this. you won't accurate timing or full timer resolution
        Console.WriteLine("{0} ms", (stop - start).Milliseconds);
        

        
        // StopWatch() uses the operating system's high-resolution performance counter:
        
        Stopwatch stopWatch = Stopwatch.StartNew();

            // do timed work here

        stopWatch.Stop();

        // don't do this. you won't get full timer resolution
        Console.WriteLine("{0} ms", stopWatch.ElapsedMilliseconds);

        // do this to get accurate high precision timing
        Console.WriteLine("{0} ms", stopWatch.Elapsed.TotalMilliseconds);
    }

    

    public static void DisplayTimerProperties()
    {
        if (Stopwatch.IsHighResolution)
        {
            Console.WriteLine("Operations timed using the system's high-resolution performance counter.");
        }
        else 
        {
            Console.WriteLine("Operations timed using the DateTime class.");
        }

        long frequency = Stopwatch.Frequency;

        Console.WriteLine("  Timer frequency in ticks per second = {0}", frequency);

        long nanosecPerTick = (1000L*1000L*1000L) / frequency;

        Console.WriteLine("  Timer is accurate within {0} nanoseconds", nanosecPerTick);
    }
    
}