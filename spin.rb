#!/usr/bin/env ruby

def spin
    #Jeez Ruby, there *has* to be a better way to trap Ctrl-C
    #keyboard interrupts.
    bail = false
    trap("INT") {puts "\n\nok. bye!";exit}
    puts "" 
    while true do
        print("|")
        STDOUT.flush()
        sleep(0.1)
        print("\x08")
        STDOUT.flush()
        sleep(0.1)
        print ("/")
        STDOUT.flush()
        sleep(0.1)
        print("\x08")
        STDOUT.flush()
        sleep(0.1)
        print ("-")
        STDOUT.flush()
        sleep(0.1)
        print("\x08")
        STDOUT.flush()
        sleep(0.1)
        print ("\\")
        STDOUT.flush()
        sleep(0.1)
        print("\x08")
        STDOUT.flush()
        sleep(0.1)
        if bail: break end
    end 
end
puts "CTRL-C to exit."
spin() 
